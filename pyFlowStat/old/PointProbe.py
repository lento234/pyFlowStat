'''
PointProbe.py

Collection of tools/functions to load and/or get spectral analysis of time series extracted from
a turbulent flow field.

functions included:
    readOfRuntime(probeLoc,ofFile,rtnType='numpy')
    genPtStat(probeName,probeLoc,tserie,Userie)
'''


#===========================================================================#
# load modules
#===========================================================================#
#standard modules
import sys
import re
import os
import csv
import collections


#scientific modules
import numpy as np
import scipy as sp
from scipy import signal
from scipy.optimize import curve_fit
# special modules

#from pyFlowStat.TurbulenceTools import TurbulenceTools as tt
import pyFlowStat.old.TurbulenceTools as tt
import pyFlowStat.old.Surface as Surface

class PointProbe(object):
    '''
    PointProbe Class

    A class to handle velocity time serie from a point.
    '''

    def __init__(self):
        self.probeLoc=[]
        self.probeTimes=[]
        self.probeVar=[]
        self.data=dict()
        return

    #===========================================================================#
    # functions
    #===========================================================================#
    def t(self):
        return self.data['t']
    def Ux(self):
        return self.data['U'][:,0]
    def Uy(self):
        return self.data['U'][:,1]
    def Uz(self):
        return self.data['U'][:,2]
    def Umag(self):
        return self.data['Umag']
    def ux(self):
        return self.UPrime()[:,0]
    def uy(self):
        return self.UPrime()[:,1]
    def uz(self):
        return self.UPrime()[:,2]
    def Umean(self):
        return np.mean(self.Umag())

    def UPrime(self):
        if 'UPrime' in self.data:
            return self.data['UPrime']
        else:
            return self.data['U']-self.data['UMean']

    def uu_bar(self):
        return np.mean(pow(signal.detrend(self.ux()),2))
    def vv_bar(self):
        return np.mean(pow(signal.detrend(self.uy()),2))
    def ww_bar(self):
        return np.mean(pow(signal.detrend(self.uz()),2))
    def uv_bar(self):
        return np.mean(signal.detrend(self.ux())*signal.detrend(self.uy()))
    def uw_bar(self):
        return np.mean(signal.detrend(self.ux())*signal.detrend(self.uz()))
    def vw_bar(self):
        return np.mean(signal.detrend(self.uy())*signal.detrend(self.uz()))
    def TKE_bar(self):
        return 0.5*(self.uu_bar()+self.vv_bar()+self.ww_bar())

    def Reij(self,store=True):
        '''
        Calculate and return the Reynolds stress tensor Reij defined as
            Reij = {ui*uj}
        with ui the velocity fluctuation from the Reynolds decomposition and {.} the averaging operator.

        Arguments:
            * store:  [bool] Stroe Reij in self.data. Default=True

        Returns:
            * Reij:  [numpy.array with Reij.shape=(3,3)] Reynolds stress tensor R.
        '''
        Reij = np.zeros([3,3])
        Reij[0,0] = self.uu_bar()
        Reij[0,1] = self.uv_bar()
        Reij[0,2] = self.uw_bar()
        Reij[1,0] = self.uv_bar()
        Reij[1,1] = self.vv_bar()
        Reij[1,2] = self.vw_bar()
        Reij[2,0] = self.uw_bar()
        Reij[2,1] = self.vw_bar()
        Reij[2,2] = self.ww_bar()

        if store==True:
            self.data['Reij'] = Reij

        return Reij


    def __iter__(self):
        '''
        '''
        return self.data.itervalues()

    def __getitem__(self, key):
        '''
        '''
        return self.data[key]

    def __setitem__(self, key, item):
        '''
        '''
        self.data[key] = item

    def copy(self):
        pp=PointProbe()
        pp.probeLoc=np.copy(self.probeLoc)
        pp.probeTimes=np.copy(self.probeTimes)
        pp.probeVar=np.copy(self.probeVar)
        pp.data=self.data.copy()
        return pp

    def readFromOpenFoam(self,probeLoc,filepath):
        '''
        Read runtime post-processing probe generated by the OpenFOAM.
        It updates member variables probeVar and probeTimes, then creates a data
        dictionnary. See member function createDataDict for more information about
        data dict.

        Arguments:
            * probeLoc:   [numpy.array or python list. shape=()] Coordinate of probe (must be included in ofFile)
            * filepath:   [string] Path to OpenFOAM probe file

        Returns:
            None
        '''
        probeTimes = []
        probeVar = []
        # read file
        crs = open(filepath, 'r')
        lineno = 0
        for line in crs:
            # This regex finds all numbers in a given string.
            # It can find floats and integers writen in normal mode (10000) or with power of 10 (10e3).
            match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
            #print(match)
            if lineno==0:
                allXs = match
            if lineno==1:
                allYs = match
            if lineno==2:
                allZs = match
                ptFound = False
                for i in range(len(allXs)):
                    if (float(allXs[i])==probeLoc[0] and float(allYs[i])==probeLoc[1] and float(allZs[i])==probeLoc[2]):
                        ptPos = i
                        ptFound = True
                if ptFound==True:
                    #print('Probe found!')
                    pass
                else:
                    print('Probe not found!')
                    break
            if lineno>3 and len(match)>0:
                if lineno==4:
                    varSize = int((len(match)-1)/(len(allXs)))  #check if probe var is scalar, vec or tensor
                    srtindex = 1+ptPos*varSize
                    endindex = srtindex+varSize
                probeTimes.append(float(match[0]))
                #probeTimes.append(float(match[0]))
                probeVar.append([float(var) for var in match[srtindex:endindex]])
            else:
                pass
            lineno = lineno+1
        crs.close()
        self.probeLoc = probeLoc
        self.probeTimes = np.array(probeTimes)
        self.probeVar = np.array(probeVar)

        # run fill data (dictionnary) depending on probeVarType()
        self.createDataDict(action=True)

    def readFromLDA(self,probeLoc,filepath):
        '''
        Read LDA file.
        It updates member variables probeVar and probeTimes, then creates a data
        dictionnary. See member function createDataDict for more information about
        data dict.

        Arguments:
            probeLoc: [numpy.array or python list. shape=(3)] Coordinate of probe (must be included in ofFile)
            filepath: [string] Path to OpenFOAM probe file

        Returns:
            None
        '''
        probeVar = []
        probeTimes = []

        crs = open(filepath, 'r')
        lineno = 0
        for line in crs:
            if lineno>=5:
                data=line.split()
                probeTimes.append(float(data[0])/1000.0)
                probeVar.append([float(data[2]),0,0])
            lineno = lineno+1
        crs.close()
        self.probeLoc=probeLoc
        self.probeVar=np.array(probeVar)
        self.probeTimes=np.array(probeTimes)
        self.createDataDict()

    def probeVarType(self):
        '''
        '''
        if self.probeVar[0].shape==():
            return 'scalar'
        elif self.probeVar[0].shape==(3,):
            return 'vector'
        elif self.probeVar[0].shape==(3,3):
            return 'tensor'


    def createDataDict(self,action=True):
        '''
        Create the correct data dict depending on probeVarType.
        '''

        if action==True:
            if self.probeVarType()=='scalar':
                self.createScalarDict()
            elif self.probeVarType()=='vector':
                self.createVectorDict()
            elif self.probeVarType()=='tensor':
                self.createTensorDict()
        else:
            pass


    def appendData(self,var,t=None,createDict=True):
        '''
        Append var to probeVar and t to probeTime. If t=None, probeTime is
        simply extended according probeTime. var can be of any dimension
        (scalar, vector, tensor, etc...)

        Low level method. The followings cases are not checked:
            * gap: gap between var and probeVar
            * overlap: overlap between var and probeVar. Cut var, or probeVar to solve such issues
            * fequency missmatch: sampling frequency between var and probeVar] must be identical

        Arguments:
            * var: [np.array. shape=(N) for scalar or shape=(N,i) for higher dimensions] variable to append
            * t: [np.array. shape=N]  time value. Default=None
            * createDict: [bool] run createDataDict after execution of appendData. Default=True
        '''

        # append var to probeVar
        if self.probeVarType()=='scalar':
            self.probeVar = np.hstack((self.probeVar,var))
        elif self.probeVarType()=='vector' or self.probeVarType()=='tensor':
            self.probeVar = np.vstack((self.probeVar,var))

        # append t to probeTimes
        if t!=None:
            self.probeTimes = np.hstack((self.probeTimes,t))
        else:
            # complet self['t'] according total length of self['U']
            t0 = self.probeTimes[0]
            t1 = self.probeTimes[1]
            frq = 1/(t1-t0)
            iterable = (t0+(1/frq)*i for i in range(self.probeVar.shape[0]))
            self.probeTimes = np.fromiter(iterable, np.float)

        self.createDataDict(action=createDict)


    def appendProbe(self,probe,rmOverlap='none',createDict=True):
        '''
        Append "probe" (PointProbe object) to current data.
        The following known issues are not checked:
            * gap: gap between U and self['U']
            * overlap: overlap between U and self['U']. Use method "cutData" to solve such issues
            * fequency missmatch: sampling frequency between U and self['U'] must be identical
            * location: append datas should (must?) come from the same probe location

        Arguments:
            * probe: [PointProbe object] PointProbe object to append
            * rmOverlap: ['none','self','probe'] In case of overlaping data, which side should be kept
              in the overlaping section?
                  * 'none': data are simply added without any check (default)
                  * 'self': data from self are removed
                  * 'probe': data from probe are removed
              If there is non overlap, or a gap, 'none' is used.
            * createDict: [bool] run method createDataDict or createScalarDict
              (dependion on the dimension of probeVar )after execution of appendData. Default=True
        '''
        if rmOverlap=='none':  # do nothing on newU and use appendData
            self.appendData(probe.probeVar,probe.probeTimes,createDict=False)
        elif rmOverlap=='probe':    #chop "probe"
            index = 0
            while probe.probeTimes[index]<self.probeTimes[-1]:
                index = index+1
            indices = np.arange(index+1,probe.probeTimes.shape[0])
            self.appendData(probe.probeVar[indices,:],probe.probeTimes[indices],createDict=False)
        elif rmOverlap=='self':       #chop "self"
            backwardindex = -1
            while self.probeTimes[backwardindex]> probe.probeTimes[0]:
                backwardindex = backwardindex-1
            maxindex = self.probeTimes.shape[0]+backwardindex
            self.cutData(np.arange(0,maxindex),createDict=False)
            self.appendData(probe.probeVar,probe.probeTimes,createDict=False)

        self.createDataDict(action=createDict)


    def cutData(self,indices,createDict=True):
        '''
        Cut data according indices.

        Arguments:
            * indices: [np.array of python list] list of int
            * createDict: [bool] run method createDataDict or createScalarDict
              (dependion on the dimension of probeVar )after execution of cutData. Default=True

        Example (assume pt as a PointProbe object):
            >>> pt['U'].shape
            [10000,3]
            >>>pt.cutData([3,4,5,6,7]) # data from index 3 to 7
            >>>pt.cutData(np.arange(10,1000))  # data from index 10 to 1000
            >>>pt.cutData(np.arange(10,1000,5))  # data from index 10 to 1000 but only every 5 indices
        '''
        self.probeTimes=self.probeTimes[np.array(indices)]

        if self.probeVarType()=='scalar':
            self.probeVar=self.probeVar[np.array(indices)]
        elif self.probeVarType()!='scalar':
            self.probeVar=self.probeVar[np.array(indices),:]

        self.createDataDict(action=createDict)


    def createVectorDict(self):
        '''
        Creates the "data" dictionnary from member variable probeLoc,
        probeTimes and probeVar. Use it only if probeVar is a vector.

        Member variable data (python ditionary) is created. It holds all the series
        which can be generate with a time resolved vector field.
        To add a new entry to data, type somthing like:
        pt.PointProbe()
        pt.readFromLDA(point,file)
        pt['myNewKey'] = myWiredNewEntry

        By default, the following keys are included in data:
            pos:   [numpy.array. shape=(3)] Probe location
            frq:   [float] Sample frequence
            U:     [numpy.array. shape=(N,3)] Vector variable U
            t:     [numpy.array. shape=(N)]   Time t
            UMean: [numpy.array. shape=(3)] Mean of U
            UStd:  [numpy.array. shape=(3)] Standard devation of U
        '''

        self.data = dict()
        self.data['pos'] = self.probeLoc
        # velocity and time
        self.data['U'] = self.probeVar
        self.data['t'] = self.probeTimes

        # timestep, sample frequence
        self.data['dt']=self.data['t'][1]-self.data['t'][0]
        self.data['frq'] = 1/self.data['dt']

        self.data['UMean'] = np.mean(self.data['U'],axis=0)
        self.data['UStd'] = np.std(self.data['U'],axis=0)

    def addVectorMagnitude(self):
        '''
        adds 'Umag' key to dict
        '''
        #Umag
        self.data['Umag'] = np.linalg.norm(self.data['U'], axis=1)

    def addFluctuations(self):
        '''
        adds 'UPrime' key to dict
        '''
        self.data['UPrime']=self.data['U']-self.data['UMean']

    def createScalarDict(self):
        '''
        Creates the "data" dictionnary from member variable probeLoc, probeTimes and probeVar

        Member variable data (python ditionary) is created. It holds all the series
        which can be generate with the probeTimes and probeVar.
        To add a new entry to data, type somthing like:
        pt.PointProbe()
        pt.readFromLDA(point,file)
        pt['myNewKey'] = myWiredNewEntry

        By default, the following keys are included in data:
            pos:  [numpy.array. shape=(3)] Probe location
            frq:  [float] Sample frequence
            S:    [numpy.array. shape=(N)] Scalar S
            t:    [numpy.array. shape=(N)] Time t
            s:    [numpy.array. shape=(N)] Scalar fluctuation u
            Soo:  [numpy.array. shape=(N)] Scalar mean with infinit window size
        '''

        self.data = dict()
        self.data['pos'] = self.probeLoc
        # velocity and time
        self.data['S'] = self.probeVar
        self.data['t'] = self.probeTimes

        # timestep, sample frequence
        self.data['dt']=self.data['t'][1]-self.data['t'][0]
        self.data['frq'] = 1/self.data['dt']

        #mean
        Soo = np.zeros((self.data['S'].shape))
        Soo = np.mean(self.data['S'])
        self.data['Soo'] = Soo
        # fluctuation
        self.data['s'] = self.data['S']-self.data['Soo']


    def createTensorDict(self):
        '''
        Creates the "data" dictionnary from member variable probeLoc, probeTimes and probeVar

        Member variable data (python ditionary) is created. It holds all the series
        which can be generate with the t and M. To add a new entry to data,
        type somthing like:
        pt.PointProbe()
        pt.readFromLDA(point,file)
        pt['myNewKey'] = myWiredNewEntry

        notes:
            The tensor is defined with 'M' (for Matrix) instead of 'T' (for Tensor).

        By default, the following keys are included in data:
            pos:  [numpy.array. shape=(3)] Probe location
            frq:  [float] Sample frequence
            M:    [numpy.array. shape=(N,3,3)] Tensor M
            t:    [numpy.array. shape=(N)]     Time t
            m:    [numpy.array. shape=(N,3,3)] Tensor fluctuation m
            Moo:  [numpy.array. shape=(N,3,3)] Tensor mean with infinit window size
        '''

        self.data = dict()
        self.data['pos'] = self.probeLoc
        # velocity and time
        self.data['M'] = self.probeVar      #M for matrix. T is for temperature and t is for time
        self.data['t'] = self.probeTimes

        # timestep, sample frequence
        self.data['dt']=self.data['t'][1]-self.data['t'][0]
        self.data['frq'] = 1/self.data['dt']

        #mean
        Soo = np.zeros((self.data['M'].shape))
        Soo = np.mean(self.data['M'])
        self.data['Moo'] = Soo
        # fluctuation
        self.data['m'] = self.data['M']-self.data['Moo']  #m for the fluctuating part of M


    def generateStatistics(self,doDetrend=True):
        '''
        Generates statistics and populates member variable data.

        Nots:
            * This method makes sense only with a PointProbe object, which
              holds a time resolved velocity serie.

        Arguments:
            doDetrend: detrend data bevor sigbal processing

        Populates the "data" python dict with with the following keys:
            rii:    [numpy.array of shape=(?)] Auto-correlation coefficent rii. For i=1,2,3
            taurii: [numpy.array of shape=(?)] Time lags for rii. For i=1,2,3
            Rii:    [numpy.array of shape=(?)] Auto-correlation Rii. For i=1,2,3
            tauRii: [numpy.array of shape=(?)] Time lags for Rii. For i=1,2,3


        '''

        self.generateCorrelations(doDetrend=doDetrend)
        self.generateSpectra(doDetrend=doDetrend)



    def generateCorrelations(self,doDetrend=True):
        # auto correlation corefficient of u
        if doDetrend:
            ux=signal.detrend(self.ux());
            uy=signal.detrend(self.uy());
            uz=signal.detrend(self.uz());
            umag=signal.detrend(self.Umag());
        else:
            ux=self.ux();
            uy=self.uy();
            uz=self.uz();
            umag=self.Umag();
        #ux=ux[-samples:-1]
        #uy=uy[-samples:-1]
        #uz=uz[-samples:-1]
        self.data['r11'],self.data['taur11'] = tt.xcorr_fft(ux, maxlags=None, norm='coeff')
        self.data['r22'],self.data['taur22'] = tt.xcorr_fft(uy, maxlags=None, norm='coeff')
        self.data['r33'],self.data['taur33'] = tt.xcorr_fft(uz, maxlags=None, norm='coeff')
        self.data['r12'],self.data['taur12'] = tt.xcorr_fft(ux,y=uy, maxlags=None, norm='coeff')
        self.data['r13'],self.data['taur13'] = tt.xcorr_fft(ux,y=uz, maxlags=None, norm='coeff')
        self.data['r23'],self.data['taur23'] = tt.xcorr_fft(uy,y=uz, maxlags=None, norm='coeff')
        self.data['rmag'],self.data['taurmag'] = tt.xcorr_fft(umag, maxlags=None, norm='coeff')
        # auto correlation of u
        self.data['R11'],self.data['tauR11'] = tt.xcorr_fft(ux, maxlags=None, norm='biased')
        self.data['R22'],self.data['tauR22'] = tt.xcorr_fft(uy, maxlags=None, norm='biased')
        self.data['R33'],self.data['tauR33'] = tt.xcorr_fft(uz, maxlags=None, norm='biased')

    def generateAutoCorrelations(self,doDetrend=True):
        # auto correlation corefficient of u
        if doDetrend:
            ux=signal.detrend(self.ux());
            uy=signal.detrend(self.uy());
            uz=signal.detrend(self.uz());
        else:
            ux=self.ux();
            uy=self.uy();
            uz=self.uz();

        self.data['r11'],self.data['taur11'] = tt.xcorr_fft(ux, maxlags=None, norm='coeff')
        self.data['r22'],self.data['taur22'] = tt.xcorr_fft(uy, maxlags=None, norm='coeff')
        self.data['r33'],self.data['taur33'] = tt.xcorr_fft(uz, maxlags=None, norm='coeff')

    def generateSpectra(self,doDetrend=True):
        '''
        uifrq:  [numpy.array of shape=(?)] u1 in frequency domain. For i=1,2,3
        uiamp:  [numpy.array of shape=(?)] amplitude of u1 in frequency domain. For i=1,2,3
        Seiifrq:[numpy.array of shape=(?)] Frequencies for energy spectrum Seii. For i=1,2,3
        Seii:   [numpy.array of shape=(?)] Energy spectrum Seii derived from Rii. For i=1,2,3
        '''
        if doDetrend:
            ux=signal.detrend(self.ux());
            uy=signal.detrend(self.uy());
            uz=signal.detrend(self.uz());
        else:
            ux=self.ux();
            uy=self.uy();
            uz=self.uz();
        #u in frequency domain
        self.data['u1frq'],self.data['u1amp'] = tt.dofft(sig=ux,samplefrq=self.data['frq'])
        self.data['u2frq'],self.data['u2amp'] = tt.dofft(sig=uy,samplefrq=self.data['frq'])
        self.data['u3frq'],self.data['u3amp'] = tt.dofft(sig=uz,samplefrq=self.data['frq'])
        #Time energy sectrum Se11 (mean: Rii in frequency domain...)
        self.data['Se11frq'],self.data['Se11'] = tt.dofft(sig=self.data['R11'],samplefrq=self.data['frq'])
        self.data['Se22frq'],self.data['Se22'] = tt.dofft(sig=self.data['R22'],samplefrq=self.data['frq'])
        self.data['Se33frq'],self.data['Se33'] = tt.dofft(sig=self.data['R33'],samplefrq=self.data['frq'])

    def generateDiagnosticStatistics(self):
        '''
        Generate diagnostic statistics. Add following entries to the data
        dictionary:
            * Uoo_c: Cumulative velocity average

        Arguments:
            * none

        Returns:
            * none


        '''
        N = self.probeTimes.shape[0]
        div = np.linspace(1,N,N)
        div = np.asarray(div,dtype=int)
        self.data['UMean_c'] = np.cumsum(self.probeVar,axis=0)
        for i in range(3):
            self.data['UMean_c'][:,i] = self.data['UMean_c'][:,i]/div


    def lengthScale(self):
        '''
        Compute turbulent length scale Lii  and time scale Tii.

        Arguments:
            No arguments

        Returns:
            This methods create the following entries in data:

            *T*: python float.
            Turbulent time scale T calculated with the auto-correlation of umag

            *L*: python float
             TUrbulent length scale L caluculated using T.

            *Tij*: python float. i and j can be x, y or z.
             Turbulent Time scale Tij.

            *Lii*: python float. i can be x, y or z
             Turbulent Length scale calulated with the turbulent time scale Tii
             and the "Taylor Frozen Turbulence" theory. Umean[i] is used as
             convective velocity.
        '''

        #def func_gauss(x, a):
        #    np.seterr('ignore')
        #   res = np.exp(-(x*x)/(a*a))
        #   print res

        def checkAutoCorr(xdata,ydata,threshold=0.1):
            '''
            Check shape of the first 3 points. A low value indicates possible
            bad data. A ratio of one means a straigh line.
            Arguments:
                * xdata = lags
                * ydata = correlation

            Returns:
                * True if higher than threshold ratio (good correlation)
            '''
            ratio1=(ydata[1]-ydata[2])/(ydata[0]-ydata[1])
            #ratio2=1/(ydata[1]-ydata[2])*(ydata[2]-ydata[3])

            if ratio1<threshold:
                return False #bad correlation
            else:
                return True

        def doAutoCorr(xkey,ykey,Tkey,Lkey=None,threshold=0.1):
            xdata=self.data[xkey]
            ydata=self.data[ykey]

            if checkAutoCorr(xdata,ydata,threshold=threshold):
                try:
                    popt, pcov = tt.fit_exp_correlation(xdata,ydata)
                    #self.data['Txx']=abs(popt[0])*np.sqrt(np.pi)*0.5*self.data['dt']
                    self.data[Tkey]=popt*self.data['dt']
                    if Lkey:
                        self.data[Lkey]=self.data[Tkey]*np.mean(self.Umag())
                except RuntimeError:
                    print("Error - curve_fit failed")
                    self.data[Tkey]=0
                    if Lkey:
                        self.data[Lkey]=0
            else:
                self.data[Tkey]=0
                if Lkey:
                    self.data[Lkey]=0

        corr_keys=['taur11','taur22','taur33','r11','r22','r33']
        if len(set(corr_keys) & set(self.data.keys()))!=len(corr_keys):
            self.generateCorrelations()
            print "Generating Missing Correleation Statistics"

        threshold=0.1


        doAutoCorr('taur11','r11','Txx','Lxx',threshold=threshold)
        doAutoCorr('taur22','r22','Tyy','Lyy',threshold=threshold)
        doAutoCorr('taur33','r33','Tzz','Lzz',threshold=threshold)

        doAutoCorr('taur12','r12','Txy',threshold=threshold)
        doAutoCorr('taur13','r13','Txz',threshold=threshold)

        doAutoCorr('taur23','r23','Tyz',threshold=threshold)

        doAutoCorr('taurmag','rmag','T','L',threshold=threshold)


    def detrend_periodic(self):
        def func_sin_u(Umean):
            f=Umean/2.0;
            def func_sin(x, a, b):
                return a*np.sin(2*np.pi*f*x+b)
            return func_sin

        def plot_sin(x, a, b,Umean):
            f=Umean/2.0;
            return a*np.sin(2*np.pi*f*x+b)

        xdata=self.t()
        Umean=self.Umean()
        self.data['u'][:,0]=signal.detrend(self.data['u'][:,0])
        ydata=self.ux()
        popt, pcov = curve_fit(func_sin_u(Umean),xdata,ydata)
        self.data['ux_old']=self.data['u'][:,0]
        self.data['ux_sin']=plot_sin(xdata,popt[0],popt[1],Umean)
        self.data['u'][:,0]=self.data['u'][:,0]-plot_sin(xdata,popt[0],popt[1],Umean)

    def detrend_sin(self):

        def func_sin(x, a, b, f):
                    return a*np.sin(2*np.pi*f*x+b)

        xdata=self.t()
        Umean=self.Umean()
        self.data['u'][:,0]=signal.detrend(self.data['u'][:,0])
        ydata=self.ux()
        popt, pcov = curve_fit(func_sin,xdata,ydata)
        self.data['ux_old']=np.copy(self.data['u'][:,0])
        self.data['ux_sin']=func_sin(xdata,popt[0],popt[1],popt[2])
        self.data['u'][:,0]=self.data['u'][:,0]-func_sin(xdata,popt[0],popt[1],popt[2])

