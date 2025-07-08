from typing import Union, Literal
import plotly.graph_objects as go


__all__ = [
    'main_layout',
]


def main_layout(fig:go.Figure, width=700, height=600, title=None, paper_color='white',
                        x='x', y='y', rows=1, cols=2, x_range=None, y_range=None,
                        x_type:Literal["linear","log","date","category","multicategory"]="-",
                        y_type:Literal["linear","log","date","category","multicategory"]="-",
                        x_hover='x', y_hover='y', customdata:Union[str, None]=None, hover_customdata='Info', 
                        legend_border_color:str='#ffffff', legend_background_color:str='#ffffff', legend_border_width:str=1,
                        legend_orientation:Literal['v','h']='v', legend_x:float=None, legend_y:str=None,
                        **kwargs) -> go.Figure:
    fig.update_layout({
        'width':width,
        'height':height,
        'plot_bgcolor':paper_color,
        'paper_bgcolor':paper_color,
        'title':title,
        **kwargs
    })
    
    for xaxis in fig.select_xaxes():
        xaxis.update(
            showgrid=True,
            gridcolor='#CCCCCC',
            zerolinecolor='#AAAAAA',
            linecolor='black',
            title=x,
            range=x_range,
            type=x_type,
        )
    for yaxis in fig.select_yaxes():
        yaxis.update(
            showgrid=True,
            gridcolor='#CCCCCC',
            zerolinecolor='#AAAAAA',
            linecolor='black',
            title=y,
            range=y_range,
            type=y_type,
        )
        
    if isinstance(customdata, str) and customdata == 'no':
        ...
    elif customdata is None:
        fig.update_traces(patch={
            'customdata': customdata, 'hovertemplate': x_hover + ': %{x}<br>' + y_hover + ': %{y}'
        })
    else:
        fig.update_traces(patch={
            'customdata': customdata,
            'hovertemplate': x_hover + ': %{x}<br>' + y_hover + ': %{y}<br>' + hover_customdata + ': %{customdata}<br>'
        })

    fig.update_layout(
        showlegend=True,
        legend=dict(
            x=legend_x,
            y=legend_y,
            bgcolor=legend_background_color,
            bordercolor=legend_border_color,
            borderwidth=legend_border_width,
            orientation=legend_orientation,
        )
    )
    
    return fig