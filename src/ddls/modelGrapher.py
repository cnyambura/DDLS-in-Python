# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:04:00 2019

@author: Jacob
"""

# PLOTTER
import numpy as np
from ddls.grapher_tools import sphere_plotter, cylinder_plotter

RESOLUTION = 256
pi=np.pi



def grapher(length, width, model, T, D_tr, D_rot, plot_type='html', save_loc=None):
    rho = length/width
    width *= 1e9
    length *= 1e9 # convert them from nm

    if model == 'cylinder':
        
        cylinder_plotter(f'{model}_{rho}', width/2, length, plot_type=plot_type, save_loc=save_loc)

    if model == 'oblate':

        rz=min(width,length)/2
        rx=max(width,length)/2
        ry=max(width,length)/2
        sphere_plotter(f'{model}_{rho}', rx, ry, rz, plot_type, save_loc)

    if model == 'prolate':
        
        rz=max(width, length)/2
        rx=min(width, length)/2
        ry=min(width, length)/2
        sphere_plotter(f'{model}_{rho}', rx, ry, rz, plot_type, save_loc)


# compare plot for solvers (bars for rho/L/W + times) when compare chosen
import plotly.graph_objects as go
import os

def compare_solvers(results, modelname, plot_type='html', save_loc=None):
    solvers = list(results.keys())
    rhos = [results[s]['rho'] if isinstance(results[s]['rho'], (int,float)) else 0 for s in solvers]
    lengths = [results[s]['length']*1e9 if results[s]['length'] else 0 for s in solvers]
    widths = [results[s]['width']*1e9 if results[s]['width'] else 0 for s in solvers]
    times = [results[s]['time'] for s in solvers]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=solvers, y=rhos, name='Aspect Ratio', marker_color='blue'))
    fig.add_trace(go.Bar(x=solvers, y=lengths, name='Length (nm)', marker_color='green'))
    fig.add_trace(go.Bar(x=solvers, y=widths, name='Width (nm)', marker_color='red'))
    # secondary for time?
    fig.add_trace(go.Scatter(x=solvers, y=times, name='Time (s)', mode='lines+markers', yaxis='y2', line=dict(color='orange')))

    fig.update_layout(
        title=f'Solver Comparison for {modelname} Model',
        xaxis_title='Solver Method',
        yaxis_title='Value',
        yaxis2=dict(title='Time (s)', overlaying='y', side='right'),
        barmode='group',
        legend=dict(x=1.1, y=1)
    )

    filename = f'{modelname}_solvers_compare'
    if plot_type == 'html':
        ext = '.html'
        save_location = f'{os.getcwd() if save_loc is None else save_loc}/{filename}{ext}'
        fig.write_html(save_location, auto_open=True)
    else:
        ext = '.png'
        save_location = f'{save_loc}/{filename}{ext}'
        fig.write_image(save_location)
    print(f'Compare figure saved at {save_location}')
