import numpy as np
import uncertainties.unumpy as unp
from uncertainties import ufloat
import math
import latex
from uncertainties.umath import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from pint import UnitRegistry
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
u = UnitRegistry()
Q_ = u.Quantity

#Apparaturkonstanten
L = Q_(1.75e-3, 'henry')
C = Q_(22.0e-9, 'farad')
C_1 = C
C_2 = Q_(9.39e-9, 'farad')
theta = np.linspace(-0.2 * np.pi, np.pi, 1000)

#Dispersionskurven
#gleiche kondensatoren
def omega(theta):
    return np.sqrt( (2 / (L.magnitude * C.magnitude)) * (1 - np.cos(theta) ) )

def nu(omega):
    return 1/(2*np.pi) * omega


#unterschiedliche Kondensatoren
def omega1(theta):
    return np.sqrt( 1/ L.magnitude * (1/C_1.magnitude + 1/C_2.magnitude) + 1/L.magnitude*np.sqrt( (1/C_1.magnitude + 1/C_2.magnitude)**2 - 4*np.sin(theta)**2/(C_1.magnitude*C_2.magnitude) ))

def omega2(theta):
    return np.sqrt( 1/ L.magnitude * (1/C_1.magnitude + 1/C_2.magnitude) - 1/L.magnitude*np.sqrt( (1/C_1.magnitude + 1/C_2.magnitude)**2 - 4*np.sin(theta)**2/(C_1.magnitude*C_2.magnitude) ))

def f(x, A, B, C):
    return A * np.exp(B * x) + C

def f_cos(x, A, B, C, D):
    return A * np.cos(B*x + C) + D

#Phasengeschwindigkeit
def v_phase(nus):
    return 2 * np.pi * nus / ( np.arccos(1 - 0.5 * (2 * np.pi * nus)**2 * L.magnitude * C.magnitude) )

#Gruppengeschwindigkeit
def v_gruppe(nus):
    return np.sqrt( 1/(L.magnitude * C.magnitude) * (1 - 0.25 * L.magnitude * C.magnitude * (2*np.pi*nus))    )

def impedanz_plot(omega):
    return np.sqrt(L.magnitude / C.magnitude) * 1/np.sqrt( 1 - 0.25 * omega**2 * L.magnitude * C.magnitude )

def impedanz(omega):
    return np.sqrt(L / C) * 1/np.sqrt( 1 - 0.25 * omega**2 * L * C )
#variabel_1,variabel_2=np.genfromtxt('name.txt',unpack=True)


#Einlesen der Messwerte
eigenfrequenzen_a_LC = np.genfromtxt('eigenfrequenzen_a_LC.txt', unpack=True)
range_lin = np.linspace(1, len(eigenfrequenzen_a_LC), 12)
Phasenverschiebung_pro_glied_LC = np.pi * range_lin / 16
latex.Latexdocument('tabs/eigenfrequenzen_dispersion_LC.tex').tabular([Phasenverschiebung_pro_glied_LC, eigenfrequenzen_a_LC],
'{$\\theta$} & {$\\nu$ in $\si{\hertz}$}', [1, 0],
caption = 'LC-Kette, Gemessene Frequenzen mit zugeordnetem Phasenversatz pro Glied', label = 'tab: dispersion_LC')


eigenfrequenzen_a_LC1C2 = np.genfromtxt('eigenfrequenzen_a_LC1C2.txt', unpack=True)
range_lin = np.linspace(1, len(eigenfrequenzen_a_LC1C2), len(eigenfrequenzen_a_LC1C2))
Phasenverschiebung_pro_glied_LC1C2 = np.pi * range_lin / 16
for i in range(0, len(Phasenverschiebung_pro_glied_LC1C2)):
    if (Phasenverschiebung_pro_glied_LC1C2[i] > np.pi/2):
        Phasenverschiebung_pro_glied_LC1C2[i] -= 2*(Phasenverschiebung_pro_glied_LC1C2[i] - np.pi/2)
