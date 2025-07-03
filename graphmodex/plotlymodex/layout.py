from typing import Union
import plotly.graph_objects as go


__all__ = [
    'plotly_main_layout',
    'plotly_main_subplot_layout',
]


def plotly_main_layout(fig: go.Figure, width=700, height=600, x='x', y='y', title=None,
                       x_range=None, y_range=None, paper_color='white', 
                       customdata: Union[str, None] = None, hover_customdata='Info', 
                       hover_x='x', hover_y='y', **kwargs) -> go.Figure:
    fig.layout = go.Layout(
        width=width,
        height=height,
        plot_bgcolor=paper_color,
        paper_bgcolor=paper_color,
        xaxis={'gridcolor': '#CCCCCC', 'zerolinecolor': '#AAAAAA', 'linecolor': 'black', 'title': x, 'range': x_range},
        yaxis={'gridcolor': '#CCCCCC', 'zerolinecolor': '#AAAAAA', 'linecolor': 'black', 'title': y, 'range': y_range},
        title={'text': title},
    )
    
    # Update the layout using valid kwargs
    fig.update_layout(
        **kwargs
    )
    
    if isinstance(customdata, str) and customdata == 'no':
        ...
    elif customdata is None:
        fig.update_traces(patch={
            'customdata': customdata, 'hovertemplate': hover_x + ': %{x}<br>' + hover_y + ': %{y}'
        })
    else:
        fig.update_traces(patch={
            'customdata': customdata,
            'hovertemplate': hover_x + ': %{x}<br>' + hover_y + ': %{y}<br>' + hover_customdata + ': %{customdata}<br>'
        })
    
    return fig




def plotly_main_subplot_layout(fig:go.Figure, width=1400, height=500, title=None, paper_color='white',
                        x='x', y='y', rows=1, cols=2, x_range=None, y_range=None,
                        customdata:Union[str, None]=None, hover_customdata='Info', 
                        hover_x='x',hover_y='y', **kwargs) -> go.Figure:
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
            range=x_range
        )
    for yaxis in fig.select_yaxes():
        yaxis.update(
            showgrid=True,
            gridcolor='#CCCCCC',
            zerolinecolor='#AAAAAA',
            linecolor='black',
            title=y,
            range=y_range
        )
    if isinstance(customdata, str) and customdata == 'no':
        ...
    elif customdata is None:
        fig.update_traces(patch={
            'customdata':customdata, 'hovertemplate': hover_x + ': %{x}<br>' + hover_y + ': %{y}'
        })
    else:
        fig.update_traces(patch={
            'customdata':customdata,
            'hovertemplate': hover_x + ': %{x}<br>' + hover_y + ': %{y}<br>' + hover_customdata + ': %{customdata}<br>'
        })
    return fig