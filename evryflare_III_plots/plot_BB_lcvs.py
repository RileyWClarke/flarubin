import glob
import copy
import numpy as np
import os
import astropy.table as tbl
from astropy import time, coordinates as coord, units as u
from astropy.stats import LombScargle
from astropy.io import fits
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from scipy.stats import sigmaclip
import scipy.signal
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from matplotlib.patches import ConnectionPatch
print ("\n")

arrow = u'$\u2191$'


i_array=[] #0
TIC_ID=[] #1
RA=[] #2
Dec=[] #3
Year=[] #4
Mon=[] #5
Day=[] #6
HR=[] #7
Min=[] #8
g_mags=[] #9
TESS_mags=[] #10
distance=[] #11
SpT=[] #12
mass=[] #13
Prot=[] #14
Ro=[] #15
Evry_Erg=[] #16
e_Evry_Erg=[] #17
TESS_erg=[] #18
e_TESS_Erg=[] #19
evr_peakFF=[] #20
tess_peakFF=[] #21
n_peaks=[] #22
tot_BB_data=[] #23
e_tot_BB_data=[] #24
tot_BB_data_trap=[] #25
e_tot_BB_data_trap=[] #26
E_tot_BB_data_trap=[] #27
tot_BB_sampl=[] #28
e_tot_BB_sampl=[] #29
E_tot_BB_sampl=[] #30
FWHM_BB_data=[] #31
e_FWHM_BB_data=[] #32
FWHM_BB_sampl=[] #33
e_FWHM_BB_sampl=[] #34
E_FWHM_BB_sampl=[] #35
FWHM=[] #36
impulse=[] #37

with open("evryflare_III_table_I.csv","r") as INFILE:
    next(INFILE)
    for lines in INFILE:
        i_array.append(int(lines.split(",")[0])) #0
        TIC_ID.append(int(lines.split(",")[1])) #1
        RA.append(float(lines.split(",")[2])) #2
        Dec.append(float(lines.split(",")[3])) #3
        Year.append(int(lines.split(",")[4])) #4
        Mon.append(int(lines.split(",")[5])) #5
        Day.append(int(lines.split(",")[6])) #6
        HR.append(int(lines.split(",")[7])) #7
        Min.append(int(lines.split(",")[8])) #8
        g_mags.append(float(lines.split(",")[9])) #9
        TESS_mags.append(float(lines.split(",")[10])) #10
        distance.append(float(lines.split(",")[11])) #11
        SpT.append(str(lines.split(",")[12])) #12
        mass.append(float(lines.split(",")[13])) #13
        Prot.append(float(lines.split(",")[14])) #14
        Ro.append(float(lines.split(",")[15])) #15
        Evry_Erg.append(float(lines.split(",")[16])) #16
        e_Evry_Erg.append(float(lines.split(",")[17])) #17
        TESS_erg.append(float(lines.split(",")[18])) #18
        e_TESS_Erg.append(float(lines.split(",")[19])) #19
        evr_peakFF.append(float(lines.split(",")[20])) #20
        tess_peakFF.append(float(lines.split(",")[21])) #21
        n_peaks.append(int(lines.split(",")[22])) #22
        tot_BB_data.append(float(lines.split(",")[23])) #23
        e_tot_BB_data.append(float(lines.split(",")[24])) #24
        tot_BB_data_trap.append(float(lines.split(",")[25])) #25
        e_tot_BB_data_trap.append(float(lines.split(",")[26])) #26
        E_tot_BB_data_trap.append(float(lines.split(",")[27])) #27
        tot_BB_sampl.append(float(lines.split(",")[28])) #28
        e_tot_BB_sampl.append(float(lines.split(",")[29])) #29
        E_tot_BB_sampl.append(float(lines.split(",")[30])) #30
        FWHM_BB_data.append(float(lines.split(",")[31])) #31
        e_FWHM_BB_data.append(float(lines.split(",")[32])) #32
        FWHM_BB_sampl.append(float(lines.split(",")[33])) #33
        e_FWHM_BB_sampl.append(float(lines.split(",")[34])) #34
        E_FWHM_BB_sampl.append(float(lines.split(",")[35])) #35
        FWHM.append(float(lines.split(",")[36])) #36
        impulse.append(float(lines.split(",")[37])) #37

i_array = np.array(i_array)
TIC_ID=np.array(TIC_ID)
TESS_mags=np.array(TESS_mags)
#print "T mag:", np.mean(TESS_mags)
#exit()

