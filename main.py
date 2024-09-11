import speech_recognition as sr
import pyttsx3

# Inicializamos el motor de síntesis de voz
engine = pyttsx3.init()

# Configurar las propiedades de la voz
engine.setProperty('rate', 150)  # Velocidad de la voz
engine.setProperty('volume', 0.9)  # Volumen de la voz

# Inicializamos el reconocedor de voz
recognizer = sr.Recognizer()

def escuchar():
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)  # Ajusta para el ruido de fondo
        audio = recognizer.listen(source)  # Escucha la voz del usuario
    try:
        # Intenta reconocer el audio usando Google Speech Recognition
        texto = recognizer.recognize_google(audio, language='es-ES')
        print(f"Usuario dijo: {texto}")
        return texto
    except sr.UnknownValueError:
        print("No entendí lo que dijiste")
        return ""
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento de voz; {e}")
        return ""

def hablar(texto):
    engine.say(texto)  # Convierte texto en voz
    engine.runAndWait()

def asistente_de_voz():
    respuestas = {
        "salir": "Adiós, fue un placer ayudarte.",
        "adios": "Adiós, fue un placer ayudarte.",
        "hasta luego": "Adiós, fue un placer ayudarte.",
        "hasta nunca": "Adiós, fue un placer ayudarte.",
        "eliminate": "Adiós, fue un placer ayudarte.",
        "cómo estás": "Estoy muy bien, gracias por preguntar.",
        "tu nombre": "Me llamo Asistente de Voz. Estoy aquí para ayudarte.",
        "Donde te modificaron": "Soy un programa derivado de tecnología GPT modificado en la Universidad Juan Misael Saracho. Carrera de informática.",
        "De dónde estas actualmente": "Según tengo programado, estoy ubicado en el campus de la Universidad Juan Misael Saracho.",
        "por que deberia considerar la carrera de informatica": "Elegir esta carrera te abrirá puertas a un mundo de innovación y soluciones tecnológicas.",
        "Qué es la carrera de informatica": "La carrera de informática se centra en el estudio de sistemas computacionales, programación, desarrollo de software y redes. Es una carrera dinámica con amplias oportunidades laborales en diferentes sectores, desde empresas tecnológicas hasta organizaciones gubernamentales.",
        "Cuáles son las principales áreas de especialización en informática": "En informática, puedes especializarte en áreas como desarrollo de software, inteligencia artificial, ciberseguridad, redes y sistemas, bases de datos, y análisis de datos. Cada área ofrece diferentes retos y oportunidades, permitiéndote encontrar el camino que más te apasione.",
        "Qué habilidades necesito desarrollar para tener éxito en informática": "Para tener éxito en informática, debes desarrollar habilidades en programación, resolución de problemas, trabajo en equipo y comunicación. Además, una actitud proactiva para aprender y adaptarte a nuevas tecnologías es crucial para mantenerte al día en esta carrera en constante evolución.",
        "Qué tipo de proyectos puedo realizar en la carrera de informática": "En la carrera de informática, puedes trabajar en proyectos como aplicaciones móviles, sistemas de gestión, juegos, algoritmos de inteligencia artificial, y soluciones para problemas del mundo real.",
        "Qué oportunidades laborales existen para los graduados en informática en Yacuiba": "En Yacuiba, los graduados en informática pueden encontrar oportunidades en empresas de tecnología, startups, instituciones gubernamentales y educativas.",
        "¿Qué beneficios ofrece estudiar informática en la Universidad Autónoma Juan Misael Saracho?": "Estudiar informática en la UAJMS te ofrece una formación sólida en tecnologías actuales, acceso a laboratorios equipados, y la posibilidad de participar en proyectos reales y prácticas profesionales. La universidad también cuenta con una red de contactos que puede ayudarte a iniciar tu carrera profesional.",
        "¿Cómo puedo prepararme para estudiar informática en la UAJMS?": "Para prepararte, te recomendamos que te familiarices con conceptos básicos de programación, matemáticas y lógica. Participa en cursos en línea, realiza proyectos personales, y mantente al día con las últimas tendencias tecnológicas. Además, visita la página de la UAJMS para conocer más sobre el plan de estudios y requisitos de admisión.",
        "¿que modalidades de ingreso existen?": "Actualmente existen 3 modalidades de ingreso: por excelencia (promedio de nota por curso), por cursos preuniversitarios impartidos por docentes capacitados de la carrera, y por Prueba de Suficiencia Académica (examen).",
        "¿que beneficios te ofrece la carrera como apoyo al estudiante?": "Actualmente, en el campus de Yacuiba se ofrecen becas comedor a estudiantes de segundo año en adelante, seguro médico para una caja de salud, y una guardería que estará pronto en funcionamiento.",
        "¿que materias se llevan en informática?": "Entre las materias que aprenderás están programación hasta 4 niveles, bases de datos, redes, ingeniería de software, inteligencia artificial, robótica, multimedia, entre otras materias impartidas por profesionales con dominio de las materias.",
        "¿te gusta el pan?": "La tuya por si acaso."
    }

    hablar("Hola, soy tu asistente de voz. ¿En qué puedo ayudarte?")
    while True:
        texto_usuario = escuchar()
        if texto_usuario:
            respuesta = respuestas.get(texto_usuario.lower(), "Lo siento, no entendí tu pregunta.")
            hablar(respuesta)
            if respuesta == "Adiós, fue un placer ayudarte.":
                break
        else:
            hablar("Por favor, repite la pregunta.")

# Iniciar el asistente
asistente_de_voz()
