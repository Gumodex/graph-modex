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
            xaxes_names='x', yaxes_names='y',
            layout_kwargs:dict=None, subplots_kwargs:dict=None,):
    """
    Combine multiple Plotly figures into a single subplot layout with shared configuration.

    Parameters
    ----------
    figs : list of go.Figure
        List of Plotly figures to combine into subplots.
    rows : int, optional
        Initial number of rows in the subplot grid. Adjusted automatically if not sufficient.
        Default is 1.
    cols : int, optional
        Number of columns in the subplot grid. Default is 2.
    subplot_titles : list of str, optional
        Titles for each subplot. If None, titles are taken from the individual figures' titles.
    title : str, optional
        Title for the entire figure. Default is 'Plots'.
    width : int, optional
        Width of the entire figure in pixels. Default is 1400.
    height : int, optional
        Height of the entire figure in pixels. Default is 600. Increased if more rows are added.
    legends : list of bool, optional
        List specifying whether to show legend for each subplot. Defaults to showing all.
    shared_xaxes : bool, optional
        Whether x-axes should be shared across subplots. Default is False.
    shared_yaxes : bool, optional
        Whether y-axes should be shared across subplots. Default is False.
    horizontal_spacing : float, optional
        Spacing between subplot columns as a fraction of the plot width. Default is 0.08.
    vertical_spacing : float, optional
        Spacing between subplot rows as a fraction of the plot height. Default is 0.08.
    layout_kwargs : dict, optional
        Additional layout settings to apply to the main figure. (Unused in current version)
    subplots_kwargs : dict, optional
        Additional keyword arguments passed to `make_subplots`.
    xaxes_names : list, optional
        Provide the names for all X axis
    yaxes_names : list, optional
        Provide the names for all Y axis

    Returns
    -------
    go.Figure
        A combined Plotly figure with subplots arranged in the specified layout.

    Raises
    ------
    ValueError
        If the input `figs` list is empty.

    Examples
    --------
    >>> from graphmodex import plotlymodex
    >>> 
    >>> fig1 = go.Figure()
    >>> fig1.add_trace(go.Scatter(x=x1, y=y1))
    >>> fig2 = go.Figure()
    >>> fig1.add_trace(go.Scatter(x=x2, y=y2))
    >>> 
    >>> plotlymodex.subplot(
    >>>         figs=[fig1, fig2], rows=1, cols=2,
    >>>         subplot_titles=['Fig 1', 'Fig 2'],
    >>>         width=700, height=700
    >>>     )
    >>> fig.show()
    >>> 
    >>> plotlymodex.subplot(
    >>>         figs=[fig1, fig2], rows=2, cols=1,
    >>>         subplot_titles=['Fig 1', 'Fig 2'],
    >>>         title='Plots', legends=[1, 0]
    >>>     )
    >>> fig.show()
    """
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

    if layout_kwargs:
        fig.update_layout(**layout_kwargs)


    # ---- AXIS' NAMES ----

    # How many axis exists
    num_x = sum(1 for k in fig.layout if k.startswith("xaxis"))
    num_y = sum(1 for k in fig.layout if k.startswith("yaxis"))

    # If only a string → replicate to all axis
    if isinstance(xaxes_names, str):
        xaxes_names = [xaxes_names] * num_x
    if isinstance(yaxes_names, str):
        yaxes_names = [yaxes_names] * num_y

    # Complete short lists with commum values
    if len(xaxes_names) < num_x:
        xaxes_names += ['x'] * (num_x - len(xaxes_names))
    if len(yaxes_names) < num_y:
        yaxes_names += ['y'] * (num_y - len(yaxes_names))

    # Apply the axis' names
    for i in range(1, num_x + 1):
        fig.layout[f"xaxis{i}"].title.text = xaxes_names[i-1]

    for i in range(1, num_y + 1):
        fig.layout[f"yaxis{i}"].title.text = yaxes_names[i-1]


    return fig