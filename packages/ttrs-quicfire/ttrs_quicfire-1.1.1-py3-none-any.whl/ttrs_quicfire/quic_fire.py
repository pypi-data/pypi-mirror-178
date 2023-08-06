# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:10:35 2022

@author: zcope
"""

#TT Libraries
from distutils.log import debug
import ttrs_quicfire.build_FF_domain as FF
import ttrs_quicfire.dat_file_functions as dat
import ttrs_quicfire.print_inp_files
import ttrs_quicfire.build_shapefiles as bs
from ttrs_quicfire.exceptions import WindDirOutOfRange, WindSpeedOutOfRange, DataLengthMismatch

#Standard Libraries
#import geopandas as gpd
import os
import numpy as np
import pandas as pd
from rasterio.features import geometry_mask
import sys
from shapely.geometry import Polygon, LineString

###############################################################################   
###Classes
class Shapefile_Paths:
    """
    Class contains shapefile names and locations
    """
    def __init__(self, SHAPE_PATH='default', burn_plot='burn_plot.shp', roads='roads.shp', 
             streams='streams.shp', wetlands='wetlands.shp', ignitions='ignitions.shp'): 
        def shapefile_check(self, file):
            """
            Returns path if shapefile exists. Else returns none.
            """
            temp_path = os.path.join(self.SHAPE_PATH, file)
            if os.path.exists(temp_path):
                return temp_path
                print('Shapefile folder contains: ' + file)
            else:
                print('[Error] File {file} not found.'.format(file=file))
                return None 
        
        if SHAPE_PATH=='default':
            SHAPE_PATH = bs.default_path('Shapefiles')
        self.SHAPE_PATH = SHAPE_PATH
        self.burn_plot = shapefile_check(self, burn_plot)
        self.roads = shapefile_check(self, roads)
        self.streams = shapefile_check(self, streams)
        self.wetlands = shapefile_check(self, wetlands)
        self.ignitions = shapefile_check(self, ignitions)
        self.bbox = None
        
        
class QF_Fuel_Arrays:
    """
    Class contains domain parameters
    """
    def __init__(self, domain, FUEL_PATH, use_topo=True): 
        self.dom = domain
        self.rhof = dat.fort_import(domain, os.path.join(FUEL_PATH, 'bulk_density.dat'))
        self.rhof_name = 'bulk_density.dat'
        self.moist = dat.fort_import(domain,  os.path.join(FUEL_PATH, 'moisture.dat'))
        self.moist_name = 'moisture.dat'
        self.depth = dat.fort_import(domain,  os.path.join(FUEL_PATH, 'depth.dat'))
        self.depth_name = 'depth.dat'
        self.topo = dat.fort_import(domain, os.path.join(FUEL_PATH, 'topo.dat'), False)
        self.topo_name = 'topo.dat'
        self.use_topo = use_topo
        self.fuel_arrs = [self.rhof,self.moist,self.depth,self.topo]
        self.name_arrs = [self.rhof_name,self.moist_name,self.depth_name,self.topo_name]
    
    def export_fuel(self, QF_PATH='default'):
        QF_PATH = self.dom.QF_PATH
        for i,f_arr in enumerate(self.fuel_arrs[:-1]):
            file_loc = os.path.join(QF_PATH, self.name_arrs[i])
            dat.fort_export(f_arr, file_loc)
        if self.use_topo:
            file_loc = os.path.join(QF_PATH, self.name_arrs[-1])
            dat.fort_export(self.fuel_arrs[-1], file_loc)

    def update_surface_moisture(self, moist_in_plot=0.1, moist_out_plot='default'):
        '''
        Removes fuel in cells that overlaps road 
        Input:
            buffer = int or float to buffer roads shapefile
        '''
        bbox_path = self.dom.shape_paths.bbox
        burn_plot_path = self.dom.shape_paths.burn_plot
        burn_plot = bs.clip_to_bbox(burn_plot_path, bbox_path)
        # Ensure burn plot is a ploygon
        if isinstance(burn_plot.iloc[0]['geometry'], LineString):
            burn_plot = bs.linestring_to_polygon(burn_plot)
        msk = self.mask_from_shape(burn_plot)

        z_layer = self.moist[0,:,:]
        z_layer[~msk] = moist_in_plot
        if moist_out_plot == 'default':
            moist_out_plot = moist_in_plot
        z_layer[msk] = moist_out_plot
        
    def mod_wetlands(self, fmc='default', bulk_density='default'):
        '''
        Removes modify fuel that intersect wetlands.shp
        '''
        bbox_path = self.dom.shape_paths.bbox
        wetlands_path = self.dom.shape_paths.wetlands
        try:
            wetlands = bs.load_shapefile(wetlands_path)
        except FileNotFoundError as e:
            print('[Error] File wetlands.shp not found, cannot run mod_wetlands()')
            answer = input('Continue building? (y/n) ')
            if answer[0].lower() == 'y':
                return
            else:
                sys.exit()
        wetlands = bs.clip_to_bbox(wetlands, bbox_path)
        
        # Ensure burn plot is a ploygon
        if isinstance(wetlands.iloc[0]['geometry'], LineString):
            wetlands = bs.linestring_to_polygon(wetlands)
        msk = self.mask_from_shape(wetlands)
        
        if fmc != 'default':
            z_layer = self.moist[0,:,:]
            z_layer[~msk] = fmc
        if bulk_density != 'default':
            z_layer = self.rhof[0,:,:]
            z_layer[~msk] = bulk_density
           
    def mask_from_shape(self, shape):
        dom = self.dom
        total_bounds = shape.total_bounds
    
        geoT = (dom.dx,0.0,total_bounds[0],
               0.0,dom.dy,total_bounds[1])    
        msk = geometry_mask(shape.geometry, np.shape(self.rhof[0,:,:]), geoT)
        
        #Orient location of mask
        shape_extent = shape.bounds
        msk = np.roll(msk, int(abs(dom.ymin-np.min(shape_extent['miny']))/dom.dy), axis=0)
        msk = np.roll(msk, int(abs(dom.xmin-np.min(shape_extent['minx']))/dom.dx), axis=1)
        return msk
    
    def build_fuelbreak(self, shape_path='default', buffer = 3):
        '''
        Removes fuel in cells that overlaps road 
        Input:
            buffer = int or float to buffer fuelbreak shapefile
        '''
        bbox_path = self.dom.shape_paths.bbox
        if shape_path == 'default':
            fb_path = self.dom.shape_paths.burn_plot
        else: fb_path = shape_path
        
        try:
            fuelbreak = bs.load_shapefile(fb_path)
        except:
            print('[Error] File burn_plot.shp not found, cannot run build_fuelbreak().\n')

        if isinstance(fuelbreak.iloc[0]['geometry'], Polygon):
            fuelbreak = bs.polygon_to_linestring(fuelbreak)
            #fuelbreak.to_file(os.path.join(self.dom.shape_paths.SHAPE_PATH, "TEST.shp"))
        
        fuelbreak = bs.clip_to_bbox(fuelbreak, bbox_path)
        fuelbreak = fuelbreak.buffer(buffer)
        fuelbreak = bs.clip_to_bbox(fuelbreak, bbox_path)
        msk = self.mask_from_shape(fuelbreak)

        for f_arr in self.fuel_arrs:
            if f_arr is not self.topo:
                for z in range(f_arr.shape[0]):
                    z_layer = f_arr[z,:,:]
                    z_layer[~msk] = 0
    
    def calc_normal_windfield(self, start_speed, start_dir, start_time=0, shift_int=300, SENSOR_HEIGHT=6.1):
        times = list(range(start_time, start_time + self.dom.sim_time + 1, shift_int))
        if start_speed <= 0 or start_speed > 20:
            raise WindSpeedOutOfRange(start_speed)
        if start_dir < 0 or start_dir >= 360:
            raise WindDirOutOfRange(start_dir)
        self.wind = WindShifts(times, start_speed, start_dir, SENSOR_HEIGHT)

    def custom_windfield(self, speeds, dirs, times, SENSOR_HEIGHT=6.1):
        if len(speeds) != len(times):
            raise DataLengthMismatch('Wind Speeds', len(speeds), 'Wind Times', len(times))
        if len(dirs) != len(times):
            raise DataLengthMismatch('Wind Directions', len(dirs), 'Wind Times', len(times))
        for speed in speeds:
            if speed <= 0 or speed > 20:
                raise WindSpeedOutOfRange(speed)
        for dir in dirs:
            if dir < 0 or dir >= 360:
                raise WindDirOutOfRange(dir)
        self.wind = WindShifts(times, speeds, dirs, SENSOR_HEIGHT, build=False)

#Currently only building normal wind field around
class WindShifts:
    """
    Class creates randomized wind field
    """
    def __init__(self, times, speed, dir, SENSOR_HEIGHT, build=True):
        self.times = times
        self.SENSOR_HEIGHT = SENSOR_HEIGHT
        if build:
            self.dirs = [dir]
            self.speeds = [speed]
            self.build_wind_field(len(self.times), self.dirs, self.speeds)
        else:
            self.dirs = dir
            self.speeds = speed
    
    def build_wind_field(self, num_values, dirs, speeds):
        for i in range(1,num_values):
            dir1 = np.random.normal(dirs[0], 30, 1)[0] + 360 #gen normal num from starting dir
            dir2 = np.random.normal(dirs[-1], 30, 1)[0] + 360 #gen normal num from prev dir
            dirs.append(round(((dir1+dir2)/2)-360, 2))
            
            speed1 = np.random.normal(speeds[0], 1, 1)[0] #gen normal num from starting speed
            speed2 = np.random.normal(speeds[-1], 1, 1)[0] #gen normal num from prev speed  
            temp_speed = round((speed1+speed2)/2, 2)
            if temp_speed <= 0:
                temp_speed = round(np.random.uniform(low=0.01, high=0.1), 2)
            speeds.append(temp_speed)
############################################################################### 


###############################################################################   
###Functions for building ignitions
def atv_ignition(dom, wind_dir, num_ignitors = 3, line_space_chain = 1, 
                 ig_type='strip', dash_int_chain = 0.5, dot_int_chain = 0.25,
                 ignitors_wait_time = 20, ignition_num_wait_time = 0,
                 ADD_TIME_AFTER_LAST_IG = 1800, SPEED_OF_IGNITION = 1):
    """
    Need to update: only builds lines currently
    """
    shape_paths = dom.shape_paths
    line_space_m = chain2meter(line_space_chain)
    dash_int_m = chain2meter(dash_int_chain)
    dot_int_m = chain2meter(dot_int_chain)
    
    ignition_lines = bs.build_ig_lines(shape_paths, line_space_m, wind_dir=wind_dir)
    ignition_lines = ignition_lines.sort_values('Dist', ascending=True)
    
    if (wind_dir>45 and wind_dir<=135) or (wind_dir>225 and wind_dir<=315):
        ig_dirs = ('N-S','S-N')
    else: ig_dirs = ('E-W','W-E')
    
    ignition_lines['Ig_Num'] = 0
    ignition_lines['ATV_Num'] = 0
    ignition_lines['Add_Time'] = 0
    ignition_lines['Dir'] = ''
    
    for i in range(len(ignition_lines)):
        temp_Ig_Num = int((i/num_ignitors)+1)
        ignition_lines.Ig_Num.iloc[i] = temp_Ig_Num
        
        temp_ATV_Num = int((i%num_ignitors)+1)
        ignition_lines.ATV_Num.iloc[i] =temp_ATV_Num 
        
        if temp_Ig_Num==1 and temp_ATV_Num ==1:
            temp_Add_Time = 0
        elif temp_ATV_Num == 1:
            temp_Add_Time = ignition_num_wait_time
        else:
            temp_Add_Time = ignitors_wait_time
        ignition_lines.Add_Time.iloc[i] = temp_Add_Time
        
        if temp_Ig_Num%2 > 0.5:
            temp_dir = ig_dirs[0]
        else: temp_dir = ig_dirs[1]
        ignition_lines.Dir.iloc[i] = temp_dir
        
    #Save shapefile
    ignition_lines.to_file(os.path.join(shape_paths.SHAPE_PATH, 'ig_lines.shp'))
    if ig_type == 'strip':
        df_ig_points = bs.line_to_points_to_df(dom, ignition_lines, spacing=4)

    elif ig_type == 'dot':
        df_ig_points = bs.line_to_points_to_df(dom, ignition_lines, spacing=dot_int_m)
        
    gen_ig_times(dom, df_ig_points, ADD_TIME_AFTER_LAST_IG, SPEED_OF_IGNITION)

def gen_ig_times(dom, df, ADD_TIME_AFTER_LAST_IG, SPEED_OF_IGNITION):
    """
    Reads in shaplefile of ig location to df and builds ignite.dat
    
    Parameters
    ----------
    QF_PATH : path to QF_RUN
    dom : domain params class   
    df : dataframe with ignition locations 
    SPEED_OF_IGNITION: (m/s)

    Modifies
    -------
    Adds time to df.IgTime
    
    Calls
    -------
    print_ignite_dat(QF_PATH, df):
    """
    QF_PATH = dom.QF_PATH
    strt_time = 1 #strt_time: Track start of atv igniter
    atv_end_times = [] #track when all atvs finish ignitions
    ig_num = np.sort(df.Ig_Num.unique())
    frames=[] #Track new df slices with time column added
    for ig in ig_num:
        ig_df = df[df['Ig_Num']==ig]
        ATV_num = np.sort(ig_df.ATV_Num.unique())
        for atv in ATV_num:            
            atv_df = ig_df[ig_df['ATV_Num']==atv]
            ig_dir = atv_df['Dir'].unique()[0]
            strt_time += atv_df['Add_Time'].unique()[0]
            end_time = int(strt_time + atv_df['Length'].unique()[0]/SPEED_OF_IGNITION)
            atv_end_times.append(end_time)
            time_interval = (end_time-strt_time)/len(atv_df)
            
            #Sort based on ig_dir
            if ig_dir == 'N-S':
                atv_df = atv_df.sort_values('Y', ascending=False)
            elif ig_dir == 'S-N':
                atv_df = atv_df.sort_values('Y', ascending=True)
            elif ig_dir == 'E-W':
                atv_df = atv_df.sort_values('X', ascending=False)
            elif ig_dir == 'W-E':
                atv_df = atv_df.sort_values('X', ascending=True)
            else: 
                print("Don't recognize ignition direction: {}".format(ig_dir))
                print("Check CSV")
                sys.exit(0)
            
            #Loop through rows to specify ignition times
            temp_IgTime = strt_time
            for i, row in atv_df.iterrows():
                atv_df.IgTime.loc[i] = temp_IgTime
                temp_IgTime += time_interval
            
            frames.append(atv_df)
            
            #Update strt_time if starting new ignion
            try:
                if atv == np.max(ATV_num): #Check if at last atv in ignition
                    strt_time = max(atv_end_times) #Mod current time if at the end of Ig_num
                    atv_end_times = [] #Reset
            except: pass #at end of iteration and don't need to calc current time any more
    
    df= pd.concat(frames)
    df.IgTime = df.IgTime.astype(int) #convert ignitions times to intervals
    dom.sim_time = df.IgTime.max() + ADD_TIME_AFTER_LAST_IG
    df = df.sort_values('IgTime', ascending=True) #sort by ignition time before printing
    print_ignite_dat(QF_PATH, df)
    
    return

def print_ignite_dat(QF_PATH, df):
    """
    Reads in shaplefile of ig location to df and builds ignite.dat
    
    Parameters
    ----------
    QF_PATH : path to QF_RUN
    df : dataframe with ignition locations     

    Prints
    -------
    ignite.dat in QF directory
    """
    with open(os.path.join(QF_PATH,'ignite.dat'), 'w') as input_file:
        input_file.write("       igntype=    4\n")
        input_file.write("    &aeriallist\n")
        input_file.write("       naerial=  {}\n".format(len(df)))
        input_file.write("    targettemp= 1000.00\n")
        input_file.write("      ramprate=  172.00\n")
        input_file.write("/\n")
        #for i, row in df.iterrows(): #Might be bad because it doesn't preserve dtype in the series
        #    input_file.write("{}   {}   {}\n".format(row['QF_X_index'], row['QF_Y_index'], row['IgTime']))
        for i in range(len(df)):    
            input_file.write("{}   {}   {}\n".format(df.iloc[i]['QF_X_index'], df.iloc[i]['QF_Y_index'], df.iloc[i]['IgTime']))
    return        
###############################################################################


###############################################################################   
###Functions for building QF_Domain Parameters
def dom_from_burn_plot(shape_paths, buffer=30, QF_PATH='default'):
    try:  
        dom = bs.boundingbox(shape_paths, buffer, QF_PATH)
    except:
        print('[Error] File burn_plot.shp not found. Cannot build input files.')
        sys.exit()
    return dom
###############################################################################


###############################################################################
###Functions for build qf_arrs (Fuel Domains)
def build_ff_domain(dom, FUEL_PATH = 'default', FF_request=True, use_topo=True):
    if FUEL_PATH=='default':
        FUEL_PATH = bs.default_path('FF_Fuel')
    qf_arrs = FF.build_ff_domain(dom, FUEL_PATH, FF_request, use_topo)
    return qf_arrs
###############################################################################


###############################################################################
###Functions for printing QF inputs
def build_qf_run(qf_arrs):
    ttrs_quicfire.print_inp_files.main(qf_arrs)
###############################################################################


###############################################################################
###Misc. helper functions

def chain2meter(val):
    return val*20.1168
###############################################################################