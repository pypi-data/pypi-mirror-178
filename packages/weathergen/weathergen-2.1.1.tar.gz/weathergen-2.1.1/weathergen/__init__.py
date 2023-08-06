import time as ttime
import numpy as np
import scipy as sp
import pandas as pd
import h5py, os
from . import utils

RGI = sp.interpolate.RegularGridInterpolator

base, this_filename = os.path.split(__file__)
#base = '/users/tom/desktop/repos/weathergen/weathergen'

def get_sites(base):
    sites = pd.read_csv(f'{base}/sites.csv', index_col=0).fillna('')
    sites = sites.loc[[os.path.exists(f'{base}/site_data/{tag}.h5') for tag in sites.index]]
    return sites

sites = get_sites(base)
        
def generate(**kwargs): return weather(**kwargs)

class weather():

    def __init__(self, site=None, time=None):

        if site is None: site = 'princeton' # if no site is supplied, use 'princeton'
        if time is None: time = ttime.time() # if no time is supplied, use current time

        if not site in sites.index:
            raise ValueError(f'The site \'{site}\' is not supported. Available sites are:\n{list(sites.index)}')
    
        self.site, self.time = site, np.atleast_1d(time)
        self.lat, self.lon, self.alt = sites.loc[sites.index == self.site, ['lat', 'lon', 'alt']].values[0]

        self.quantiles = self.quantiles(np.linspace(0,1,1001))
        self.generate()

        # define some stuff
        if self.has_surface_data:

            self.rain_precipitation_rate[self.rain_precipitation_rate < 1e-3] = 0 # we ignore precipitation less than 0.001 mm/hr
            self.snow_precipitation_rate[self.snow_precipitation_rate < 1e-3] = 0
            
        if self.has_profile_data:

            self.cloud_cover = np.minimum(1, np.maximum(0, self.cloud_cover))

            for k in ['water_vapor', 'ozone', 'ice_water', 'snow_water', 'rain_water', 'liquid_water']:
                if not hasattr(self, f'surface_{k}'): setattr(self, f'surface_{k}', getattr(self, k)[0])
                setattr(self, f'column_{k}', np.trapz(np.r_[getattr(self, f'surface_{k}')[None], getattr(self, k)], np.r_[self.alt, self.height], axis=0))

        self.wind_bearing              = np.degrees(np.arctan2(self.wind_east, self.wind_north) + np.pi)
        self.wind_speed                = np.sqrt(np.square(self.wind_east) + np.square(self.wind_north))

        self.relative_humidity         = np.minimum(100, np.maximum(1, utils.AH_to_RH(self.temperature, self.water_vapor)))
        self.dew_point                 = utils.get_dew_point(self.temperature, self.relative_humidity)
        

            

    def generate(self):

        filename = f'{base}/site_data/{self.site}.h5'
        self._gen_data = {}
        with h5py.File(filename, 'r') as f:
            for key in list(f.keys()): 
                self._gen_data[key] = f[key][()] if not key == 'gen_labels' else f[key][()].astype(str)

        self.has_surface_data = self._gen_data['has_surface_data']
        self.has_profile_data = self._gen_data['has_profile_data']
        
        dt_gen = np.gradient(self.time).min()
        gen_time = np.arange(self.time.min(), self.time.max() + dt_gen, dt_gen)
            
        n_gen  = len(gen_time)
        f_gen  = np.fft.fftfreq(n_gen, dt_gen)

        self.year_day = list(map(utils.get_utc_year_day, gen_time))
        self.day_hour = list(map(utils.get_utc_day_hour, gen_time))

        GOOD    = ~np.isnan(self._gen_data['azdft_binned'])
        AZDFT   = np.c_[[sp.interpolate.interp1d(self._gen_data['azdft_freq'][g], azdft[g], fill_value=0, bounds_error=False, kind='cubic')(f_gen) 
                                                    for azdft, g in zip(self._gen_data['azdft_binned'], GOOD)]]

        GEN_DFT = AZDFT * np.sqrt(2 * n_gen / dt_gen) * np.exp(1j*np.random.uniform(low=0,high=2*np.pi,size=AZDFT.shape))
        GEN_V   = np.real(np.fft.ifft(GEN_DFT))
        ZD      = np.matmul(self._gen_data['eigenmodes'], GEN_V)

        yd_points = self._gen_data['year_day_edge_points']
        dh_points = self._gen_data['day_hour_edge_points']
        self.binned_mean_data = self._gen_data['binned_mean_grid']
        self.binned_norm_data = self._gen_data['binned_norm_grid']

        ZD *= RGI((yd_points, dh_points), self.binned_norm_data, method='linear')((self.year_day, self.day_hour)).T
        self.offset = RGI((yd_points, dh_points), self.binned_mean_data, method='linear')((self.year_day, self.day_hour)).T
        ZD += self.offset

        self.ZD = ZD.T
        QD = self._gen_data['QD']

        GD = np.zeros(ZD.shape)
        for i in range(GD.shape[0]):
            GD[i] = sp.interpolate.interp1d(self._gen_data['z'], QD[i], kind='quadratic',  bounds_error=False, fill_value='extrapolate')(ZD[i]) 

        for c, gd, qd in zip(self._gen_data['gen_labels'], 
                             np.split(GD, np.cumsum(self._gen_data['gen_widths'].astype(int))[:-1]),
                             np.split(QD, np.cumsum(self._gen_data['gen_widths'].astype(int))[:-1])):
            
            rs_gen = sp.interpolate.interp1d(gen_time, gd)(self.time)
            pctls  = sp.interpolate.interp1d(self._gen_data['q'], qd)(self.quantiles.q)
            if rs_gen.shape[0] == 1: rs_gen = rs_gen.ravel(); pctls = pctls.ravel()

            setattr(self, c, rs_gen)
            setattr(self.quantiles, c, pctls)

        if self.has_profile_data: setattr(self, 'height', self._gen_data['height'])
        
    class quantiles():

        def __init__(self, q):

            self.q = q