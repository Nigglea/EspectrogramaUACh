import cv2
import numpy as np
import scipy.signal as sc
from Soundlapse import funcionestimelapse as tl
from Soundlapse import logspec as log
from Soundlapse import file 
import soundfile as audio


def freq_ticks(scale='1/3 octave'):
    third_octave   = [16,20,25,31.5,40,50,63,80,100,125,
                    160,200,250,315,400,500,630,800,1000,1250,
                    1600,2000,2500,3150,4000,5000,6300,8000,10000,
                    12250,16000,20000]
    octave         = [16,31.5,63,125,250,500,1000,2000,4000,8000,16000]
    half_octave    = [16,22.4,31.5,45,63,90,125,180,250,355,
                    500,710,1000,1400,2000,2800,4000,5600,8000,11200,
                    16000]
    audacity       = [20,30,40,60,80,100,160,200,300,400,
                    600,800,1000,1300,1600,2000,3000,4000,6000,8000,
                    10000,14000,19000]  
    audacity_short = [30,60,100,190,300,600,1000,1900,3000,6000,10000,
                    19000]
    if scale == '1/3 octave':
        Freq_Ticks = [(third_octave[int(i)],third_octave[int(i)] )for i in range(len(third_octave))]
    if scale == 'octave':
        Freq_Ticks = [(octave[int(i)],octave[int(i)]) for i in range(len(octave))]  
    if scale == '1/2 octave':
        Freq_Ticks = [(half_octave[int(i)],half_octave[int(i)] )for i in range(len(half_octave))]
    if scale == 'audacity':
        Freq_Ticks = [(audacity[int(i)],audacity[int(i)] )for i in range(len(audacity))]
    if scale == 'audacity short':
        Freq_Ticks = [(audacity_short[int(i)],audacity_short[int(i)]) for i in range(len(audacity_short))]
    return Freq_Ticks

def time_ticks(dB,X,seg,T_pass=None):
    T_ref    = len(dB)
    len_t    = np.divide(np.divide(T_ref,len(X)),seg)
    if len_t>=3600:
        T_end    = np.divide(len_t,3600)
        if T_pass==None:
            T_pass=int(T_end)+3
    if len_t<3600 and len_t>=60:
        T_end    = np.divide(len_t,60)
        if T_end<20:
            if T_pass==None:
                T_pass=int(T_end)+3
        else:
            if T_pass==None:
                T_pass=int(T_end/5)
    if len_t<60:
        T_end    = len_t
        if T_end<20:
            if T_pass==None:
                T_pass=int(T_end)+3
        else:
            if T_pass==None:
                T_pass=int(T_end/5)
    Time     = np.around(np.linspace(0,T_end,num=T_pass),1)
    Time_Ticks=[((Time[int(i)]),Time[int(i)])for i in range(len(Time))]
    return Time_Ticks

def time_calculator(in_t_inic,in_t_segm,in_t_delta,in_t_fade):
    filez = file.filebrowser()
    acom_chunks=0
    m_rest = 0
    for filepath in filez:
        if filepath == filez[0]:
            time_lapse_vector = np.zeros(shape=(1, 2))  # Prealocación de vector de ceros para el timelapse.
        in_sig                                  = audio.SoundFile(filepath, 'r')  # Lectura de Audio.
        samp_freq                               = in_sig.samplerate  # Frecuencia de Muestreo.
        len_in_sig                              = len(in_sig)  # Número de muestras de la señal.
        # Preprocesado: Transformación de seg/min a muestras.
        m_pass                                  = len_in_sig + m_rest
        m_desc, m_fades, m_inic_desc, m_segment = tl.time_to_samples(in_t_inic, in_t_segm, in_t_delta, in_t_fade, samp_freq)

        n_chunks,m_rest                         = tl.get_nchunks_cal(m_pass, m_inic_desc, m_segment, m_desc)  # Número de segmentos del timelapse
        acom_chunks +=n_chunks
    sum_continuo = 0
    time_chunk = (in_t_segm-2*in_t_fade)
    for i in range(acom_chunks-1):
        sum_continuo += time_chunk
    sum_fade = 0
    for j in range(acom_chunks-2):
        sum_fade += in_t_fade
    time = 2*in_t_fade + sum_fade + sum_continuo
    if time>60 and time<3600:
        minute=int(time/60)
        sec = int(time - minute*60)
        if minute >1:
            return print('El soundlapse duraria '+str(minute)+' minutos '+'y '+str(sec)+' segundos')
        else:
            return print('El soundlapse duraria '+str(minute)+' minuto '+'y '+str(sec)+' segundos')   
    if time>3600:
        hour=int(time/3600)
        minute=int((time - hour*3600)/60)
        sec = int(time - minute*60 - hour*3600)
        if hour>1:
            if minute >1:
                return print('El soundlapse duraria '+str(hour)+'horas'+str(minute)+' minutos '+'y '+str(sec)+' segundos')
            else:
                return print('El soundlapse duraria '+str(hour)+'horas'+str(minute)+' minuto '+'y '+str(sec)+' segundos')
        else:
            if minute >1:
                return print('El soundlapse duraria '+str(hour)+'hora'+str(minute)+' minutos '+'y '+str(sec)+' segundos')
            else:
                return print('El soundlapse duraria '+str(hour)+'hora'+str(minute)+' minuto '+'y '+str(sec)+' segundos')
    if time<60:
        return print('El soundlapse duraria '+str(int(time))+' segundos')

def total_len(filez):
    cont=0
    for filepath in filez:
        in_sig                                  = audio.SoundFile(filepath, 'r') 
        len_sig                                 = len(in_sig)
        cont                                   += len_sig
    time=cont/(44100*3600)
    time_hrs=int(time)
    time_min=(time-time_hrs)*60
    time_sec=int((time_min-int(time_min))*60)
    len_ideal=(time_hrs*3600 + int(time_min)*60 + time_sec)*44100
    if time_hrs>=1:    
        target='Hrs'
        print(time_hrs,'horas',int(time_min),'minutos',time_sec,'segundos en',len(filez),'archivos')          
    else:
        if time_min>=1:
            target='Min'
            print(int(time_min),'minutos',time_sec,'segundos en',len(filez),'archivos')
        else:
            target='Seg'
            print(time_sec,'segundos en',len(filez),'archivos')
    return cont,len_ideal,target    

def time_hover(dB,X,seg,target):
    T_ref    = len(dB)
    if target=='Hrs':
        T_end    = np.divide(np.divide(np.divide(T_ref,len(X)),seg),3600)
    if target=='Min':
        T_end    = np.divide(np.divide(np.divide(T_ref,len(X)),seg),60)  
    if target=='Seg':
        T_end    = np.divide(np.divide(T_ref,len(X)),seg)  
    Time_ref = np.linspace(0,T_end,num=T_ref)
    return Time_ref

def spec_norm(dB):
    exp_dB      = np.power(10,np.divide(dB,20))
    max_exp_dB  = np.max(exp_dB) 
    norm_exp_dB = np.divide(exp_dB,max_exp_dB)
    new_dB      = log.decibel(norm_exp_dB)
    return new_dB