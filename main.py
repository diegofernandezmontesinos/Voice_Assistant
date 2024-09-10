import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    #almacenar el reconocedor en variable
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("Now you can speak")

        #guardar lo que escuche como audio

        audio = r.listen(origen)

        try:
            #buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-es")

            # prueba de que pudo ingresar
            print("You said: " + pedido)

            #devolver pedido
            return pedido

        #en caso de que no comprenda audio

        except sr.UnknownValueError:
            #prueba de que no comprendio audio
            print("I couldn't understand")

            #devolver error
            return "Still waiting"

        #en caso de que no pueda resovler el pedido

        except sr.RequestError:
            print("There's no service")
            # devolver error
            return "Still waiting"

        #en caso de que sea un error inesperado
        except:
            print("There have been an unespected error")
            # devolver error
            return "Still waiting"

#funcion para que el asistente pueda ser escuchado

def hablar(mensaje):
    #encender el motor de pyttsx3
    engine = pyttsx3.init()

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#hablar("Hello world")
'''
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)
'''

#informar el día
def pedir_dia():
    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear variable para el dia de la semana
    dia_semana = dia.weekday()
    #diccionario con los nombres de los días
    calendario = {0: 'Monday',
                  1: 'Tuesday',
                  2: 'Wednesday',
                  3: 'Thursday',
                  4: 'Friday',
                  5: 'Saturday',
                  6: 'Sunday'}

    #decir el dia de la semana

    print(calendario[dia_semana])

    hablar(f'Hoy es {calendario[dia_semana]}')

#pedir_dia()

#informar la hora
def pedir_hora():
    #crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora= f'In this moment it is {hora.hour} hours with {hora.minute} minutes'
    print(hora)

    #decir la hora
    hablar(hora)


#funcion saludo inicial

def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora .hour > 20:
        momento = 'Good evening'
    elif 6 <= hora.hour < 13:
        momento = 'Good morning'
    else:
        momento = 'Good afternoon'

    #decir saludo
    hablar(f'{momento}, I am Wall-E, your personal assistant. Please tell me what do you need')

#funcion central del asistente

def pedir_cosas():
    #activar el saludo inicial
    saludo_inicial()

    # variale de corte
    comenzar = True

    #loop central
    while comenzar:
        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'open youtube' in pedido:
            hablar('Ok, I am going to open Youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'open the browser' in pedido:
            hablar('Ok, I am going to open the browser')
            webbrowser.open('https://www.google.com')
            continue
        elif 'what time it is' in pedido:
            pedir_hora()
            continue
        elif 'what day is it' in pedido:
            pedir_dia()
            continue
        elif 'search in wikipedia' in pedido:
            hablar('Ok, I am going to search that in wikipedia')
            pedido = pedido.replace('search in wikipedia', '')
            resultado = wikipedia.summary(pedido, sentences = 2)
            hablar('Wikipedida say: ')
            hablar(resultado)
            continue
        elif 'search in the browser' in pedido:
            hablar('I am going search that in the browser')
            resultado = pedido.replace('search in the browser', '')
            pywhatkit.search(resultado)
            hablar('This is what I found')
            continue
        elif 'play' in pedido:
            hablar('Good idea, I am going to play that video')
            pywhatkit.playonyt(pedido)
        elif 'joke' in pedido:
            hablar('Do you want a joke?')
            hablar(pyjokes.get_joke('es'))
        elif 'stock value' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon' : 'AMZN',
                       'google' : 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_accion = accion_buscada['regularMarketPrice']
                hablar(f'I found it, the price of the stock {accion} is {precio_accion}')
                continue
            except:
                hablar("I couldn't found it")
                continue
        elif 'bye' in pedido:
            hablar('Great, I am going to take a rest')
            break

pedir_cosas()



