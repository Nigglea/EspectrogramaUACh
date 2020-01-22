import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
import holoviews as hv
from holoviews import opts
import holoviews.operation.datashader as hd
import bokeh.models as bm
hv.extension('bokeh')

def plot(dB_plot,X,Ylog,
        Freq_Ticks,Time_Ticks,target,
        title,archive,ylim=(20,20000)):
    agg   = hv.Image((dB_plot),rtol=513)
    agg.opts(cmap='Greys',colorbar=True)
    img   = hd.rasterize(agg,height=600,width=1600,y_range=(min(Ylog),max(Ylog)))
    img2  = img*hv.util.Dynamic(hd.rasterize(agg, width=480, height=600), operation=hv.QuadMesh)
    hover = bm.HoverTool(tooltips=[
        ('Tiempo','@Tiempo'),
        ('Hz','@Freq'),
        ('dB','@dB')]
        )
    img2.opts(opts.QuadMesh(tools=['crosshair',hover],
                            height=600,width=1600,
                            ylim=ylim,
                            logy=True,
                            alpha=0, hover_alpha=0.1,
                            fontsize={'title': 16, 'labels': 40, 'xticks': 14, 'yticks': 14}
                        )
            )
    img2.opts(xlabel='Time ['+target+']',ylabel='Frecuency [Hz]',
            yticks=Freq_Ticks,
            xticks=Time_Ticks,
            axiswise=True,
            framewise=True,
            title=title
            )
    path='Resultados/'+archive+'.html'
    hv.save(img2,path)
    return path,print('Imagen creada')

def mel_plot(dB_plot,Time_ref,Ymel,
        Freq_Ticks,Time_Ticks,target,
        title,archive,ylim=(20,20000)):
    agg   = hv.QuadMesh((Time_ref,Ymel,dB_plot.T))
    agg.opts(opts.QuadMesh(cmap='Greys',ylim=ylim,logy=True,colorbar=True))
    img   = hd.rasterize(agg,height=600,width=1600,y_range=(min(Ymel),max(Ymel)))
    img2  = img*hv.util.Dynamic(hd.rasterize(agg, width=600, height=800), operation=hv.QuadMesh)
    hover = bm.HoverTool(tooltips=[
        ('Tiempo','@Tiempo'),
        ('Hz','@Freq'),
        ('dB','@dB')]
        )
    img2.opts(opts.QuadMesh(tools       = ['crosshair','hover'],
                            height      = 600,
                            width       = 1600,
                            ylim        = ylim,
                            logy        = True,
                            alpha       = 0, 
                            hover_alpha = 0.1,
                            cmap        = 'Greys',
                            colorbar    = True
                            )
            )
    img2.opts(xlabel  = 'Tiempo ['+target+']',
            ylabel    = 'Frecuencia [Hz]',
            yticks    = Freq_Ticks,
            xticks    = Time_Ticks,
            axiswise  = True,
            framewise = True,
            title     = title
            )
    path='Resultados/'+archive+'.html'
    hv.save(img2,path)
    return path,print('Imagen creada')