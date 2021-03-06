import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms,
std_devs as stds)
import scipy.constants as const
#Temperaturen einlesen
T_error = 0
T_1_raw = np.genfromtxt('T_1.txt', unpack = True)
T_2_raw = np.genfromtxt('T_2.txt', unpack = True)
T_1 = unp.uarray(T_1_raw, len(T_1_raw) * [T_error])
T_2 = unp.uarray(T_2_raw, len(T_2_raw) * [T_error])
P_raw = np.genfromtxt('N_mech.txt', unpack = True)
P = unp.uarray(P_raw, len(P_raw) * [0])
P_mid = np.mean(noms(P)[1:-1])
print('P_mid', P_mid)


#umrechnung kalvin
T_1 += 273.15
T_2 += 273.15
timeinterval = 60
t = np.linspace(0, (len(T_1) - 1) * timeinterval, num = len(T_1))
#print(t)
#Drücke einlesen
p_error = 0
p_a_raw = np.genfromtxt('p_a.txt', unpack = True)
p_b_raw = np.genfromtxt('p_b.txt', unpack = True)
p_a = unp.uarray(p_a_raw, len(p_a_raw) * [p_error])
p_b = unp.uarray(p_b_raw, len(p_b_raw) * [p_error])

#umrechnung pascal
p_a += 1
p_b += 1


#in tabelle speichern
with open('temppres.tex', 'w') as f:


    f.write('\\begin{table} \n \\centering \n \\begin{tabular}{')
    f.write(5 *'S ')
    f.write('} \n \\toprule  \n')
    f.write('{Zeit in $\si{\second}$} & {$T_1$ in $\si{\kelvin}$} & {$p_b$ in $\si{\\bar}$} & {$T_1$ in $\si{\kelvin}$} & {$p_b$ in $\si{\\bar}$} \\\ \n')
    f.write('\\midrule  \n ')
    for i in range (0,18):
        f.write('{:.0f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} \\\ \n'.format( t[i] ,noms(T_1)[i], noms(p_b)[i], noms(T_2)[i], noms(p_a)[i]))
    f.write('\\bottomrule \n \\end{tabular} \n \\caption{Temperaturen und Drücke} \n \\label{tab: tempdruck} \n  \\end{table}')


p_a *= 1e05
p_b *= 1e05


#Konstanten
R = const.gas_constant
print(R)
rho_H2O = 1000
vol_1 = 3e-03
vol_2 = 3e-03
kappa = 1.14
# in g/dm^3, bei T = 0 und p = 1 bar
rho_0_CI2F2C = 5.51


#Massen
m_1 = 3
m_2 = 3
m_k = 660
c_w = 4182
c_k = 1

#verschieden Funktionen für curve_fit
def F1 (t, A, B, C):
    return A*t**2 + B*t + C

def F2(t, A, B):
    return (A)/(1 + B*t**1.5)

def F3(t, A, B, C):
    return (A*t**1.5)/(1 + B*t**1.5) + C

#curve_fit für F1, F2, F3
paramsF1_T1, covarianceF1_T1 = curve_fit(F1, t, noms(T_1), sigma=0.1)
errorsF1_T1 = np.sqrt(np.diag(covarianceF1_T1))
A_F1_T1 = ufloat(paramsF1_T1[0], errorsF1_T1[0]) * 10**6
B_F1_T1 = ufloat(paramsF1_T1[1], errorsF1_T1[1]) * 100
C_F1_T1 = ufloat(paramsF1_T1[2], errorsF1_T1[2])

x_t = np.linspace(1, 1200 , num = 1000)
plt.plot(t, noms(T_1), 'rx', label="Gemessene Werte $T_1$")
plt.plot(x_t, F1(x_t, *paramsF1_T1), 'b-', label='Regressionskurve')
plt.xlim(60, 960)
plt.xlabel('Zeit in $s$')
plt.grid(which="both")
plt.ylabel('Temperatur in $K$')
plt.legend(loc="best")
plt.savefig('plot1.pdf')

paramsF1_T2, covarianceF1_T2 = curve_fit(F1, t, noms(T_2))
errorsF1_T2 = np.sqrt(np.diag(covarianceF1_T2))
A_F1_T2 = ufloat(paramsF1_T2[0], errorsF1_T2[0]) * 10**6
B_F1_T2 = ufloat(paramsF1_T2[1], errorsF1_T2[1]) * 100
C_F1_T2 = ufloat(paramsF1_T2[2], errorsF1_T2[2])