def getDataPoints(filepath):
    '''
    Get a list of all the points included in a probe file "probeFile" generated by the OpenFOAM sample tool

    Arguments:
        * filepath: [str()] path to file "probeFile"

    Returns:
        * pointlist: [list(), shape=(N,3)] list of points (let's say N points) included in "probeFile"
    '''
    f = open(filepath, 'r')
    xlist=[]
    ylist=[]
    zlist=[]
    lineno=0
    for line in f:
        # This regex finds all numbers in a given string.
        # It can find floats and integers writen in normal mode (10000) or with power of 10 (10e3).
        match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
        #print(match)
        if lineno==0:
            xlist = match
        if lineno==1:
            ylist = match
        if lineno==2:
           zlist = match
           break
        lineno+=1
    f.close()
    pointlist = np.zeros(shape=(len(xlist),3))
    pointlist[:,0]=xlist
    pointlist[:,1]=ylist
    pointlist[:,2]=zlist

    return pointlist


def getOFPointProbeList(filename,reshape=True,createDict=True):
    '''
    Read OpenFOAM probe file. Ideally, the points in the file should form a line.
    Any kind of probe can be read: scalar, vector, symmetric tensor and tensor.


    Arguments:
        * filename: [string] path to a probe file generate by OpenFOAM.
        * reshape: [bool] rearange tensor and sym tensor in a 3x3 matrix. Default=True.
        * createDict: [bool] run method createDataDict or createScalarDict. Default=True.
          (dependion on the dimension of probeVar )after execution of appendData. Default=True.

    Returns
        * pts: [list] list of PointProbe object
    '''
    def getLongVar(match):
        return match[1+i*varLength:(varLength+1)+i*varLength]

    pointlist=getDataPoints(filename)
    pts=[PointProbe()]*len(pointlist)

    for i in range(0,len(pointlist)):
        pts[i]=PointProbe()
        pts[i].probeLoc=pointlist[i]

    # read file
    crs = open(filename, 'r')
    lineno = 0
    varLength = 0
    nbPts = 0
    for line in crs:
        # This regex finds all numbers in a given string.
        # It can find floats and integers writen in normal mode (10000) or with power of 10 (10e3).
        match = np.array(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))
        match=match.astype(np.float)
        if lineno==0:
            nbPts = match.shape[0]

        if lineno>3 and len(match)>0:
            # get variable dimension: scalar, vector, symetric tensor (upper triangle 3*3), tensor (3*3)
            #   if varLength==1: scalar
            #   if varLength==3: vector
            #   if varLength==6: symtensor
            #   if varLength==9: tensor
            if lineno==4:
                varLength = int((len(match)-1)/nbPts)

            for i in range(0,len(pointlist)):
                var = []
                pts[i].probeTimes.append(match[0])
                # read the variable values for PointProbe i
                if varLength==1:
                    var = match[1+i]
                elif varLength==3:
                    var = getLongVar(match)
                elif varLength>3 and reshape==False:
                    var = getLongVar(match)
                elif varLength==9 and reshape==True:
                    var = getLongVar(match).reshape(3,3)
                elif varLength==6 and reshape==True:
                    varVec = getLongVar(match)
                    var = np.array([[varVec[0], varVec[1], varVec[2]],
                                    [varVec[1], varVec[3], varVec[4]],
                                    [varVec[2], varVec[4], varVec[5]]])

                pts[i].probeVar.append(var)

        else:
            pass
        lineno = lineno+1
    crs.close()

    for i in range(0,len(pointlist)):
        pts[i].probeTimes = np.array(pts[i].probeTimes)
        pts[i].probeVar = np.array(pts[i].probeVar)
        pts[i].createDataDict(action=createDict)

    return pts