latex.Latexdocument('tabs/eigenfrequenzen_dispersion_LC1C2.tex').tabular([Phasenverschiebung_pro_glied_LC1C2, eigenfrequenzen_a_LC1C2],
'{$\\theta$} & {$\\nu$ in $\si{\hertz}$}', [1, 0],
caption = '$LC_1C_2$-Kette, Gemessene Frequenzen mit zugeordnetem Phasenversatz pro Glied', label = 'tab: dispersion_LC1C2')

frequenzen_sweep_LC = np.genfromtxt('frequenz_sweep_LC.txt', unpack = True)
x_range_LC = ((np.linspace(1, len(frequenzen_sweep_LC), len(frequenzen_sweep_LC))-1) * 4)[::-1]
params_LC, covariance_LC = curve_fit(f, x_range_LC, frequenzen_sweep_LC)
errors_LC = np.sqrt(np.diag(covariance_LC))
A_param = ufloat(params_LC[0], errors_LC[0])
B_param = ufloat(params_LC[1], errors_LC[1])
C_param = ufloat(params_LC[2], errors_LC[2])
print('Parameter des Fits LC, A= ', A_param, ' B= ', B_param, ' C= ', C_param)
latex.Latexdocument('tabs/sweep_LC.tex').tabular([x_range_LC[::-1], frequenzen_sweep_LC[::-1]],
'{x in $\si{\centi\meter}$} & {Frequenzen in $\si{\hertz}$}', [0, 0],
caption = 'LC-Kette, Referenzpunkte für den Frequenzsweep', label = 'tab: sweep_LC')
def frequenz_sweep_LC(x):
    return A_param * exp(B_param * x) + C_param


frequenzen_sweep_LC1C2 = np.genfromtxt('frequenz_sweep_LC1C2.txt', unpack = True)
x_range_LC1C2 = ((np.linspace(1, len(frequenzen_sweep_LC1C2), len(frequenzen_sweep_LC1C2))-1) * 4)[::-1]
print(x_range_LC1C2)
params_LC1C2, covariance_LC1C2 = curve_fit(f, x_range_LC1C2, frequenzen_sweep_LC1C2)
errors_LC1C2 = np.sqrt(np.diag(covariance_LC1C2))
A_param_LC1C2 = ufloat(params_LC1C2[0], errors_LC1C2[0])
B_param_LC1C2 = ufloat(params_LC1C2[1], errors_LC1C2[1])
C_param_LC1C2 = ufloat(params_LC1C2[2], errors_LC1C2[2])
latex.Latexdocument('tabs/sweep_LC1C2.tex').tabular([x_range_LC1C2[::-1], frequenzen_sweep_LC1C2[::-1]],
'{x in $\si{\centi\meter}$} & {Frequenzen in $\si{\hertz}$}', [0, 0],
caption = '$LC_1C_2$-Kette, Referenzpunkte für den Frequenzsweep', label = 'tab: sweep_LC1C2')

def frequenz_sweep_LC1C2(x):
    return A_param_LC1C2 * exp(B_param_LC1C2 * x) + C_param_LC1C2

print('Parameter des Fits LC1C2, A= ', A_param_LC1C2, ' B= ', B_param_LC1C2, ' C= ', C_param_LC1C2)
#Berechnungen
#Theoretische Werte
omega_G_LC = 2*np.sqrt(1 / (L.magnitude * C.magnitude))
print('Theoretische Grenzfrequenz LC: ', nu(omega_G_LC))

omega_G_u_LC1C2 = np.sqrt(2 / (L * C_1))
omega_G_o_LC1C2 = np.sqrt(2 / (L * C_2))
omega_G_korrektur = np.sqrt(2/L * (C_1 + C_2)/(C_1 * C_2))
print('Theoretische Grenzfrequenz unten LC1C2: ', nu(omega_G_u_LC1C2))
print('Theoretische Grenzfrequenz oben LC1C2: ', nu(omega_G_o_LC1C2))
print('Theoretische Grenzfrequenz Korrektur LC1C2: ', nu(omega_G_korrektur))


