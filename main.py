import pandas as pd
import numpy as np
import itertools
import math

from flask import Flask, render_template, request
app = Flask(__name__)

@app.after_request
def add_header(xd):
    xd.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    xd.headers["Pragma"] = "no-cache"
    xd.headers["Expires"] = "0"
    xd.headers['Cache-Control'] = 'public, max-age=0'
    return xd


@app.route('/')
def home():

    datos = pd.DataFrame()
    demanda = [100, 200, 300, 400, 500, 600]
    probabilidad = [0.15, 0.25, 0.18, 0.22, 0.13, 0.07]
    datos["Demanda"] = demanda
    datos["Probabilidad"] = probabilidad
    datos
    data = datos.to_html(classes="table table-hover table-striped",
                      justify="justify-all", border=0)
    return render_template('home.html', data=data)

@app.route("/resolucion")
def resolucion():
    datos = pd.DataFrame()
    demanda = [100, 200, 300, 400, 500, 600]
    probabilidad = [0.15, 0.25, 0.18, 0.22, 0.13, 0.07]
    datos["Demanda"] = demanda
    datos["Probabilidad"] = probabilidad
    # Cálculo la suma acumulativa de las probabilidades
    a0 = np.cumsum(probabilidad)
    a0
    datos["Acumulada"] = a0
    datos
    data2 = datos.to_html(classes="table table-hover table-striped",
                         justify="justify-all", border=0)
    # Min y Max
    datos['Min'] = datos["Acumulada"]
    datos['Max'] = datos["Acumulada"]
    lis = datos["Min"].values
    lis2 = datos['Max'].values
    lis[0] = 0
    for i in range(1, 6):
        lis[i] = lis2[i - 1]
    datos['Min'] = lis
    datos
    data3 = datos.to_html(classes="table table-hover table-striped",
                         justify="justify-all", border=0)

    # Números aleatorios
    aleatorio = [0.11, 0.44, 0.90, 0.52, 0.00, 0.54, 0.56, 0.66, 0.52, 0.46, 0.24, 0.31, 0.49, 0.03, 0.50, 0.65, 0.80,
                 0.74, 0.32, 0.66]
    # simulacion=[100,300,500,300,100,300,300,400,300,300,200,200,300,100,300,400,500,400,200,400]
    nueva = pd.DataFrame()
    nueva["Aleatorio"] = aleatorio
    nueva

    nuevata= nueva.to_html(classes="table table-hover table-striped",
                         justify="justify-all", border=0)

    # Otra sección
    def busqueda(arrmin, arrmax, valor):
        # print(valor)
        for i in range(len(arrmin)):
            # print(arrmin[i],arrmax[i])
            if valor >= arrmin[i] and valor <= arrmax[i]:
                return i
        return -1

    n = len(nueva)
    xpos = nueva['Aleatorio']
    posi = [0] * n
    for j in range(n):
        val = xpos[j]
        pos = busqueda(datos['Min'].values, datos['Max'].values, val)
        posi[j] = pos
    posi

    simula = []
    a = 0
    ind = [1 + i for i in range(len(datos))]
    datos["Indice"] = ind
    for i in range(n):
        sim = datos.loc[datos["Indice"] == posi[i] + 1]
        simu = sim.filter(["Demanda"]).values
        iterator = itertools.chain(*simu)
        for item in iterator:
            a = item
        simula.append(round(a, 2))
    simula
    nueva["Simulación"] = pd.DataFrame(simula)
    nueva

    data4 = nueva.to_html(classes="table table-hover table-striped",
                         justify="justify-all", border=0)
    
    import statistics
    total9=sum(simula)

    mean9 = statistics.mean(simula)
    

    return render_template('resolucion.html', data2=data2, data3=data3, nuevata=nuevata, data4=data4, data9=total9, data10=mean9)




if __name__ == "__main__":
    app.run(port=5000, debug=True)