def getVectorPointProbeList(filename):
    '''
    Arguments:
        * filename: [string] path to file which contains all the points of the line.
          filename is normally generate by the OpenFOAM sample tool for probes. No
          check if the file exist.

    Returns
        * pts: [list] list of PointProbe object
    '''
    pointlist=getDataPoints(filename)
    pts=[PointProbe()]*len(pointlist)

    for i in range(0,len(pointlist)):
        pts[i]=PointProbe()
        pts[i].probeLoc=pointlist[i]

    # read file
    crs = open(filename, 'r')
    lineno = 0
    for line in crs:
        # This regex finds all numbers in a given string.
        # It can find floats and integers writen in normal mode (10000) or with power of 10 (10e3).
        match = np.array(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))
        match=match.astype(np.float)
        #print(match)

        if lineno>3 and len(match)>0:
            for i in range(0,len(pointlist)):
                pts[i].probeTimes.append(match[0])
                pts[i].probeVar.append(match[1+i*3:4+i*3])
        else:
            pass
        lineno = lineno+1
    crs.close()

    for i in range(0,len(pointlist)):
        pts[i].probeTimes = np.array(pts[i].probeTimes)
        pts[i].probeVar = np.array(pts[i].probeVar)
        pts[i].createDataDict()

    return pts

