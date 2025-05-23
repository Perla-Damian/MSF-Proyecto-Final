"""
Proyecto Final: Sistema Endocrino: Hipotiroidismo


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno: Damian Arroyo Perla Guadalupe
Número de control: 21212150
Correo institucional: l21212150@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot


# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,30,1E-3,6,3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 =np.sin(m.pi/2*t) #Respiración Normal


def sys_endocrino (R3, C2):
    R1,R2,L1, C1 = 33E3, 33E3,560E-3,10E-6
    alpha3 = C2 * R1 * C1 * L1
    alpha2 = C2 * R1 * R2 * C1 + C2 * R1 * R3 * C1 + C2 * L1
    alpha1 = C1 * R1 + C2 * R1 + C2 * R2 + C2 * R3
    alpha0 = 1
    num = [alpha0]
    den = [alpha3, alpha2, alpha1, alpha0]
    sys = ctrl.tf(num,den)
    return sys

#Función de transferencia: Individuo Saludable [control]
R3, C2 = 10E3,1E-6
sysS = sys_endocrino(R3, C2)
print('Individuo Sano [control]:')
print(sysS)

#Función de transferencia: Individuo Enfermo [caso]
R3, C2 = 33E3,10E-6
sysE = sys_endocrino(R3, C2)
print('Individuo Enfermo [caso]:')
print(sysE)

rosa = [255/255, 32/255, 78/255]
rosamasrosa = [160/255, 21/255, 62/255]
morado = [93/255, 14/255, 65/255]
azul = [0/255, 34/255, 77/255]

def plotsignals (u, sysS, sysE, sysPID, signal):
    fig = plt.figure()
    ts, Vs = ctrl.forced_response(sysS, t, u, x0)
    plt.plot(t, Vs, '-', color = rosa, label = '$V_s(t): Control$')
    ts, Ve = ctrl.forced_response(sysE, t, u, x0)
    plt.plot(t, Ve, '-', color = morado, label = '$V_s(t): Hipotiroidismo$')
    ts, pid = ctrl.forced_response(sysPID, t, Vs, x0)
    plt.plot(t, pid, ':', linewidth = 3, color = azul, label = '$V_s(t):Tratamiento$')

    plt.grid(False)
    plt.xlim(0, 30)
    plt.ylim(-1, 1)
    plt.xticks(np.arange(0, 31, 2))
    plt.yticks(np.arange(-1, 1.25, 0.25))
    plt.xlabel('$t$ [s]', fontsize = 12)
    plt.ylabel('$Vs(t)$ [V]', fontsize = 12)
    plt.legend(bbox_to_anchor = (0.5, -0.3), loc = 'center',
               ncol = 4, fontsize = 8, frameon = False)
    plt.show()
    fig.set_size_inches(w, h)
    fig.tight_layout()
    namepdf = 'python_' + signal + '.pdf'
    fig.savefig(namepdf, bbox_inches = 'tight')


def tratamiento(Cr, Re, Rr, Ce, sysE):
    numPID = [Re*Rr*Ce*Cr, Re*Ce + Rr*Cr, 1]
    denPID = [Re*Cr, 0]
    PID = ctrl.tf(numPID, denPID)
    X = ctrl.series(PID, sysE)
    sysPID = ctrl.feedback(X, 1, sign = -1)
    return sysPID

# Sistema de control en lazo cerrado
kP, kI, kD, Cr = 913.4762, 3145.0167,40.9623, 1E-6
Re = 1/(kI*Cr)
Rr = kP*Re
Ce = kD/Rr
sysPID = tratamiento(Cr, Re, Rr, Ce, sysE)
plotsignals(u1, sysS, sysE, sysPID, 'normal')

# Mostrar valores de los componentes
print('Componentes físicos del controlador:')
print('Re =', Re, 'Ω')
print('Rr =', Rr, 'Ω')
print('Cr =', Cr, 'F')
print('Ce =', Ce, 'F')
          