plt.clf()
plt.plot(t, noms(T_2), 'rx', label="Gemessene Werte $T_2$")
plt.plot(x_t, F1(x_t, *paramsF1_T2), 'g-', label='Regressionskurve')
plt.xlim(60, 960)
plt.xlabel('Zeit in $s$')
plt.ylabel('Temperatur in $K$')
plt.grid(which="both")
plt.legend(loc="best")
plt.savefig('plot2_1.pdf')

paramsF1_T2, covarianceF1_T2 = curve_fit(F1, t[6:-1], noms(T_2)[6:-1])
errorsF1_T2 = np.sqrt(np.diag(covarianceF1_T2))
A_F1_T2_2 = ufloat(paramsF1_T2[0], errorsF1_T2[0]) * 10**6
B_F1_T2_2 = ufloat(paramsF1_T2[1], errorsF1_T2[1]) * 100
C_F1_T2_2 = ufloat(paramsF1_T2[2], errorsF1_T2[2])

plt.clf()
plt.plot(t, noms(T_2), 'rx', label="Gemessene Werte $T_2$")
plt.plot(x_t, F1(x_t, *paramsF1_T2), 'g-', label='Regressionskurve')
plt.ylim(275,300)
plt.xlim(t[6], t[-1])
plt.xlabel('Zeit in $s$')
plt.ylabel('Temperatur in $K$')
plt.grid(which="both")
plt.legend(loc="best")
plt.savefig('plot2_2.pdf')

#paramsF2_T2, covarianceF2_T2 = curve_fit(F2, t, noms(T_2))
#errorsF2_T2 = np.sqrt(np.diag(covarianceF2_T2))


with open('fitconst.tex', 'w') as f:


    f.write('\\begin{table} \n \\centering \n \\begin{tabular}{')
    f.write(4 *'S ')
    f.write('} \n \\toprule  \n')
    f.write('{Funktion} & {$A$} & {$B$} & {$C$} \\\ \n')
    f.write('\\midrule  \n ')
    f.write('$T_1$ & $\\num{{{:.2f} \pm {:.2f}}}$ & $\\num{{{:.2f}\pm {:.2f}}}$ & $\\num{{{:.2f} \pm {:.2f}}}$ \\\ \n'.format(A_F1_T1.n, A_F1_T1.s, B_F1_T1.n, B_F1_T1.s, C_F1_T1.n, C_F1_T1.s))
    f.write('$T_2$ & $\\num{{{:.2f} \pm {:.2f}}}$ & $\\num{{{:.2f} \pm {:.2f}}}$ & $\\num{{{:.2f} \pm {:.2f}}}$ \\\ \n'.format(A_F1_T2.n, A_F1_T2.s, B_F1_T2.n, B_F1_T2.s, C_F1_T2.n, C_F1_T2.s))
    f.write('$T_2*$ & $\\num{{{:.2f} \pm {:.2f}}}$ & $\\num{{{:.2f}\pm {:.2f}}}$ & $\\num{{{:.2f} \pm {:.2f}}}$ \\\ \n'.format(A_F1_T2_2.n, A_F1_T2_2.s, B_F1_T2_2.n, B_F1_T2_2.s, C_F1_T2_2.n, C_F1_T2_2.s))
    f.write('\\bottomrule \n \\end{tabular} \n \\caption{Regressionsparameter} \n \\label{tab: regress} \n  \\end{table}')



#paramsF3, covarianceF3 = curve_fit(F3, t, noms(T_1))
#errorsF3 = np.sqrt(np.diag(covarianceF3))



A_F1_T1 /= (10**6)
A_F1_T2_2 /= (10**6)
B_F1_T1 /= 100
B_F1_T2_2 /= 100

#Differentialquotient
def dT_dt(t, A, B):
    return 2*A*t + B
#für 60, 120, 180, 240
dT1_dt = unp.uarray(np.zeros(18), np.zeros(18))
for i in range(0,18):
    dT1_dt[i] = dT_dt(t[i], A_F1_T1, B_F1_T1)

dT2_dt = unp.uarray(np.zeros(18), np.zeros(18))
for i in range(0,18):
    dT2_dt[i] = dT_dt(t[i], A_F1_T2_2, B_F1_T2_2)

dQ1_dt =  unp.uarray(np.zeros(18), np.zeros(18))
for i in range(0,18):
    dQ1_dt[i] = dT1_dt[i] * (m_1 * c_w + m_k * c_k)

dQ2_dt =  unp.uarray(np.zeros(18), np.zeros(18))
for i in range(0,18):
    dQ2_dt[i] = dT2_dt[i] * (m_2 * c_w + m_k * c_k)