def getScalarPointProbeList(filename):
    '''
    Arguments:
        * filename: [string] path to file which contains all the points of the line.
        filename is normally generate by the OpenFOAM sample tool for probes.
    Returns
        * pts: [list] list of PointProbe object
    '''
    pointlist=getDataPoints(filename)
    pts=[PointProbe()]*len(pointlist)

    for i in range(0,len(pointlist)):
        pts[i]=PointProbe()
        pts[i].probeLoc=pointlist[i]

    # read file
    crs = open(filename, 'r')
    lineno = 0
    for line in crs:
        # This regex finds all numbers in a given string.
        # It can find floats and integers writen in normal mode (10000) or with power of 10 (10e3).
        match = np.array(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))
        match=match.astype(np.float)

        if lineno>3 and len(match)>0:
            for i in range(0,len(pointlist)):
                pts[i].probeTimes.append(match[0])
                pts[i].probeVar.append(match[1+i])
        else:
            pass
        lineno = lineno+1
    crs.close()

    for i in range(0,len(pointlist)):
        pts[i].probeTimes = np.array(pts[i].probeTimes)
        pts[i].probeVar = np.array(pts[i].probeVar)
        pts[i].createScalarDict()

    return pts

def getPIVVectorPointProbeList(directory,pointlist,nr,frq):
    filelist=Surface.getVC7filelist(directory,nr)

    pts=[PointProbe()]*len(pointlist)

    for i in range(0,len(pointlist)):
        pts[i]=PointProbe()
        pts[i].probeLoc=pointlist[i,:]

    # read file

    for i,pivfile in enumerate(filelist):
        print("reading " + pivfile)
        tempS=Surface.Surface()
        tempS.readFromVC7(os.path.join(directory,pivfile))

        for j,pt in enumerate(pts):
            pt.probeTimes.append(i*1.0/frq)
            #print pt.probeTimes

            #print [tempS.vx[pt.probeLoc[0],pt.probeLoc[1]],tempS.vy[pt.probeLoc[0],pt.probeLoc[1]],tempS.vz[pt.probeLoc[0],pt.probeLoc[1]]]
            vx=tempS.vx[pt.probeLoc[1],pt.probeLoc[0]]
            vy=tempS.vy[pt.probeLoc[1],pt.probeLoc[0]]
            vz=tempS.vz[pt.probeLoc[1],pt.probeLoc[0]]
            if np.isnan(vx):
                vx=0
            if np.isnan(vy):
                vy=0
            if np.isnan(vz):
                vz=0
            pt.probeVar.append([vx,vy,vz])

    for i in range(0,len(pointlist)):
        pts[i].probeTimes = np.array(pts[i].probeTimes)
        pts[i].probeVar = np.array(pts[i].probeVar)
        pts[i].createDataDict()

    return pts