def get_temp_data(i):

    data_times=[]
    data_temps=[]
    data_lowerr=[]
    data_upperr=[]
    data_formal_lowerr=[]
    data_formal_upperr=[]
    with open(str(i)+"_flaretemp_data_lc.csv","r") as INFILE:
        for lines in INFILE:
            data_times.append(float(lines.split(",")[0]))
            data_temps.append(float(lines.split(",")[1]))
            data_lowerr.append(float(lines.split(",")[2]))
            data_upperr.append(float(lines.split(",")[3]))
            data_formal_lowerr.append(float(lines.split(",")[4]))
            data_formal_upperr.append(float(lines.split(",")[5]))
    data_times=np.array(data_times)
    data_temps=np.array(data_temps)
    data_lowerr=np.array(data_lowerr)
    data_upperr=np.array(data_upperr)
    data_formal_lowerr=np.array(data_formal_lowerr)
    data_formal_upperr=np.array(data_formal_upperr)

    return (data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr) 

def get_temp_model(i):

    model_times=[]
    model_temps=[]
    model_lowerr=[]
    model_upperr=[]
    with open(str(i)+"_flaretemp_model_lc.csv","r") as INFILE:
        for lines in INFILE:
            model_times.append(float(lines.split(",")[0]))
            model_temps.append(float(lines.split(",")[1]))
            model_lowerr.append(float(lines.split(",")[2]))
            model_upperr.append(float(lines.split(",")[3]))
    model_times=np.array(model_times)
    model_temps=np.array(model_temps)
    model_lowerr=np.array(model_lowerr)
    model_upperr=np.array(model_upperr)
    
    return (model_times, model_temps, model_lowerr, model_upperr)

def get_flare_fits(i):
    
    fit_times=[]
    fit_evry_fracflux=[]
    fit_tess_fracflux=[]
    with open(str(i)+"_flare_fits_lc.csv","r") as INFILE:
        for lines in INFILE:
            fit_times.append(float(lines.split(",")[0]))
            fit_evry_fracflux.append(float(lines.split(",")[1]))
            fit_tess_fracflux.append(float(lines.split(",")[2]))
    fit_times=np.array(fit_times)
    fit_evry_fracflux=np.array(fit_evry_fracflux)
    fit_tess_fracflux=np.array(fit_tess_fracflux)
            
    return (fit_times, fit_evry_fracflux, fit_tess_fracflux)

def get_fracflux(i):

    x_tess_and_evry=[]
    y_tess_and_evry=[]
    y_err_tess_and_evry=[]
    flag=[]
    with open(str(i)+"_flare_fluxes_lc.csv","r") as INFILE:
        for lines in INFILE:
            x_tess_and_evry.append(float(lines.split(",")[0]))
            y_tess_and_evry.append(float(lines.split(",")[1]))
            y_err_tess_and_evry.append(float(lines.split(",")[2]))
            flag.append(int(lines.split(",")[3]))
    x_tess_and_evry=np.array(x_tess_and_evry)
    y_tess_and_evry=np.array(y_tess_and_evry)
    y_err_tess_and_evry=np.array(y_err_tess_and_evry)
    flag=np.array(flag)

    x_tess = x_tess_and_evry[flag==0]
    y_tess = y_tess_and_evry[flag==0]
    y_tess_err = y_err_tess_and_evry[flag==0]
    x_evry = x_tess_and_evry[flag==1]
    y_evry = y_tess_and_evry[flag==1]
    y_evry_err = y_err_tess_and_evry[flag==1]
    
    return (x_tess, y_tess, y_tess_err, x_evry, y_evry, y_evry_err)

###################################################################

