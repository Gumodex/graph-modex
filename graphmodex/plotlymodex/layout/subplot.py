import os
import sys
import copy

import plotly.subplots as subplots

sys.path.append(os.path.abspath('..'))
from graphmodex import plotlymodex


__all__ = [
    'subplot'
]


def subplot(figs:list, rows:int=1, cols:int=2, subplot_titles:list[str]=None, title:str='Plots',
            width:int=1400, height:int=600, legends:list[bool]=[],
            shared_xaxes:bool=False, shared_yaxes:bool=False,
            horizontal_spacing:float=0.08, vertical_spacing:float=0.08,
            layout_kwargs:dict=None, subplots_kwargs:dict=None):

    if len(figs) == 0:
        raise ValueError("The 'figs' argument must contain at least one figure.")
    
    figs = [copy.deepcopy(f) for f in figs]

    while len(legends) < len(figs):
        legends.append(1)
    legends = [bool(x) for x in legends]
    for i, fig_ in enumerate(figs):
        for trace_ in fig_.data:
            trace_.showlegend = legends[i]

    while rows*cols < len(figs):
        rows += 1
        height += 400
        vertical_spacing = 0.1
    
    if subplot_titles is None:
        subplot_titles = []
        for fig_ in figs:
            subplot_titles.append(fig_.layout['title']['text'])

    fig = subplots.make_subplots(
        rows=rows, cols=cols, subplot_titles=subplot_titles,
        shared_xaxes=shared_xaxes, shared_yaxes=shared_yaxes, 
        horizontal_spacing=horizontal_spacing, vertical_spacing=vertical_spacing,
        **(subplots_kwargs or {})
    )

    for i, f in enumerate(figs):
        row = i // cols + 1
        col = i % cols + 1
        for trace in f.data:
            fig.add_trace(trace, row=row, col=col)

    plotlymodex.main_layout(fig, title=title, width=width, height=height, x='x', y='y')

    return fig