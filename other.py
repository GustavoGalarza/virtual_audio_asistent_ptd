import torch
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import speech_recognition as sr

# Configuración del modelo y el tokenizador
model_name = 'ostorc/Conversational_Spanish_GPT'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Configuración del motor de texto a voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # velocidad de habla
engine.setProperty('volume', 1)  # volumen (0.0 a 1.0)

# Inicialización del reconocedor de voz
recognizer = sr.Recognizer()

def speak(text):
    """Función para que el asistente hable"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Función para escuchar el comando del usuario"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language='es-ES')
            print(f"Usuario dijo: {command}")
            return command
        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            return None
        except sr.RequestError:
            print("No se pudo conectar con el servicio de reconocimiento de voz.")
            return None
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado para el reconocimiento de voz.")
            return None

def chat_with_model(user_input):
    """Función para interactuar con el modelo GPT-2"""
    with torch.no_grad():
        user_inputs_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        user_inputs_ids = user_inputs_ids.to(device)
        chat_history = model.generate(user_inputs_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        step_model_answer = tokenizer.decode(chat_history[:, user_inputs_ids.shape[-1]:][0], skip_special_tokens=True)
        return step_model_answer

# Ejecución del asistente de voz
speak("El asistente de voz está listo. Di 'salir' para terminar.")
while True:
    try:
        user_input = listen()
        if user_input:
            if user_input.lower() == 'salir':
                speak("Hasta luego.")
                break
            response = chat_with_model(user_input)
            print(f"GPT-2 respondió: {response}")
            speak(response)
        else:
            speak("Por favor, repite el comando.")
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Cerrando el asistente.")
        speak("Hasta luego.")
        break
    except Exception as e:
        print(f"Se produjo un error: {e}")
        speak("Se produjo un error. Por favor, inténtalo de nuevo.")