"""
# grab temperature at FlPeak in FWHM:
for i in i_array:
    x_tess, y_tess, y_tess_err, x_evry, y_evry, y_evry_err = get_fracflux(i)

    data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(i)

    model_times, model_temps, model_lowerr, model_upperr = get_temp_model(i)
    
    index = list(y_tess).index(np.nanmax(y_tess))

    flpk_time = x_tess[index]
    tess_pk_err = y_tess_err[index]
    evry_pk_err = y_evry_err[index] #might be wrong indexing

    diff_times = np.absolute(x_evry - flpk_time)
    x_evry_flpk = x_evry[list(diff_times).index(np.min(diff_times))]

    #fl_st = x_evry_flpk - 0.5*
    #fl_sp = x_evry_flpk
    #ED_val = np.trapz(y_evry[(x_evry>=fl_st)&(x_evry<=fl_sp)], x_evry[(x_evry>=fl_st)&(x_evry<=fl_sp)])
    # plot this and make sure is working
    #exit()
    
    diff_times = np.absolute(data_times - flpk_time)
    INS_TEMP = data_temps[list(diff_times).index(np.min(diff_times))]
    INS_T_UPP = data_formal_upperr[list(diff_times).index(np.min(diff_times))]
    INS_T_LOW = data_formal_lowerr[list(diff_times).index(np.min(diff_times))]
    
    #info = str(i)+","+str(INS_TEMP)+","+str(INS_T_LOW)+","+str(INS_T_UPP)+"\n"
    #with open("temperature_info_addendum.csv","a") as ADDENDUM:
    #    ADDENDUM.write(info)
    #info = str(i)+","+str(evry_pk_err)+","+str(tess_pk_err)+"\n"
    #with open("peak_info_addendum.csv","a") as ADDENDUM:
    #    ADDENDUM.write(info)
    #info = str(i)+","+str(Evry_FWHM_energy)+"\n"
    #with open("energy_info_addendum.csv","a") as ADDENDUM2:
    #    ADDENDUM2.write(info)

    plt.title(i)
    plt.plot(model_times, model_temps,color="royalblue")
    plt.plot(data_times, data_temps, ls="-",color="grey",alpha=0.6)
    plt.errorbar(data_times, data_temps, yerr=[data_lowerr, data_upperr],marker="o",ls="none",color="black")
    plt.axhline(14000, color="darkorange")
    plt.axhline(20000, color="red")
    plt.axhline(30000, color="purple")
    plt.xlabel("Time [d]",color="black", fontsize=16)
    plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=16)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)
    plt.show()
    #exit()
    
exit()
"""

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(102)

model_times, model_temps, model_lowerr, model_upperr = get_temp_model(102)

x_tess, y_tess, y_tess_err, x_evry, y_evry, y_evry_err = get_fracflux(102)

#plt.plot(x_tess, y_tess, marker="o", ls="none", color="darkorange")
#plt.show()
#exit()

fig, ax = plt.subplots(figsize=(7,5))

plt.fill_between((model_times-0.0569)*24.0*60.0, model_temps-model_lowerr,model_temps+model_upperr,color="burlywood")
plt.plot((model_times-0.0569)*24.0*60.0, model_temps, linewidth=2.5, color="darkorange")

#plt.fill_between((data_times-0.0573)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey")
plt.errorbar((data_times-0.0569)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none")

plt.xlabel("Time [min]",color="black", fontsize=16)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=16)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

plt.text(25,15300,"TIC-220433364,\n2018-11-03 2:35 UT", fontsize=13, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-26, 15800, "Clear signal", fontsize=16, color="black")

xyA=(9.46, 6800)
xyB= (14, 10283)

con = ConnectionPatch(xyA, xyB, coordsA="data", coordsB="data", axesA=ax, axesB=ax, color="grey")
ax.add_artist(con)

plt.text(14.3, 10150, "1$\sigma$ model uncertainty",fontsize=13)

xyA=(18.023, 5085)
xyB= (25,7400)

con = ConnectionPatch(xyA, xyB, coordsA="data", coordsB="data", axesA=ax, axesB=ax, color="grey")
ax.add_artist(con)

plt.text(25.6, 7300, "model temperature",fontsize=13)

plt.tight_layout()
plt.savefig("model_example_clear_signal.png")
plt.show()

#####################################################################

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(692)

model_times, model_temps, model_lowerr, model_upperr = get_temp_model(692)

x_tess, y_tess, y_tess_err, x_evry, y_evry, y_evry_err = get_fracflux(692)

CUT = 0.0408

data_temps = data_temps[data_times>CUT]
data_lowerr = data_lowerr[data_times>CUT]
data_upperr = data_upperr[data_times>CUT]
data_formal_lowerr = data_formal_lowerr[data_times>CUT]
data_formal_upperr = data_formal_upperr[data_times>CUT]
data_times = data_times[data_times>CUT]

model_temps = model_temps[model_times>CUT]
model_lowerr = model_lowerr[model_times>CUT]
model_upperr = model_upperr[model_times>CUT]
model_times = model_times[model_times>CUT]

#plt.plot(data_times, data_temps, marker="o", ls="none", color="darkorange")
#plt.show()
#exit()

"""
fig, ax = plt.subplots(figsize=(7,5))

plt.fill_between((model_times-0.0569)*24.0*60.0, model_temps-model_lowerr,model_temps+model_upperr,color="burlywood")
plt.plot((model_times-0.0569)*24.0*60.0, model_temps, linewidth=2.5, color="darkorange")

plt.errorbar((data_times-0.0569)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none")

plt.xlabel("Time [min]",color="black", fontsize=16)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=16)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

plt.text(20.7,17300,"TIC-140045538,\n2018-08-14 1:52 UT", fontsize=13, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-20, 17900, "Noisy signal", fontsize=16, color="black")

#plt.xlim(-18.8,45.4)
plt.tight_layout()

plt.savefig("model_example_noisy_signal.png")
plt.show()
"""