#Berechnungen
distance_f_g_LC = ufloat(10.2, 0.5)
distance_f_g_u_LC1C2 = ufloat(6.5, 0.5)
distance_f_g_o_LC1C2 = ufloat(10.7, 0.5)
print('Aus Sweep Methode bestimmte Grenzfrequenz LC: ', frequenz_sweep_LC(distance_f_g_LC))
print('Prozentuale Abweichung: ', (frequenz_sweep_LC(distance_f_g_LC))/nu(omega_G_LC) - 1)
print('Aus Sweep Methode bestimmte Grenzfrequenz unten LC1C2: ', frequenz_sweep_LC1C2(distance_f_g_u_LC1C2))
print('Prozentuale Abweichung: ', (frequenz_sweep_LC1C2(distance_f_g_u_LC1C2))/nu(omega_G_u_LC1C2.magnitude) - 1)
print('Aus Sweep Methode bestimmte Grenzfrequenz oben LC1C2: ', frequenz_sweep_LC1C2(distance_f_g_o_LC1C2))
print('Prozentuale Abweichung: ', (frequenz_sweep_LC1C2(distance_f_g_o_LC1C2))/nu(omega_G_o_LC1C2.magnitude) - 1)
print('Aus Sweep Methode bestimmte Grenzfrequenz Korrektur LC1C2: ', frequenz_sweep_LC1C2(ufloat(14, 0.5)))
print('Prozentuale Abweichung: ', (frequenz_sweep_LC1C2(ufloat(14, 0.5))/nu(omega_G_korrektur).magnitude) - 1)

#Phasengeschwindigkeit
eigenfrequenzen_offen = np.genfromtxt('eigenfrequenzen_offen.txt', unpack=True)
range_lin = np.linspace(1, len(eigenfrequenzen_offen), len(eigenfrequenzen_offen))
Phasenverschiebung_offen = np.pi * range_lin / 16
Phasengeschwindigkeit = 2 * np.pi * eigenfrequenzen_offen/Phasenverschiebung_offen
latex.Latexdocument('tabs/v_phase_LC.tex').tabular([Phasenverschiebung_offen, eigenfrequenzen_offen, Phasengeschwindigkeit],
'{Phasenverschiebung $\\theta$} & {Frequenzen in $\si{\hertz}$} & {$v_{ph}$ in $\si{\meter\per\second}$}', [0, 0, 0],
caption = 'Eigenfrequenzen der LC Kette und berechnete Phasengeschwindigkeiten', label = 'tab: v_phase')


#stehende Wellen
#nu1 = 5092 Hz
messpunkte = np.linspace(1, 17, 17)
print(messpunkte)
spannungsverlauf_nu1 = np.genfromtxt('spannung_nu1.txt', unpack=True)
#latex.Latexdocument('tabs/spannung_nu1.tex').tabular([messpunkte, spannungsverlauf_nu1],
#'{Messpunkte} & {Spannung in $\si{\\volt}$}', [0, 2],
#caption = 'Spannungsverlauf unter der Eigenfrequenz $\\nu_1$', label = 'tab: U_nu1')
spannungsverlauf_nu2 = np.genfromtxt('spannung_nu2.txt', unpack=True)
spannungsverlauf_geschlossen = np.genfromtxt('spannung_geschlossen.txt', unpack=True)
latex.Latexdocument('tabs/spannung_nu1.tex').tabular([messpunkte, spannungsverlauf_nu1, spannungsverlauf_nu2, spannungsverlauf_geschlossen],
'{Messpunkte} & {$U_{\\nu_1}$ in $\si{\\volt}$} & {$U_{\\nu_2}$ in $\si{\\volt}$} & {$U_{G}$ in $\si{\\volt}$ }', [0, 2, 2, 2],
caption = 'Spannungsverläufe $U_{\\nu_1}$ und $U_{\\nu_2}$ unter den Eigenfrequenzen $\\nu_1$ und $\\nu_2$ bei der offenen LC-Kette; Spannungsverlauf $U_{G}$ der geschlossenen LC-Kette', label = 'tab: U_nu12')
#params_nu1, covariance_nu1 = curve_fit(f_cos, messpunkte, spannungsverlauf_nu1)
#params_nu2, covariance_nu2 = curve_fit(f_cos, messpunkte, spannungsverlauf_nu2)
spannungsverlauf_geschlossen = np.genfromtxt('spannung_geschlossen.txt', unpack=True)


