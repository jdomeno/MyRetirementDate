import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class ModeloFinanciero:
    def __init__(self, salario_inicial, patrimonio_inicial, anio_inicial,
                 prestamo_inicial, alquiler1_inicial, alquiler2_inicial):
        self.salario_inicial = salario_inicial
        self.patrimonio_inicial = patrimonio_inicial
        self.anio_inicial = anio_inicial
        self.prestamo_inicial = prestamo_inicial
        self.alquiler1_inicial = alquiler1_inicial
        self.alquiler2_inicial = alquiler2_inicial

    # -------------------------------
    # Probabilidad de éxito al jubilarse
    # -------------------------------
    def curva_probabilidad_retiro(self, salario_inicial, ahorro_inicial, gasto_anual, ahorro_deseado,
                                  pension_anual=12000, edad_actual=48, edad_max=100,
                                  edad_retiro_deseada=65, inflacion_media=0.02, rentabilidad_media=0.04,
                                  simulaciones=500, umbral=0.9):
        edades = list(range(edad_actual, edad_max + 1))
        probabilidades = []

        for edad_retiro in edades:
            exitos = 0
            for _ in range(simulaciones):
                inflacion = np.random.normal(inflacion_media, 0.005)
                rentabilidad = np.random.normal(rentabilidad_media, 0.01)
                salarios = salario_inicial
                pensiones = pension_anual
                alquileres = (self.alquiler1_inicial + self.alquiler2_inicial)
                gastos = gasto_anual + ahorro_deseado
                ahorros = ahorro_inicial + ahorro_deseado

                for edad in range(edad_retiro, edad_max + 1):
                    # Salario hasta la edad de retiro
                    if edad < edad_retiro:
                        salarios = salarios * (1 + inflacion)
                        pensiones = 0
                    # Pensión a partir de los 65
                    if edad >= 65:
                        salarios = 0
                        pensiones = pensiones * (1 + inflacion)
           
                    alquileres =  alquileres * (1 + inflacion)   # Alquileres siempre
                    ingresos = salarios + pensiones + alquileres
                    gastos = gastos * (1 + inflacion) 
                    ahorros = ahorros * (1 + rentabilidad) + ingresos - gastos

                    if ahorros < 0:
                        break
                else:
                    exitos += 1

            prob_exito = exitos / simulaciones
            probabilidades.append(prob_exito)

        edad_optima = None
        for e, p in zip(edades, probabilidades):
            if p >= umbral:
                edad_optima = e
                break

        return edades, probabilidades, edad_optima

    def graficar_curva_retiro(self, edades, probabilidades, edad_optima=None):
        plt.figure(figsize=(10,6))
        plt.plot(edades, probabilidades, marker="o", label="Probabilidad de éxito")
        if edad_optima:
            plt.axvline(edad_optima, color="green", linestyle="--", label=f"Edad óptima {edad_optima}")
        plt.title("Probabilidad de éxito financiero según edad de retiro")
        plt.xlabel("Edad de retiro")
        plt.ylabel("Probabilidad de éxito")
        plt.grid(True)
        plt.ylim(0, 1)
        plt.legend()
        plt.show()

    # -------------------------------
    # Evolución patrimonial año a año     #######  OK!!!!!!!!!!!!!!!!
    # -------------------------------
    def simular_evolucion_patrimonial(self, salario_inicial, ahorro_inicial, gasto_anual, ahorro_deseado,
                                   pension_anual=15000, edad_actual=48, edad_max=100,
                                   edad_retiro_deseada=65, inflacion_media=0.02, rentabilidad_media=0.04):
        inflacion = inflacion_media
        rentabilidad = rentabilidad_media
        datos = []

        salarios = salario_inicial

        alquileres = (self.alquiler1_inicial + self.alquiler2_inicial)
        gastos = gasto_anual + ahorro_deseado
        ahorros = ahorro_inicial + ahorro_deseado
        
        for edad in range(edad_actual, edad_max + 1):
            
            # Salario hasta la edad de retiro
            if edad < edad_retiro_deseada:
                salarios = salarios * (1 + inflacion) 
                pensiones = 0
            elif edad == edad_retiro_deseada:
                salarios = 0 
            
            # Pensión a partir de los 65
            if edad == 65:
                pensiones = pension_anual
                salarios = 0
            if edad > 65:
                pensiones = pensiones * (1 + inflacion)
                salarios = 0
                
            alquileres =  alquileres * (1 + inflacion)   # Alquileres siempre     
            ingresos = salarios + pensiones + alquileres
            gastos = gastos * (1 + inflacion)
            ahorros = ahorros * (1 + rentabilidad) + ingresos - gastos
            
            datos.append({
                "Edad": edad,
                "Salario":  round(salarios, 2),
                "Pensión":  round(pensiones, 2),
                "Alquileres":  round(alquileres, 2),               
                "Ingresos": round(ingresos, 2),
                "Gastos": round(gastos, 2),
                "Patrimonio": round(ahorros, 2)
                
            })

        return pd.DataFrame(datos)


    def graficar_evolucion(self, df, titulo="Evolución Financiera Anual"):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=("Patrimonio", "Ingresos y Gastos"))

        # Primer subplot: Patrimonio
        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Patrimonio"],
                                 mode='lines', name='Patrimonio',
                                 line=dict(color='green')),
                      row=1, col=1)

        # Segundo subplot: Ingresos y Gastos
        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Ingresos"],
                                 mode='lines', name='Ingresos',
                                 line=dict(color='blue')),
                      row=2, col=1)

        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Gastos"],
                                 mode='lines', name='Gastos',
                                 line=dict(color='red')),
                      row=2, col=1)
                      
        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Salario"],
                         mode='lines', name='Salario',
                         line=dict(color='yellow')),
              row=2, col=1)              

        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Pensión"],
                         mode='lines', name='Pensión',
                         line=dict(color='orange')),
              row=2, col=1)              

        fig.add_trace(go.Scatter(x=df["Edad"], y=df["Alquileres"],
                         mode='lines', name='Alquileres',
                         line=dict(color='cyan')),
              row=2, col=1)              



        fig.update_layout(title_text=titulo,
                          template="plotly_dark",
                          height=600,
                          legend_title_text="Desglose",
                          showlegend=True)

        return fig



    # -------------------------------
    # Resumen por década
    # -------------------------------
    def resumen_por_decada(self, df):
        df["Decada"] = (df["Edad"] // 10) * 10
        resumen = df.groupby("Decada").agg({
            "Ingresos": "mean",
            "Gastos": "mean",
            "Patrimonio": "last"
        }).reset_index()
        resumen.columns = ["Década", "Promedio Ingresos", "Promedio Gastos", "Patrimonio Final"]
        return resumen

    # -------------------------------
    # Comparación de escenarios
    # -------------------------------
    def comparar_escenarios(self, params1, params2):
        df1 = self.simular_evolucion_patronal(**params1)
        df2 = self.simular_evolucion_patronal(**params2)
        df1["Escenario"] = "Escenario A"
        df2["Escenario"] = "Escenario B"
        return pd.concat([df1, df2])

    def graficar_comparacion(self, df):
        fig = px.line(df, x="Edad", y="Patrimonio", color="Escenario",
                      title="Comparación de Patrimonio entre Escenarios",
                      template="plotly_dark",
                      color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(legend_title_text="Escenario")
        return fig