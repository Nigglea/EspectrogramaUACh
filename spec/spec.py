import sys
import librosa.core as lib
import pandas as pd
import Soundlapse.logspec as lgs
from Soundlapse import tools
from Soundlapse import plotting as plt
from Soundlapse import melspec as mel
import numpy as np
import xarray as xr



def create_log(filez,seg=1):
    cont=0
    n_frames=1
    for filepath in filez:
        cont+=1
        seg=1
        sig,fs = lib.load(filepath,sr=44100)
        frames = int(seg*fs)
        frames_len = int(np.around(len(sig)/frames,0))
        if cont==1:
            offset=seg*(n_frames-1)
            frames_sig,fs =  lib.load(filepath,sr=44100,duration=seg,offset=offset)
            (X, Y, d) = lgs.long_spectrogram(frames_sig,fs)
            Ylog  = np.power(10,Y)
            CC = pd.DataFrame(data=d.T,columns=Ylog)
            CC.to_csv('temporal files/data_spec.csv',index=False)
            n_frames = 2
            while n_frames<=frames_len:
                offset=seg*(n_frames-1)
                frames_sig,fs = lib.load(filepath,sr=44100,duration=seg,offset=offset)
                (X, Y, d) = lgs.long_spectrogram(frames_sig,fs)
                DD = pd.DataFrame(data=d.T)
                n_frames += 1
                percent_progress   = (n_frames/float(frames_len) * 100)                                                 # Porcentaje de progreso.
                sys.stdout.write("\rProgreso: "+str(percent_progress)+'%. ')                                # Barra de progreso.
                sys.stdout.flush() 
                DD.to_csv('temporal files/data_spec.csv',mode='a',header=False,index=False)
        if cont>1:
            n_frames=1
            while n_frames<=frames_len:
                offset=seg*(n_frames-1)
                frames_sig,fs = lib.load(filepath,sr=44100,duration=seg,offset=offset)
                (X, Y, d) = lgs.long_spectrogram(frames_sig,fs)
                DD = pd.DataFrame(data=d.T)
                n_frames += 1
                percent_progress   = (n_frames/float(frames_len) * 100)                                                  # Porcentaje de progreso.
                sys.stdout.write("\rProgreso: "+str(percent_progress)+'%. ')                                # Barra de progreso.
                sys.stdout.flush() 
                DD.to_csv('temporal files/data_spec.csv',mode='a',header=False,index=False)
        print('check',cont)
    return X,Ylog

def create_mel(filez,seg=1):
    cont=0
    n_frames=1
    for filepath in filez:
        cont+=1
        seg=1
        sig,fs = lib.load(filepath,sr=44100)
        frames = int(seg*fs)
        frames_len = int(np.around(len(sig)/frames,0))
        if cont==1:
            offset=seg*(n_frames-1)
            frames_sig,fs =  lib.load(filepath,sr=44100,duration=seg,offset=offset)
            (X, Y, d) = mel.spectrogram(frames_sig,fs)
            CC = pd.DataFrame(data=d.T,columns=Y)
            CC.to_csv('temporal files/mel.csv',index=False)
            n_frames = 2
            while n_frames<=frames_len:
                offset=seg*(n_frames-1)
                frames_sig,fs = lib.load(filepath,sr=44100,duration=seg,offset=offset)
                (X, Y, d) = mel.spectrogram(frames_sig,fs)
                DD = pd.DataFrame(data=d.T)
                n_frames += 1
                percent_progress   = (n_frames/float(frames_len) * 100)                                                 # Porcentaje de progreso.
                sys.stdout.write("\rProgreso: "+str(percent_progress)+'%. ')                                # Barra de progreso.
                sys.stdout.flush() 
                DD.to_csv('temporal files/mel.csv',mode='a',header=False,index=False)
        if cont>1:
            n_frames=1
            while n_frames<=frames_len:
                offset=seg*(n_frames-1)
                frames_sig,fs = lib.load(filepath,sr=44100,duration=seg,offset=offset)
                (X, Y, d) = mel.spectrogram(frames_sig,fs)
                DD = pd.DataFrame(data=d.T)
                n_frames += 1
                percent_progress   = (n_frames/float(frames_len) * 100)                                                  # Porcentaje de progreso.
                sys.stdout.write("\rProgreso: "+str(percent_progress)+'%. ')                                # Barra de progreso.
                sys.stdout.flush() 
                DD.to_csv('temporal files/mel.csv',mode='a',header=False,index=False)
        print('check',cont)
    return X,Y