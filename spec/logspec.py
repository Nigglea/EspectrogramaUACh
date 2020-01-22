import numpy
import scipy
import scipy.io.wavfile as wav
import scipy.signal as sign
import librosa.core as lib 

def decibel(lin):
	eps = numpy.finfo(float).eps
	d = 20*numpy.log10(lin)
	return d

def norm(sig):
	sig_max = numpy.float(numpy.max(numpy.abs(sig)))
	return sig / sig_max

def log_scale(spec,freq,fs,size):

	y=numpy.linspace(0,size,num=size+1,dtype='int')
	k=numpy.divide(size,numpy.log10(fs/2))
	x=numpy.zeros(size+1)
	logspec=numpy.zeros((len(x),len(spec[0])))
	for i in y:
		exp=numpy.divide(i,k)
		po=numpy.around(numpy.power(10,exp),2)
		x[i]=po	
		try:	
			x_min=numpy.max(numpy.where(po>freq))
		except ValueError:
			x_min=0
		try:
			x_max=numpy.min(numpy.where(po<freq))
		except ValueError:
			x_max=len(freq)-1
		delta_1=float(po-freq[x_min])
		delta_2=float(freq[x_max]-po)
		if delta_1<delta_2:
			logspec[i]=spec[x_min][:]
		if delta_1>delta_2:
			logspec[i]=spec[x_max][:]
	x=numpy.log10(numpy.array((x)))
	logspec=numpy.array((logspec))
	return x ,logspec

def long_spectrogram(data,fs,win_length=16384,hop_length=8192,yprune=512,
						fmax = None,n_fft=None):
	if n_fft == None:
		n_fft=win_length
	C = lib.stft(data,n_fft=n_fft ,win_length=win_length, hop_length=hop_length)
	C = numpy.abs(C)
	# 
	if fmax == None:
		fmax = int(fs/2)
	ylen = int((fmax/2+1))
	# 
	C = C[0:ylen]
	# 
	ylen = len(C)
	# 
	x = numpy.linspace(0, len(data)/fs, len(C[0]))
	# 
	y = numpy.linspace(1, fmax, ylen)
	# 
	(y,d) = log_scale(spec=C, freq=y, fs=fs,size=yprune)
	# 
	d=decibel(d)
	return (x, y, d)
