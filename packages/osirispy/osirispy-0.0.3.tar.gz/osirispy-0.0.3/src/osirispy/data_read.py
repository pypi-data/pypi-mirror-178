import numpy as np
import h5py

class axis:
    def __init__(self,nx,lims,name):
        self._nx=nx
        self._name=name
        self._ax_arr=np.linspace(lims[0],lims[1],nx)
        
    
    @property
    def nx(self):
        return self._nx
    
    @property
    def name(self):
        return self._name
    
    @property
    def ax_arr(self):
        return self._ax_arr
    
class data_2d:
    def __init__(self,fname):
        f=h5py.File(fname,"r")
        #field
        E_rad=np.array(f["E2"]) #charge for density, e2 for OSIRIS fields, e3_x2_slice for slices
        #time axis
        ax2=f["AXIS/AXIS2"]        
        axis2=np.array(ax2)
        ax2name=ax2.attrs["NAME"][0].decode('UTF-8')+" ["+ax2.attrs["UNITS"][0].decode('UTF-8')+"]"

        #spatial axis
        ax1=f["AXIS/AXIS1"]        
        axis1=np.array(ax1)
        ax1name=ax1.attrs["NAME"][0].decode('UTF-8')+" ["+ax1.attrs["UNITS"][0].decode('UTF-8')+"]"
        #timestamp
        
        dataname=f.attrs["NAME"][0].decode('UTF-8')+" ["+f.attrs["UNITS"][0].decode('UTF-8')+"]"
        time_s=f.attrs["TIME"][0]
        f.close()

        self._axis1=axis(len(E_rad),axis1,ax1name)
        self._axis2=axis(len(E_rad[0]),axis2,ax2name)
        self._data=E_rad
        self._name=dataname
        self._time_s=time_s
        
    @property
    def axis1(self):
        return self._axis1

    @property
    def axis2(self):
        return self._axis2

    @property
    def data(self):
        return self._data
    
    @property
    def name(self):
        return self._name
    
    @property
    def data(self):
        return self._data
    