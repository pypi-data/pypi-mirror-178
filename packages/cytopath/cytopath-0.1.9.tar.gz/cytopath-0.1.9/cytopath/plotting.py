from .plotting_functions.plot_alignment import pl_cytopath_alignment
from .plotting_functions.plot_sampling import pl_cytopath_sampling
from .plotting_functions.plot_radial_heatmap import radial_heatmap

def plot_trajectories(data, directory='', basis='', size=10, figsize=(12,3), save_type='svg', smoothing=False):
    pl_cytopath_alignment(data, folder=directory, basis=basis, size=size, figsize=figsize, smoothing=smoothing, save_type=save_type)

def plot_sampling(data, directory='', basis=''):
    pl_cytopath_sampling(data, folder=directory, basis=basis)
