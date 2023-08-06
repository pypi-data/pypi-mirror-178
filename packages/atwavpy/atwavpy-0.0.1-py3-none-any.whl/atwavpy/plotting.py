
##################################################################

import numpy as np
import matplotlib.pyplot as plt

##################################################################

__all__ = ['plot_beam_caustic', 'plot_peak_focal']

##################################################################

def plot_beam_caustic(field):
    ydim = field.caustic_xdim*1e6
    fig = plt.figure()
    plt.imshow(np.abs(field.caustic)**2, extent=[field.caustic_range[-1]*1e3, field.caustic_range[0]*1e3, -ydim/2, ydim/2], aspect='auto')
    fig.suptitle('Beam Caustic', y=0.96, fontweight='bold', fontsize=18)
    plt.xlabel('Longitudinal Position [$\mathrm{mm}$]', fontsize=16)
    plt.ylabel('Transverse Position [$\mathrm{\mu m}$]', fontsize=16)        

##################################################################

def plot_peak_focal(field):
    nz = field.caustic.shape[0]
    zrange = np.linspace(field.caustic_range[-1], field.caustic_range[0], nz)*1e3
    fig = plt.figure()
    plt.plot(zrange, np.sum(np.abs(field.caustic)**2, axis=1))
    fig.suptitle('Peak Focal Position', y=0.96, fontweight='bold', fontsize=18)
    plt.xlabel('Longitudinal Position [$\mathrm{mm}$]', fontsize=16)
    plt.ylabel('Intensity [$\mathrm{a.u.}$]', fontsize=16)   
    

##################################################################