#Theorieplots der Disperionsrelation
plt.plot(theta, nu(omega(theta))/1000, label='Dispersionskurve $\\nu(\\theta)$' )
plt.plot(Phasenverschiebung_pro_glied_LC, eigenfrequenzen_a_LC/1000, 'rx', label = 'Messdaten')
plt.plot(theta, np.ones(len(theta))*nu(omega_G_LC)/1000, 'b--', label='Grenzfrequenz $\\nu_G$' )
print(nu(omega_G_LC))
plt.ylabel('Frequenz $\\nu$ in kHz')
plt.xlabel('Phasenverschiebung pro Glied $\\theta$')
plt.xlim(0, theta[-1])
plt.xticks([0, np.pi/8, np.pi / 4, 3*np.pi/8 , np.pi/2, 5 * np.pi/8, 3*np.pi/4, 7*np.pi/8, np.pi],
           [r"$0$", r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$", r"$\frac{3\pi}{8}$", r"$\frac{\pi}{2}$",
            r"$\frac{5\pi}{8}$", r"$\frac{3\pi}{4}$", r"$\frac{7\pi}{8}$", r"$\pi$"], fontsize = 16)
plt.legend(loc='best')
plt.grid()
plt.savefig('plots/dispersion.pdf')

#stehende Wellen
plt.clf()
m_range = np.linspace(0, 18, 100)
plt.plot(messpunkte, spannungsverlauf_nu1, 'bo', label='Messwerte')
#plt.plot(m_range, f_cos(m_range, *params_nu1), 'b-')
plt.grid()
plt.legend(loc='best')
plt.xlabel('Messpunkte')
plt.ylabel('Spannung in V')
plt.xlim(0.8, 17.2)
plt.xticks(messpunkte, [int(i) for i in messpunkte], fontsize = 10)
plt.ylim(0, 2)
plt.savefig('plots/spannungsverlauf_nu1.pdf')

plt.clf()
plt.plot(messpunkte, spannungsverlauf_nu2, 'bo', label='Messwerte')
#plt.plot(m_range, f_cos(m_range, *params_nu2), 'b-')
plt.grid()
plt.xlabel('Messpunkte')
plt.ylabel('Spannung in V')
plt.xticks(messpunkte, [int(i) for i in messpunkte], fontsize = 10)
plt.xlim(0.8, 17.2)
plt.ylim(-0.1, 2.5)
plt.legend(loc='best')
plt.savefig('plots/spannungsverlauf_nu2.pdf')

plt.clf()
plt.plot(messpunkte, spannungsverlauf_geschlossen, 'bo', label='Messwerte')
#plt.plot(m_range, f_cos(m_range, *params_nu2), 'b-')
plt.grid()
plt.xlabel('Messpunkte')
plt.ylabel('Spannung in V')
plt.xticks(messpunkte, [int(i) for i in messpunkte], fontsize = 10)
plt.xlim(0.8, 17.2)
plt.ylim(0.35, 0.5)
plt.legend(loc='best')
plt.savefig('plots/spannungsverlauf_geschlossen.pdf')


