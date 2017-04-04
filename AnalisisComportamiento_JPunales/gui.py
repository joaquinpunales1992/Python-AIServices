import Tkinter as tk
from Tkinter import *
import tkFileDialog
import tkMessageBox
import WatsonPersonalityInsight as WPI
import WatsonToneAnalyzer as WTA
import config



class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Analisis de Comportamiento by JoaquinP")
        self.parent.minsize(1100, 310)
        self.parent.maxsize(1100, 410)
        #Escala
        self.vEscalaScore = tk.Scale(self, from_=0.0, to=1.0, resolution=0.1, tickinterval=0.5, orient=HORIZONTAL, font="MSSansSerif 10 bold", label="Porcentaje de Certeza:", bd=2, length=310)
        self.vEscalaScore.grid(row=1, column=1, columnspan=8, rowspan=1)
        #Botones
        self.vBotonCargarArchivo = tk.Button(self, text='Cargar Archivo', command=self.obtnerArhivoDatos,  height=5, width=25, bd=4,  font="MSSansSerif 10 bold", bg="#E6E0F8")
        self.vBotonCargarArchivo.grid(row=0, column=2, columnspan=2, rowspan=1)
        self.vBotonInvocarPI = tk.Button(self, text="Consultar", command=self.obtenerResultados, height=5, width=25, bd=4, font="MSSansSerif 10 bold", bg="#E6E0F8", state=DISABLED)
        self.vBotonInvocarPI.grid(row=0, column=4, columnspan=2, rowspan=1)
        #Listas
        self.vListaResultado = tk.Listbox(self, width=60, height=8, bg="#E6E0F8", selectbackground="#819FF7", highlightthickness=3, fg= "#6E6E6E",    font="MSSansSerif 15")
        self.vListaResultado.grid(row=2,column=0, rowspan = 3)
        self.vListaPreguntas = tk.Listbox(self, width=60, height=8 , selectbackground="#819FF7", highlightthickness=3, bg="#E6E0F8",fg= "#6E6E6E", font="MSSansSerif 15")
        self.vListaPreguntas.grid(row=0, column=0, rowspan=2)
        self.crearGraficaTonos()


    def crearGraficaTonos(self):
        self.vValorEnojo = DoubleVar()
        self.vValorDisgusto = DoubleVar()
        self.vValorTemor = DoubleVar()
        self.vValorAlegria = DoubleVar()
        self.vValorTristesa = DoubleVar()
        self.vLabelEnojo = tk.Label(self, text="Enojo:")
        self.vLabelEnojo.grid(row=2, column=1, columnspan=2, rowspan=1)
        self.vEntryEnojo = tk.Entry(self, textvariable=self.vValorEnojo, width=9, state="disabled")
        self.vEntryEnojo.grid(row=2, column=2, columnspan=2, rowspan=1)
        self.vLabelDisgusto = tk.Label(self, text="Disgusto: ")
        self.vLabelDisgusto.grid(row=2, column=3, columnspan=2, rowspan=1)
        self.vEntryDisgusto = tk.Entry(self, textvariable=self.vValorDisgusto, width=9, state="disabled")
        self.vEntryDisgusto.grid(row=2, column=4, columnspan=1, rowspan=1)
        self.vLabelTemor = tk.Label(self, text="Temor:")
        self.vLabelTemor.grid(row=3, column=1, columnspan=2, rowspan=1)
        self.vEntryTemor = tk.Entry(self, textvariable=self.vValorTemor, width=9, state="disabled")
        self.vEntryTemor.grid(row=3, column=2, columnspan=2, rowspan=1)
        self.vLabelAlegria = tk.Label(self, text="Alegria:")
        self.vLabelAlegria.grid(row=3, column=3, columnspan=2, rowspan=1)
        self.vEntryAlegria = tk.Entry(self, textvariable=self.vValorAlegria, width=9, state="disabled")
        self.vEntryAlegria.grid(row=3, column=4, columnspan=1, rowspan=1)
        self.vLabelTristesa = tk.Label(self, text="Tristesa:")
        self.vLabelTristesa.grid(row=4, column=1, columnspan=2, rowspan=1)
        self.vEntryTristesa = tk.Entry(self, textvariable=self.vValorTristesa, width=9, state="disabled")
        self.vEntryTristesa.grid(row=4, column=2, columnspan=2, rowspan=1)

    def validarParametros(self, pInvoca):
        if (pInvoca == 'obtenerResultados'):
            self.vPreguntaSeleccionada = self.vListaPreguntas.curselection()
            if (self.vPreguntaSeleccionada == ()):
                tkMessageBox.showwarning("Advertencia", "Debes seleccionar una pregunta :(")
            else:
                return True



    def obtenerResultados(self):
        vValidacionParametros =  self.validarParametros('obtenerResultados')
        if (vValidacionParametros):
            self.vListaResultado.delete(0, END)
            vCategoriaJSON  =  self.vListaPreguntas.get(self.vListaPreguntas.curselection())
            for vConsuptionPreference in self.vResultadoPersonalidad["consumption_preferences"]:
                if (self.obtenerConsumptionPreferenceJSON(vCategoriaJSON) == vConsuptionPreference["consumption_preference_category_id"] or vCategoriaJSON == 1):
                    for vConsuptionPreferenceItem in vConsuptionPreference["consumption_preferences"]:
                         if (vConsuptionPreferenceItem["score"] >= float(self.vEscalaScore.get())):
                             vPreferenciaJSON = self.obtenerPreferenciaJSON(vConsuptionPreferenceItem["consumption_preference_id"])
                             self.vListaResultado.insert(END, "  " + (vPreferenciaJSON).encode('utf-8') + ":")
                             self.vListaResultado.insert(END, "     " + (vConsuptionPreferenceItem["name"]).encode('utf-8'))
                             self.vListaResultado.insert(END, "     " + self.obtenerPorcentajeCerteza(vConsuptionPreferenceItem["score"]))


    def cargarListaCategorias(self, pCategoria):
        self.vListaPreguntas.insert(END, self.obtenerCategoriaJSON(pCategoria))

    def obtenerPorcentajeCerteza(self, pScore):
        vResultado = str('% ' + str(pScore * 100) + ' de certeza')
        return vResultado


    def obtenerConsumptionPreferenceJSON(self, pCategoriaJSON):
        return{
             'Preferencias con respecto a las compras': 'consumption_preferences_shopping',
             'Preferencias con respecto a Salud y deporte': 'consumption_preferences_health_and_activity',
             'Preferencias con respecto al medio ambiente': 'consumption_preferences_environmental_concern',
             'Preferencias con respecto a emprender' : 'consumption_preferences_entrepreneurship',
             'Preferencias con respecto a las peliculas': 'consumption_preferences_movie',
             'Preferencias con respecto a la musica': 'consumption_preferences_music',
             'Preferencias con respecto a leer': 'consumption_preferences_reading',
             'Preferencias con respecto al voluntariado': 'consumption_preferences_volunteering'
            }.get(pCategoriaJSON, pCategoriaJSON)


    def obtenerCategoriaJSON(self, pCategoriaJSON):
        return{
            'consumption_preferences_shopping': 'Preferencias con respecto a las compras',
            'consumption_preferences_health_and_activity': 'Preferencias con respecto a Salud y deporte',
            'consumption_preferences_environmental_concern': 'Preferencias con respecto al medio ambiente',
            'consumption_preferences_entrepreneurship': 'Preferencias con respecto a emprender',
            'consumption_preferences_movie': 'Preferencias con respecto a las peliculas',
            'consumption_preferences_music': 'Preferencias con respecto a la musica',
            'consumption_preferences_reading': 'Preferencias con respecto a leer',
            'consumption_preferences_volunteering': 'Preferencias con respecto al voluntariado'
            }.get(pCategoriaJSON, pCategoriaJSON)


    def obtenerPreferenciaJSON(self, pPreferenciaJSON):
        return{
            'consumption_preferences_automobile_ownership_cost': 'Preferencia con respecto a la compra de automoviles',
            'consumption_preferences_automobile_safety': 'Preferencia con respecto a la seguridad de los automoviles',
            'consumption_preferences_clothes_quality': 'Preferencia con respecto a la calidad de la ropa',
            'consumption_preferences_clothes_style': 'Preferencia con respecto a los colores de la ropa',
            'consumption_preferences_clothes_comfort': 'Preferencia con respecto al confort de la ropa',
            'consumption_preferences_influence_brand_name': 'Preferencia con respecto a las marcas de ropa',
            'consumption_preferences_influence_utility': 'Preferencia con respecto a la influencia de los utilitis',
            'consumption_preferences_influence_online_ads': 'Preferencia con respecto a las publicidades de internet',
            'consumption_preferences_influence_social_media': 'Preferencia con respecto a las redes sociales',
            'consumption_preferences_influence_family_members': 'Preferencia con respecto a la influencia familiar',
            'consumption_preferences_spur_of_moment': 'Preferencia con respecto a disfrutar el momento',
            'consumption_preferences_credit_card_payment': 'Preferencia con respecto a las tarjetas de credito',
            'consumption_preferences_eat_out': 'Preferencia con respecto a salir a comer',
            'consumption_preferences_gym_membership': 'Preferencia con respecto a los gimnasios',
            'consumption_preferences_outdoor': 'Preferencia con respecto a salir al exterior',
            'consumption_preferences_concerned_environment': 'Preferencia con respecto al medio ambiente',
            'consumption_preferences_start_business': 'Preferencia con respecto a emprender un negocio',
            'consumption_preferences_movie_romance': 'Preferencia con respecto a las peliculas romanticas',
            'consumption_preferences_movie_adventure': 'Preferencia con respecto a las peliculas de aventura',
            'consumption_preferences_movie_horror': 'Preferencia con respecto a las peliculas de terror',
            'consumption_preferences_movie_musical': 'Preferencia con respecto a las peliculas musicales',
            'consumption_preferences_movie_historical': 'Preferencia con respecto a las peliculas de historia',
            'consumption_preferences_movie_science_fiction': 'Preferencia con respecto a las peliculas de ciencia ficcion',
            'consumption_preferences_movie_war': 'Preferencia con respecto a las peliculas de guerra',
            'consumption_preferences_movie_drama': 'Preferencia con respecto a las peliculas de drama',
            'consumption_preferences_movie_action': 'Preferencia con respecto a las peliculas de accion',
            'consumption_preferences_movie_documentary': 'Preferencia con respecto a las peliculas documentales',
            'consumption_preferences_music_rap': 'Prefencia con respecto a la musica RAP',
            'consumption_preferences_music_country': 'Preferencia con respecto a la musica Country',
            'consumption_preferences_music_r_b': 'Preferencia con respecto a la musica R&B',
            'consumption_preferences_music_hip_hop': 'Preferencia con respecto a la musica Hip Hop',
            'consumption_preferences_music_live_event': 'Preferencia con respecto a los conciertos',
            'consumption_preferences_music_playing': 'Preferencia con respecto a tocar un instrumento',
            'consumption_preferences_music_latin': 'Preferencias con respecto a la musica Latina',
            'consumption_preferences_music_rock': 'Preferencia con respecto a la musica Rock',
            'consumption_preferences_music_classical': 'Preferencia con respecto a la musica clasica',
            'consumption_preferences_read_frequency': 'Preferencia con respecto a la lectura',
            'consumption_preferences_books_entertainment_magazines': 'Preferencia con respecto a leer revistas',
            'consumption_preferences_books_non_fiction': 'Preferencia con respecto a los libros basados en hechos reales',
            'consumption_preferences_books_financial_investing': 'Preferencia con respecto a los libros financieros',
            'consumption_preferences_books_autobiographies': 'Preferencia con respecto a los libros autobiograficos',
            'consumption_preferences_volunteer': 'Preferencia con respecto al voluntariado'
              }.get(pPreferenciaJSON, pPreferenciaJSON)


    def obtnerArhivoDatos(self):
        self.vListaPreguntas.delete(0, END)
        vArchivoDatos = tkFileDialog.askopenfilename()
        self.invocarServiciosWatson(vArchivoDatos)


    def invocarServiciosWatson(self, pArchivoDatos):
        vTono = WTA.Tono()
        vResultadoTono = vTono.invocarWToneAnalyzer(pArchivoDatos)
        self.cargarTono(vResultadoTono)
        personalidad = WPI.Personalidad()
        self.vResultadoPersonalidad = personalidad.invocarWatsonPI(pArchivoDatos)
        for vConsuptionPreference in self.vResultadoPersonalidad["consumption_preferences"]:
            self.cargarListaCategorias(vConsuptionPreference["consumption_preference_category_id"])
        self.vBotonInvocarPI.configure(state="normal")



    def cargarTono(self, pResultadoTono):
        for vTono in pResultadoTono["document_tone"]["tone_categories"][0]["tones"]:
            if (vTono["tone_id"] == "anger"):
                self.vEntryEnojo.config(state="normal")
                self.vValorEnojo.set(vTono["score"])
            if (vTono["tone_id"] == "disgust"):
                self.vEntryDisgusto.config(state="normal")
                self.vValorDisgusto.set(vTono["score"])
            if (vTono["tone_id"] == "fear"):
                self.vEntryTemor.config(state="normal")
                self.vValorTemor.set(vTono["score"])
            if (vTono["tone_id"] == "joy"):
                self.vEntryAlegria.config(state="normal")
                self.vValorAlegria.set(vTono["score"])
            if (vTono["tone_id"] == "sadness"):
                self.vEntryTristesa.config(state="normal")
                self.vValorTristesa.set(vTono["score"])


if __name__ == "__main__":
    root = tk.Tk()

    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.iconbitmap(config.rutaIcono)
    root.mainloop()