#####################################################################

#exit()

fig, ax = plt.subplots(figsize=(12,12))
plt.axis('off')

##### Flare 1 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(0)

data_temps = data_temps[data_times<0.12]
data_lowerr = data_lowerr[data_times<0.12]
data_upperr = data_upperr[data_times<0.12]
data_formal_lowerr = data_formal_lowerr[data_times<0.12]
data_formal_upperr = data_formal_upperr[data_times<0.12]
data_times = data_times[data_times<0.12]

ax1 = fig.add_subplot(4,2,1)

ax1.fill_between((data_times-0.0573)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax1.errorbar((data_times-0.0573)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax1.plot((data_times[data_temps<900.0]-0.0573)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

plt.xlabel("Time [min]",color="black", fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

#ax1.set_ylim([0.05, -0.45]) #Evryscope

#ax1.plot((data_times-0.0573)*24.0*60.0, y_evry_mag, marker="o",ls="none",color="cornflowerblue")

plt.text(47,39000,"TIC-294750180,\n2018-10-20 5:36 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-19, 43500, "A", fontsize=16, color="black")

##### Flare 2 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(4)

ax2 = fig.add_subplot(4,2,2)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax2.fill_between((data_times-0.0557)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax2.errorbar((data_times-0.0557)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax2.plot((data_times[data_temps<900.0]-0.0557)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax2.set_ylim([-1000, 22000]) #Evryscope


plt.text(10.2,16300,"TIC-229807000,\n2018-08-19 7:46 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-20.2, 18200, "B", fontsize=16, color="black")

##### Flare 3 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(17)

ax3 = fig.add_subplot(4,2,3)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax3.fill_between((data_times-0.0491)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax3.errorbar((data_times-0.0491)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax3.plot((data_times[data_temps<900.0]-0.0491)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax3.set_ylim([-1000, 27000]) #Evryscope

plt.text(55,20100, "TIC-339576478,\n2018-08-17 7:35 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-25, 21900, "C", fontsize=16, color="black")

##### Flare 4 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(19)

data_temps = data_temps[data_times<0.14]
data_lowerr = data_lowerr[data_times<0.14]
data_upperr = data_upperr[data_times<0.14]
data_formal_lowerr = data_formal_lowerr[data_times<0.14]
data_formal_upperr = data_formal_upperr[data_times<0.14]
data_times = data_times[data_times<0.14]

ax4 = fig.add_subplot(4,2,4)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax4.fill_between((data_times-0.0614)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax4.errorbar((data_times-0.0614)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax4.plot((data_times[data_temps<900.0]-0.0614)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax4.set_ylim([-1000, 30000]) #Evryscope

plt.text(59.5, 22500, "TIC-294750180,\n2018-08-20 7:23 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-20.5, 24600, "D", fontsize=16, color="black")

##### Flare 5 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(43)

data_temps = data_temps[(data_times<0.14)]
data_lowerr = data_lowerr[(data_times<0.14)]
data_upperr = data_upperr[(data_times<0.14)]
data_formal_lowerr = data_formal_lowerr[(data_times<0.14)]
data_formal_upperr = data_formal_upperr[(data_times<0.14)]
data_times = data_times[(data_times<0.14)]

data_lowerr = data_lowerr[(data_temps<20888)]
data_upperr = data_upperr[(data_temps<20888)]
data_formal_lowerr = data_formal_lowerr[(data_temps<20888)]
data_formal_upperr = data_formal_upperr[(data_temps<20888)]
data_times = data_times[(data_temps<20888)]
data_temps = data_temps[(data_temps<20888)]

#print data_times[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))] - data_formal_lowerr[list(data_temps).index(np.max(data_temps))]

x_arrow = (0.101386619732 - 0.0597)*24.0*60.0
y_arrow = 9781.428893
#exit()

ax5 = fig.add_subplot(4,2,5)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax5.fill_between((data_times-0.0597)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax5.errorbar((data_times-0.0597)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax5.plot((data_times[data_temps<900.0]-0.0597)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax5.plot(x_arrow+0.8, y_arrow, marker=arrow, ms=13, ls="none", color="black")

ax5.set_ylim([-1000, 20000]) #Evryscope

plt.text(55.5,14700,"TIC-339576478,\n2018-09-09 1:42 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-33.1, 16300, "E", fontsize=16, color="black")

##### Flare 6 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(482)

data_lowerr = data_lowerr[(data_temps<20408)]
data_upperr = data_upperr[(data_temps<20408)]
data_formal_lowerr = data_formal_lowerr[(data_temps<20408)]
data_formal_upperr = data_formal_upperr[(data_temps<20408)]
data_times = data_times[(data_temps<20408)]
data_temps = data_temps[(data_temps<20408)]

#print data_times[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))] - data_formal_lowerr[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))]

x_arrow = (0.074997890275 - 0.05597)*24.0*60.0
y_arrow = 11726.4448667

ax6 = fig.add_subplot(4,2,6)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax6.fill_between((data_times-0.05597)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax6.errorbar((data_times-0.05597)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax6.plot((data_times[data_temps<900.0]-0.05597)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax6.plot(x_arrow, y_arrow, marker=arrow, ms=13, ls="none", color="black")

ax6.set_ylim([-1000, 20000]) #Evryscope

plt.text(16.6,14800,"TIC-441398770,\n2018-08-12 1:57 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-23.8, 16200, "F", fontsize=16, color="black")

##### Flare 7 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(769)

data_lowerr = data_lowerr[(data_temps<38201)]
data_upperr = data_upperr[(data_temps<38201)]
data_formal_lowerr = data_formal_lowerr[(data_temps<38201)]
data_formal_upperr = data_formal_upperr[(data_temps<38201)]
data_times = data_times[(data_temps<38201)]
data_temps = data_temps[(data_temps<38201)]

print data_times[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))] - data_formal_lowerr[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))]

x_arrow = (0.0722211301 - 0.0590)*24.0*60.0
y_arrow = 15386.216975

#exit()

ax7 = fig.add_subplot(4,2,7)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax7.fill_between((data_times-0.0590)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax7.errorbar((data_times-0.0590)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax7.plot((data_times[data_temps<900.0]-0.0590)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=2, color="white", ls="none",zorder=1.0)

ax7.plot(x_arrow-0.3, y_arrow, marker=arrow, ms=13, ls="none", color="black")

ax7.set_ylim([-1000, 18000]) #Evryscope

plt.text(38.3,11500,"TIC-388857263,\n(Proxima Cen)\n2019-06-03 4:37 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-20.1, 14700, "G", fontsize=16, color="black")

##### Flare 8 ########

data_times, data_temps, data_lowerr, data_upperr, data_formal_lowerr, data_formal_upperr = get_temp_data(233)

data_temps = data_temps[data_times<0.33]
data_lowerr = data_lowerr[data_times<0.33]
data_upperr = data_upperr[data_times<0.33]
data_formal_lowerr = data_formal_lowerr[data_times<0.33]
data_formal_upperr = data_formal_upperr[data_times<0.33]
data_times = data_times[data_times<0.33]

data_lowerr = data_lowerr[(data_temps<23263)]
data_upperr = data_upperr[(data_temps<23263)]
data_formal_lowerr = data_formal_lowerr[(data_temps<23263)]
data_formal_upperr = data_formal_upperr[(data_temps<23263)]
data_times = data_times[(data_temps<23263)]
data_temps = data_temps[(data_temps<23263)]

#print data_times[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))] - data_formal_lowerr[list(data_temps).index(np.max(data_temps))],data_temps[list(data_temps).index(np.max(data_temps))]

x_arrow = (np.array([0.191664809827, 0.261108579]) - 0.2089)*24.0*60.0
#y_arrow = np.array([20319.1914232, 3132.235812])
y_arrow = np.array([15000, 3132.235812])
#exit()

ax8 = fig.add_subplot(4,2,8)

plt.xlabel("Time [min]",color="black",fontsize=13)
plt.ylabel("$T_\mathrm{Eff}$ [K]", fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(fontsize=13)

ax8.set_ylim([-1000, 16000]) #was 22,000  #Evryscope

ax8.fill_between((data_times-0.2089)*24.0*60.0, data_temps-data_lowerr,data_temps+data_upperr,color="lightgrey",zorder=0.01)
ax8.errorbar((data_times-0.2089)*24.0*60.0, data_temps, yerr=[data_formal_lowerr, data_formal_upperr], marker="o", color="black", ls="none",zorder=0.05)
ax8.plot((data_times[data_temps<900.0]-0.2089)*24.0*60.0, data_temps[data_temps<900.0], marker="o", ms=1, color="white", ls="none",zorder=1.0)

ax8.plot(x_arrow, y_arrow, marker=arrow, ms=13, ls="none", color="black")

plt.text(42,11900,"TIC-201919099,\n2018-10-05 8:23 UT", fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
plt.text(-158, 13000, "H", fontsize=16, color="black")

plt.tight_layout()
plt.savefig("blackbody_panels.png")
plt.show()