plt.clf()
plt.plot(theta, nu( omega1(theta) )/1000, label='$\\nu_1(\\theta)$' )
plt.plot(theta, nu( omega2(theta) )/1000, label='$\\nu_2(\\theta)$' )
plt.plot(Phasenverschiebung_pro_glied_LC1C2, eigenfrequenzen_a_LC1C2/1000, 'rx', label='Messwerte')
plt.plot(theta, np.ones(len(theta))*nu(omega_G_u_LC1C2)/1000, 'g--', label= 'Grenzfequenzen')
plt.plot(theta, np.ones(len(theta))*nu(omega_G_o_LC1C2)/1000, 'g--')
plt.plot(theta, np.ones(len(theta))*nu(omega_G_korrektur)/1000, 'g--')
plt.ylabel('Frequenz $\\nu$ in kHz')
plt.xlabel('Phasenverschiebung pro Glied $\\theta$')
plt.xlim(0, np.pi/2 + 0.02)
plt.xticks([0, np.pi/8, np.pi / 4, 3*np.pi/8 , np.pi/2],
           [r"$0$", r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$", r"$\frac{3\pi}{8}$", r"$\frac{\pi}{2}$"], fontsize = 16)
plt.legend(loc='best')
plt.grid()
plt.savefig('plots/dispersion1.pdf')


plt.clf()
plt.plot(nu(omega(theta))/1000, v_phase(nu(omega(theta)))/1000, label='$v_{Ph}(\\nu)$' )
plt.plot(eigenfrequenzen_offen/1000, 2 * np.pi * eigenfrequenzen_offen/Phasenverschiebung_offen/1000, 'rx', label='Messwerte')
plt.ylabel('Phasengeschwindigkeit $v$ in rad/ms')
plt.xlabel('Frequenz $\\nu$ in kHz')
plt.xlim((eigenfrequenzen_offen[0]-1000)/1000, (eigenfrequenzen_offen[-1]+1000)/1000)
plt.legend(loc='best')
plt.grid()
plt.savefig('plots/v_phase.pdf')


#plt.clf()
#plt.plot( omega(theta), impedanz_plot(omega(theta)), label='$Z(\omega)$' )
#plt.ylabel('Impedanz $Z$')
#plt.xlabel('Kreisfrequenz $\omega$ in $1/s$')
#plt.xlim(omega(theta)[0], omega(theta)[-1])
#plt.legend(loc='best')
#plt.grid()
#plt.savefig('plots/impedanz.pdf')

x_lim = np.linspace(x_range_LC[0]+2, x_range_LC[-1]-2, 100)
plt.clf()
plt.plot(x_range_LC, frequenzen_sweep_LC/1000, 'rx', label='Messwerte')
plt.plot(x_lim, f(x_lim, *params_LC)/1000, 'b-', label='Fit $\\nu(x)$')
plt.xlabel('Abstand zum Nullpunkt in cm')
plt.ylabel('Frequenz $\\nu$ in kHz')
plt.grid()
plt.xlim(x_range_LC[-1]-2, x_range_LC[0]+2)
plt.legend(loc='best')
plt.savefig('plots/frequenzsweep_LC.pdf')

x_lim = np.linspace(x_range_LC1C2[0]+2, x_range_LC1C2[-1]-2, 100)
plt.clf()
plt.plot(x_range_LC1C2, frequenzen_sweep_LC1C2/1000, 'rx', label='Messwerte')
plt.plot(x_lim, f(x_lim, *params_LC1C2)/1000, 'b-', label='Fit $\\nu(x)$')
plt.xlabel('Abstand zum Nullpunkt in cm')
plt.ylabel('Frequenz $\\nu$ in Hz')
plt.xlim(x_range_LC1C2[-1]-2, x_range_LC1C2[0]+2)
plt.grid()
plt.legend(loc='best')
plt.savefig('plots/frequenzsweep_LC1C2.pdf')
