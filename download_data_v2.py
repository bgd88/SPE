#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:59:12 2021

@author: loic
"""
import datetime
import numpy as np
import scipy.signal
import glob, os, sys
from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime, Stream

def MakeDir(nameDir):
    try:
        os.makedirs(nameDir)
    except:
        pass

client = Client("SCEDC")


direc = '/Volumes/Gdrive/SPE/data'
year = 2016
dy = ["%.3d" % i for i in range(92, 93)]



for day in dy:

    t1 = UTCDateTime(str(year) + day + "T000000.0")
    t2 = UTCDateTime(str(year) + day + "T235959.999999")
    inv = client.get_stations(network='SN', station='L3*', level='channel',
                              starttime=t1, endtime=t2)

    print(inv)
    dir1 = direc + os.sep + str(year) + "/Event_" + str(year) + "_" + day
    MakeDir(dir1)

    for K in inv:
        for sta in K:
            for chan in sta:
                fname = dir1 + "/" + str(K.code) + "." + str(sta.code) \
                             + "." + str(chan.code) + '.sac'

                if os.path.exists(fname)==False:
                    try:
                        st = client.get_waveforms(network=K.code,
                                                  station=sta.code,
                                                  channel=chan.code,
                                                  location='*', starttime=t1,
                                                  endtime=t1+24*3600-.005)
                        st.detrend(type='constant')
                        st.detrend(type='linear')
                        st.filter("bandpass", freqmin=0.01, freqmax = 24,
                                  zerophase=True)
                        st.detrend(type='constant')
                        st.detrend(type='linear')
                        if len(st)>=1:
                            st.merge(method=1,fill_value=0)
                        print(st)


                        if st[0].stats.sampling_rate==500:
                            st[0].decimate(5)
                            st[0].decimate(2)
                        elif st[0].stats.sampling_rate==200:
                            st[0].decimate(4)
                        elif st[0].stats.sampling_rate==100:
                            st[0].decimate(2)

                        st.write(fname, format='sac')

                    except:
                        pass