#Berechnung von L
#print(len(noms(T_1)))
def Gaskurve(T, A, B):
    return A * np.exp(B/T)
L_params, L_cov = curve_fit(Gaskurve, noms(T_1), noms(p_b))
errors_L = np.sqrt(np.diag(L_cov))
print ('-l_R:', L_params[1], 'pm', errors_L[1])
uB = ufloat(L_params[1],errors_L[1] )
L = - uB * R

x_t = np.linspace(1, 1000 , 1000)
plt.clf()
plt.xlim(1/T_1[0].n, 1/T_1[-1].n)
plt.ylim(1e05, 1e07)
plt.plot(1/noms(T_1)[1:-1], noms(p_b)[1:-1],'rx', label="Gemessene Werte $p_{b}$")
plt.plot(1/x_t, Gaskurve(x_t, *L_params), 'b-', label = "Regressionsgerade")
plt.yscale("log")
plt.ylabel('$p_b$ in $Pa$')
plt.xlabel('$1/T_1$ in $K^{-1}$')
plt.grid(which="both")
plt.legend(loc="best")
plt.savefig('plot3.pdf')


#Massendurchsatz
dm_dt = - dQ2_dt / L
print('dm: ' , dm_dt*120)
print(p_a)
#umrechnung in kg/s
dm_dt *= 0.12


#mechanische Arbeit
#ideale Gasgleichung pV = nRT equals p = nRT/V
T_0 = 273.15
const = ((T_0 * rho_0_CI2F2C)/ 1e05)
def rho(p, T):
    return const * (p/T)

N_mech = unp.uarray(np.zeros(18), np.zeros(18))
for i in range(0,18):
    N_mech[i] =  1/(kappa-1) * (p_b[i] * (p_a[i]/p_b[i])**(1/kappa) - p_a[i] ) * dm_dt[i]/(rho(p_a[i], T_2[i]))
print('N_mech: ', N_mech)

#Wirkungskoeffizient

nu_ideal = T_1 / (T_1 - T_2)
print(len(noms(nu_ideal)))
nu_real = dQ1_dt / P
print(nu_real)
#T_1 += 273.15
#T_2 += 273.15




with open('differenz.tex', 'w') as f:

    f.write('\\begin{table} \n \\centering \n \\begin{tabular}{')
    f.write(5 *'S ')
    f.write('} \n \\toprule  \n')
    f.write('{Zeit in $\si{\second}$} & {$\\frac{dT_1}{dt}$ in $\si{\kelvin \per \second}$} & {$\\frac{dT_2}{dt}$ in $\si{\kelvin \per \second}$} & {$\\nu_{real}$}& {$\\nu_{ideal}$} \\\ \n')
    f.write('\\midrule  \n ')
    for i in range (0,18):
        f.write('{:.0f} & $\\num{{ {:.4f} \pm {:.4f} }}$ & $\\num{{ {:.4f} \pm {:.4f} }}$ & $\\num{{ {:.2f} \pm {:.2f} }}$ & $\\num{{ {:.2f} }}$\\\ \n'.format(t[i] ,noms(dT1_dt)[i], stds(dT1_dt)[i], noms(dT2_dt)[i], stds(dT2_dt)[i], noms(nu_real)[i], stds(nu_real)[i], noms(nu_ideal)[i]))
    f.write('\\bottomrule \n \\end{tabular} \n \\caption{Differenzenquotienten und reale Güteziffer} \n \\label{tab: dTdt} \n  \\end{table}')


#umrechnen in g/s
dm_dt *= 1000
with open('massendurchsatz.tex', 'w') as f:

    f.write('\\begin{table} \n \\centering \n \\begin{tabular}{')
    f.write(3*'S ')
    f.write('} \n \\toprule  \n')
    f.write('{Zeit in $\si{\second}$} & {$\\frac{dm}{dt}$ in $\si{\gram \per \second}$} & {$N_{mech}$ in $\si{\watt}$}  \\\ \n')
    f.write('\\midrule  \n ')
    for i in range (0,18):
        f.write('{:.0f}  & $\\num{{ {:.2f} \pm {:.2f} }}$ & $\\num{{ {:.2f} \pm {:.2f} }}$ \\\ \n'.format(t[i] ,noms(dm_dt)[i], stds(dm_dt)[i], noms(N_mech)[i], stds(N_mech)[i]))
    f.write('\\bottomrule \n \\end{tabular} \n \\caption{Massendurchsatz und Kompressorleistung} \n \\label{tab: dmdtNmech} \n  \\end{table}')
