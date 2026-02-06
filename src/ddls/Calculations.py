# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:31:36 2019

@author: Jacob
"""
from ddls.geometric_functions_for_DDLS import GeneralDims, OptimizingFunction
import numpy as np
import time
from scipy.optimize import root
from statistics import mode
from statistics import StatisticsError
from ddls.modelGrapher import grapher, compare_solvers
# for per-solver shape plots in compare (to show solver in HTML + auto-open)
from ddls.grapher_tools import sphere_plotter, cylinder_plotter

### SOLVER: 

amtg = 300 # amount of starting guesses
digits = 6 # desired digits when solving

def Solver(modelname, T, D_tr, D_rot, solver_choice='hybr', plot_type='html', save_loc=None):
    # use modern root (hybr default) instead of fsolve; support compare of hybr+lm only (broyden1 errors); perf timing + compare plot
    methods = ['hybr', 'lm']
    if solver_choice == 'compare':
        print(f"Comparing all solvers for {modelname} model...")
        results = {}
        for method in methods:
            start = time.perf_counter()
            zeros = []
            if modelname == 'prolate':
                for val in np.linspace(1.000001, 80.9, amtg):
                    sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=method)
                    zeros.append(sol.x[0] if sol.success else np.nan)
            if modelname == 'oblate':
                for val in np.linspace(.000001, 0.99999, amtg):
                    sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=method)
                    zeros.append(sol.x[0] if sol.success else np.nan)
            if modelname == 'cylinder':
                for val in np.linspace(0.01, 9.9, amtg):
                    sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=method)
                    zeros.append(sol.x[0] if sol.success else np.nan)
            elapsed = time.perf_counter() - start
            try:
                rho = mode([round(z, digits) for z in zeros if not np.isnan(z)])
                length, width = GeneralDims(modelname, rho, T, D_tr, D_rot)
                results[method] = {'rho': rho, 'length': length, 'width': width, 'time': elapsed}
                print(f"  {method} solver -> Aspect ratio: {rho}, Length: {round(10**9*length)} nm, Width: {round(10**9*width)} nm, Time: {elapsed:.4f}s")
                # generate per-solver 3D shape (shows solver in title; auto-opens HTML for each)
                fname = f'{modelname}_{rho}_{method}'
                length_nm = length * 1e9
                width_nm = width * 1e9
                if modelname == 'cylinder':
                    cylinder_plotter(fname, width_nm/2, length_nm, plot_type=plot_type, save_loc=save_loc)
                elif modelname in ('oblate', 'prolate'):
                    rz = min(width_nm, length_nm)/2
                    rx = max(width_nm, length_nm)/2
                    ry = max(width_nm, length_nm)/2
                    sphere_plotter(fname, rx, ry, rz, plot_type=plot_type, save_loc=save_loc)
            except:
                results[method] = {'rho': "No solution", 'length': None, 'width': None, 'time': elapsed}
                print(f"  {method} solver -> No solution, Time: {elapsed:.4f}s")
        # use default for final dims/plot
        solver_choice = 'hybr'
        print("Using 'hybr' for final dimensions/plot.")
        # generate compare figure as last option
        compare_solvers(results, modelname, plot_type, save_loc)
    # standard run for chosen method
    zeros = []
    if modelname == 'prolate':
        for val in np.linspace(1.000001, 80.9, amtg):
            sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=solver_choice)
            zeros.append(sol.x[0] if sol.success else np.nan)
    if modelname == 'oblate':
        for val in np.linspace(.000001, 0.99999, amtg):
            sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=solver_choice)
            zeros.append(sol.x[0] if sol.success else np.nan)
    if modelname == 'cylinder':
        for val in np.linspace(0.01, 9.9, amtg):
            sol = root(OptimizingFunction(modelname, T, D_tr, D_rot), val, method=solver_choice)
            zeros.append(sol.x[0] if sol.success else np.nan)
    
    try:
        rho = mode([round(z, digits) for z in zeros if not np.isnan(z)])
        print(f"Aspect ratio (for {modelname} model, {solver_choice} solver): {rho}")
        length, width = GeneralDims(modelname, rho, T, D_tr, D_rot)
        print(f"Length: {round(10**9 * length)} nm")
        print(f"Width: {round(10**9 * width)} nm")
        return length, width

    except (StatisticsError, ValueError):
        print("No solution.")
        return None, None
        
def runner(model, T, D_tr, D_rot, plot_type='html', save_loc=None, solver_choice='hybr'):
    length, width = Solver(model, T, D_tr, D_rot, solver_choice, plot_type, save_loc)
    if length is not None:
        grapher(length, width, model, T, D_tr, D_rot, plot_type, save_loc)
