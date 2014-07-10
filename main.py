import os, sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.interpolate as interp
from netCDF4 import Dataset
import operator

in_file =  str(sys.argv[1])
output_radius =  float(sys.argv[2])
output_time =  float(sys.argv[3])
ncfile = Dataset(in_file, 'r', format='NETCDF3')

#Read relevant data from TRANSP file
time = ncfile.variables['TIME'][:]

#Convert input time to an index
t_idx, min_value = min(enumerate(abs(time - output_time)), key=operator.itemgetter(1))

x = ncfile.variables['X'][t_idx,:]
xb = ncfile.variables['XB'][t_idx,:]
ni = ncfile.variables['NI'][t_idx,:]
ne = ncfile.variables['NE'][t_idx,:]
ti = ncfile.variables['TI'][t_idx,:]
te = ncfile.variables['TE'][t_idx,:]
fbtx = ncfile.variables['FBTX'][t_idx,:]
bpbt = ncfile.variables['FBPBT'][t_idx,:]
btx = ncfile.variables['BTX'][t_idx,:]
rmaj = ncfile.variables['RMAJM'][t_idx,:]
bpol = ncfile.variables['BPOL'][t_idx,:]
omega = ncfile.variables['OMEGA'][t_idx,:]
q = ncfile.variables['Q'][t_idx,:]
shat = ncfile.variables['SHAT'][t_idx,:]
flux_centres = ncfile.variables['RMJMP'][t_idx,:]
elongation = ncfile.variables['ELONG'][t_idx,:]
triang = ncfile.variables['TRIANG'][t_idx,:]
zeffp = ncfile.variables['ZEFFP'][t_idx,:]

#Normalization quantities
amin = 0.58044
boltz_jk = 1.3806488e-23
boltz_evk = 8.6173324e-5
proton_mass = 1.672621777e-27


###################################
#Calculate equilibrium parameters #
###################################
equil = {}
equil['dens_1'] = np.interp(output_radius, x, ni)*1e6/1e19
equil['dens_2'] = np.interp(output_radius, x, ne)*1e6/1e19
equil['temp_1'] = np.interp(output_radius, x, ti)/1000 #keV
vth = np.sqrt((2*equil['temp_1']*1000*boltz_jk/boltz_evk)/(2*proton_mass))
equil['temp_2'] = np.interp(output_radius, x, te)/1000 #keV
equil['omega'] = np.interp(output_radius, x, omega) #rad/s
mag_axis_idx, min_value = min(enumerate(abs(bpbt)), key=operator.itemgetter(1))
equil['btref'] = fbtx[mag_axis_idx]*btx[mag_axis_idx]
equil['beta'] = 403.0*equil['dens_1']*equil['temp_1']/(1e5*equil['btref']**2)
equil['zeff'] = np.interp(output_radius, x, zeffp)
equil['qinp'] = np.interp(output_radius, x, q)

# Gradient calculation requires numerical differentiation
# Use a second order central method: f'(x) = [f(x+h) - f(x-h)]/2h
# Find points closest points either side of output_radius and use those
rad_idx, min_value = min(enumerate(abs(x - output_radius)), key=operator.itemgetter(1))
if x[rad_idx] < output_radius:
  rad_idx += 1
else:
  rad_idx -= 1

equil['fprim_1'] = -(ni[rad_idx+1]-ni[rad_idx-1])/(x[rad_idx+1]-x[rad_idx-1])/ni[rad_idx]
equil['fprim_2'] = -(ne[rad_idx+1]-ne[rad_idx-1])/(x[rad_idx+1]-x[rad_idx-1])/ne[rad_idx]
equil['tprim_1'] = -(ti[rad_idx+1]-ti[rad_idx-1])/(x[rad_idx+1]-x[rad_idx-1])/ti[rad_idx]
equil['tprim_2'] = -(te[rad_idx+1]-te[rad_idx-1])/(x[rad_idx+1]-x[rad_idx-1])/te[rad_idx]
equil['g_exb'] = (omega[rad_idx+1]-omega[rad_idx-1])/(x[rad_idx+1]-x[rad_idx-1])*(x[rad_idx]/q[rad_idx])*(amin/vth)
print equil['g_exb']
print rad_idx, x[rad_idx+1]-x[rad_idx-1], omega[rad_idx+1]-omega[rad_idx-1], output_radius/equil['qinp'], amin/vth




f = open('gs2.in', 'w')
f.write('Equilibrium Parameters: \n')
for name, value in equil.items():
  f.write(name + ' = ' + str(value) + '\n')


###################################
#Calculate geoemetry parameters #
###################################
geometry = {}




