def readcsv(csvfile,delimiter,fieldnames=None):
    '''
    Read a csv file with headers on the first line. If no headers, a list of
    headers must be specified with fieldnames. csv files are  very common data
    file for scientists. This method might become quickly limited, for special
    cases, see standard python module "csv":
    http://docs.python.org/2/library/csv.html

    Arguments:
        *csvfile*: python string.
         Path to the CVS file. It can be absolute or relative.

        *delimiter*: python string.
         Delimiter use in the csv file. For tabs, use '\t'. For semicolon, use
         ';'. For comma, use ','.

        *fieldnames*: python list of strings.
         list of header if any in the csv file.

    Returns:
        *data*: python collection.defaultdict.
         Advenced python dict with headers as dict keys.

    Examples:
        >>> data = readcsv(data.csv,delimiter=';')   #cvs with header and ';' as delimiter
        >>> data = readcsv(data.csv,delimiter='\t', fieldnames=['x','y','U'])   #cvs without header and a tab as delimiter
        >>> listOfHeaders = data.keys()
        >>> dataForHeaderA = data['A']
    '''
    data = collections.defaultdict(list)
    with open(csvfile) as f:
        reader = csv.DictReader(f,delimiter=delimiter,fieldnames=fieldnames)
        #headers = reader.fieldnames
        for row in reader:
            for (k,v) in row.items():
                data[k].append(float(v))
    return data