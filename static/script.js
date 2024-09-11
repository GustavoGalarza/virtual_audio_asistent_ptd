document.addEventListener("DOMContentLoaded", function() {
    const recordBtn = document.getElementById('recordBtn');
    const conversationDiv = document.getElementById('conversation');
    const responseDiv = document.getElementById('response');
    const convertTextToSpeechBtn = document.getElementById('convertTextToSpeech');
    const textInput = document.getElementById('textInput');
    const toggleBtn = document.getElementById('toggleBtn');
    const recognizedTextDiv = document.getElementById('recognized-text');  // Definición añadida aquí

    if (!recordBtn || !conversationDiv || !toggleBtn || !responseDiv || !convertTextToSpeechBtn || !textInput || !recognizedTextDiv) {
        console.error("No se encontraron los elementos necesarios en el DOM.");
        return;
    }

    // Event listener for recording button
    recordBtn.addEventListener('click', () => {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = function() {
                recordBtn.textContent = "Escuchando...";
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                addMessage('Usuario', transcript);
                sendToBackend(transcript);
            };

            recognition.onerror = function(event) {
                console.log('Error:', event.error);
            };

            recognition.onend = function() {
                recordBtn.textContent = "🎤 Pulsar para hablar";
            };

            recognition.start();
        } else {
            alert("El reconocimiento de voz no es compatible con tu navegador.");
        }
    });

    // Event listener for text-to-speech button
    convertTextToSpeechBtn.addEventListener('click', () => {
        const text = textInput.value.trim();
        if (text) {
            speakResponse(text);
        } else {
            alert("Por favor, ingresa un texto.");
        }
    });

    // Function to add message to the conversation
    function addMessage(sender, message) {
        const newMessage = document.createElement('p');
        newMessage.textContent = `${sender}: ${message}`;
        conversationDiv.appendChild(newMessage);
        conversationDiv.scrollTop = conversationDiv.scrollHeight;
    }

    // Function to send transcript to backend
    function sendToBackend(text) {
        fetch('http://127.0.0.1:5000/send_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from Flask:', data.response);
            addMessage('Chatbot', data.response);
            speakResponse(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to speak the response
    function speakResponse(text) {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';  // Configuración para español
        synth.speak(utterance);
    }

    // Function to show specific page
    window.showPage = function(pageId) {
        const pages = document.querySelectorAll('.page');
        pages.forEach(page => {
            page.classList.remove('active');
            if (page.id === pageId) {
                page.classList.add('active');
            }
        });
    }
    
    // Set default page
    showPage('voice-assistant');

    // Event listener for the voice recognition toggle button
    let recognition = null;
    let recognizing = false;

    toggleBtn.addEventListener('click', () => {
        if ('webkitSpeechRecognition' in window) {
            if (recognizing) {
                recognition.stop();
                toggleBtn.textContent = "🎤 Activar Micrófono";
                recognizing = false;
            } else {
                recognition = new webkitSpeechRecognition();
                recognition.lang = 'es-ES';
                recognition.continuous = true;
                recognition.interimResults = false;

                recognition.onstart = function() {
                    recognizing = true;
                    toggleBtn.textContent = "👤 Desactivar Micrófono";
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    recognizedTextDiv.textContent = transcript;
                };

                recognition.onerror = function(event) {
                    console.log('Error:', event.error);
                };

                recognition.onend = function() {
                    recognizing = false;
                    toggleBtn.textContent = "🎤 Activar Micrófono";
                };

                recognition.start();
            }
        } else {
            alert("El reconocimiento de voz no es compatible con tu navegador.");
        }
    });
});
