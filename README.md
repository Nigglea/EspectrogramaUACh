# EspectrogramaUACh

## Logarithmic Spectrograms of long duration
This repository contains the functions to plot spectrograms mentioned in *High Performance Tools to Generate and Visualize Sound Time-Lapse* [Espejo et al. 2020]


### Lenguage
This algorithm was created in Python 3.7.4.

#### Install packages
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements to use STL.

```bash
pip install -r requirements.txt  
```
or 
```bash
pip3 install -r requirements.txt  
```

## STFT
A la seleccion de archivos *.wav* se le realiza una *Transformada de Fourier en tiempo corto* (siglas en ingles STFT) con los siguientes parametros: 

    - resolucion 
1 Segundo

    - largo de ventana 
    
2 <sup>14</sup> Muestras

    - largo de traslape 

2 <sup>13</sup> Muestras




### Authors
<p style="text-align:center">Diego Espejo <br>
<a href="mailto:diego.es
         pejo@alumnos.uach.cl">diego.espejo@alumnos.uach.cl</a><br>
<p style="text-align:center">Victor Vargas <br>
<a href="mailto:victorvargassandoval93@gmail.com">victorvargassandoval93@gmail.com</a><br>
<p style="text-align:center">Asistentes de investigación en procesamiento de señales <br>
<a href="http://www.acusticauach.cl">www.acusticauach.cl</a><br>

### Acknowledgments
We acknowledge support from CONICYT-Chile, through the FONDECYT Regular projects 1190722 and 1170305.

### Reference
