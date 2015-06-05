#-*- coding: utf-8 -*-
"""
plotEnv
=======

Custom plotting environment using seaborn (based on Matplotlib). Color scheme using
flat ui (http://designmodo.github.io/Flat-UI/).


:First Added:   2015-05-25
:Author:        Lento Manickathan

"""

# Import required modules
from matplotlib import pyplot as _plt
import seaborn as _sns
import numpy as _np


def setupPlotEnv(numColors=1,style='ticks'):
    """
    Setup the Qualitative plotting environment:
        1) Change color scheme to flat ui
        2) change style using seaborn
        3) Turns interactive on
        4) Change figure shape and font size ideal for publishing: see _modifyFigureAxes 

    Parameters
    ----------
    plotType : 'qualitative', ... {'sequential'}

    numColors : int, or one of {1 (default), 3, 9}
                The number of colour required for plotting.

    style : dict, None, or one of {darkgrid, whitegrid, dark, white, ticks (default)}
            A dictionary of parameters or the name of a preconfigured set.
                     
    
    See Also
    --------
    Color Scheme : Flat ui
                   http://designmodo.github.io/Flat-UI/

    seaborn.set : seaborn's aesthetic parameter setting function

    pyplot.ion : Turn interactive mode on.

    _modifyFigureAxes : Function to modify figure shape and font size


    Examples
    --------
    >>> setupPlotEnv(numColors=1, style='ticks')

    """

    # Define the color palatte
    if numColors == 1:
        # Midnight blue 
        flatui = ['#2c3e50']
    elif numColors == 2:
        # Alizarin, Peter river
        flatui = ['#e74c3c', '#3498db']
    elif numColors == 3:
        # Alizarin, Emerald, Peter river
        flatui = ['#e74c3c', '#2ecc71', '#3498db']
    elif numColors >= 4 and numColors <= 9:
        # Alizarin, Sun Flower, Emerald, Peter river, Wisteria, Midnight blue
        # Asbestos, Green sea, Pumpkin
        flatui = ['#e74c3c', '#f1c40f', '#2ecc71', '#3498db', '#8e44ad','#2c3e50',\
                  '#7f8c8d', '#16a085', '#d35400'][:numColors]
    else:
        return NotImplementedError('numColors should be 1 to 9.')
        
    # Change style according seaborn style
    _sns.set_style(style=style)

    # Change color scheme with flat ui color palette
    _sns.set_palette(flatui, n_colors=numColors)
    

    # Turn interactive on
    _plt.ion()

    # Adjust the size of the figure
    _modifyFigureAxes()

    return _sns.color_palette(n_colors=numColors)


def cleanupFigure(despine=True, tightenFigure=True, addMarkers=False, addLegend=True, labels=None, legendLoc=0):
    """
    Cleans up the figure by:
        1) Removing unnecessary top and right spines using seaborn's `despine` function
        2) Tighten the figure using pyplot's `tight_layout` function
        3) If outputFormat is projector, add markers to each data points.

    Parameters
    ----------
    despine : bool, True (default) or False

    tightenFigure : bool, True (default) or False
                     
 
    See Also
    --------
    seaborn.despine : Seaborn's despine function

    pyplot.tight_layout : Function to adjust the subplot padding

   
    Examples
    --------
    >>> cleanupFigure(despine=True, tightenFigure=True)
    
    """
    
    # Get current figure
    fig = _plt.gcf()
    
    # Remove extra spline
    if despine:
        _sns.despine()
   
    # Remove the extra white spaces
    if tightenFigure:
        fig.tight_layout()

    if addMarkers is True:
        for ax in fig.get_axes():
            _addMarkers(ax)

    if addLegend is True:
        if labels is None:
            _plt.legend(loc=legendLoc)
        else:
            _plt.legend(labels, loc=legendLoc)


def _modifyFigureAxes():
    """
    Modify the pyplot rc parameters figure axes according to: 
        http://wiki.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    """

    # Modify plot axes
    fig_width_pt    = 246.0 # Get this from LaTeX using \showthe\columnwidth
    inches_per_pt   = 1.0/72.27               # Convert pt to inch
    golden_mean     = (_np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
    fig_width       = 2*fig_width_pt*inches_per_pt  # width in inches
    fig_height      = fig_width*golden_mean      # height in inches
    fig_size        =  [fig_width,fig_height]
    params          = { 'axes.labelsize':   16,
                        'text.fontsize':    16,
                        'legend.fontsize':  10,
                        'xtick.labelsize':  14,
                        'ytick.labelsize':  14,#'lines.linewidth':  1.5,
                        'figure.figsize':   fig_size}#,
                     #'text.usetex':        True},
                    #'font.family': '   sans-serif'}
    _plt.rcParams.update(params)


def _addMarkers(ax):
    """
    Take each Line2D in the axes, ax, and add markers to the line. 
    Better for viewing in presentation slides (projectors)
    """

    # Marker size
    markerSize = 5

    # Marker types
    markerTypes = [ 'o', 's', 'D', 'v', '^', '<', 
                    '>','*', ',', '.', 'p', 'd', ]

    # Set marker for each line
    for i, line in enumerate(ax.get_lines()):
        line.set_marker(markerTypes[i])
        line.set_markersize(markerSize)

