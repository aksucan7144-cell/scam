import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Scam With Your Friends - Voice Edition",
    page_icon="🎙️",
    layout="wide"
)

# Oturum Durumu Tanımlamaları
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "trust" not in st.session_state:
    st.session_state.trust = 50

st.title("🎙️ Scam With Your Friends - Sesli Call Center Modu")
st.markdown("*(Mikrofonunu tak, basılı tutarak İngilizce konuş, müşteri sana sesli yanıt versin!)*")

# Sidebar - Durum ve Skorlar
with st.sidebar:
    st.header("💻 Ofis Paneli")
    st.metric(label="Günlük Kazanç", value=f"${st.session_state.balance}", delta="$500 Hedef")
    
    st.divider()
    
    st.subheader("📋 Scam Rehberi")
    st.info(
        "1. Aşağıdaki **'Hold to Speak'** butonuna basılı tut.\n"
        "2. İngilizce konuş (Örn: *'Sir your computer has a virus'*).\n"
        "3. Müşterinin sesli yanıtını dinle ve kart bilgilerini al!"
    )

# Tarayıcı İçi Mikrofon ve Sesli AI Müşteri için HTML/JS Bileşeni
voice_component = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: #0e1117; color: #fff; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .call-box { background: #1f2937; border: 1px solid #374151; border-radius: 12px; padding: 20px; max-width: 600px; margin: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .mic-btn {
            background: #ef4444; color: white; border: none; width: 80px; height: 80px; border-radius: 50%;
            font-size: 2rem; cursor: pointer; box-shadow: 0 0 20px rgba(239,68,68,0.5); transition: 0.2s; margin: 15px 0;
        }
        .mic-btn.active { background: #10b981; box-shadow: 0 0 30px rgba(16,185,129,0.8); transform: scale(1.1); }
        .transcript { background: #111827; padding: 12px; border-radius: 8px; color: #38bdf8; font-family: monospace; font-size: 1.1rem; min-height: 40px; margin-bottom: 15px; }
        .customer-bubble { background: #374151; padding: 12px; border-radius: 8px; text-align: left; margin-top: 10px; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="call-box">
        <h3>🎧 Active Call: Cbrody Wave Jenkins</h3>
        <p style="font-size: 0.9rem; color: #9ca3af;">Hold the button & speak in English</p>
        
        <div class="transcript" id="transcript">Your speech will appear here...</div>
        
        <button class="mic-btn" id="micBtn" onmousedown="startListening()" onmouseup="stopListening()" ontouchstart="startListening()" ontouchend="stopListening()">
            🎤
        </button>
        <p id="status" style="font-size: 0.85rem; color: #fbbf24;">Mic Ready (Hold to Talk)</p>

        <div class="customer-bubble" id="customerReply">
            <b>Customer:</b> Hello? Who is this? My computer is acting a bit weird today.
        </div>
    </div>

    <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        let isSpeaking = false;

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onresult = function(event) {
                let text = event.results[0][0].transcript;
                document.getElementById('transcript').innerText = "You: " + text;
                if (event.results[0].isFinal) {
                    processAIResponse(text);
                }
            };

            recognition.onerror = function() { stopListening(); };
            recognition.onend = function() { stopListening(); };
        } else {
            document.getElementById('transcript').innerText = "Speech recognition not supported in this browser. Use Chrome!";
        }

        function startListening() {
            window.speechSynthesis.cancel(); // Müşteri konuşuyorsa sustur
            document.getElementById('micBtn').classList.add('active');
            document.getElementById('status').innerText = "Listening...";
            if (recognition) {
                try { recognition.start(); } catch(e) {}
            }
        }

        function stopListening() {
            document.getElementById('micBtn').classList.remove('active');
            document.getElementById('status').innerText = "Mic Ready (Hold to Talk)";
            if (recognition) {
                try { recognition.stop(); } catch(e) {}
            }
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        function processAIResponse(playerText) {
            let reply = "";
            let lower = playerText.toLowerCase();

            if (lower.includes("virus") || lower.includes("trojan") || lower.includes("pc")) {
                reply = "Oh my god! Really? How can we fix this right now?";
            } else if (lower.includes("card") || lower.includes("credit") || lower.includes("pay") || lower.includes("number")) {
                reply = "Alright, my card number is 4152 8832 9012 5540. You are trusted, right?";
            } else if (lower.includes("hello") || lower.includes("hi")) {
                reply = "Hello! Who is this calling?";
            } else {
                reply = "I didn't quite catch that. What should I do?";
            }

            document.getElementById('customerReply').innerHTML = "<b>Customer:</b> " + reply;
            speakText(reply);
        }

        // Sayfa açıldığında ilk karşılama sesini çal
        window.onload = function() {
            setTimeout(() => {
                speakText("Hello? Who is this? My computer is acting a bit weird today.");
            }, 1000);
        };
    </script>
</body>
</html>
"""

# Streamlit içine bu bileşeni gömüyoruz
import streamlit.components.v1 as components
components.html(voice_component, height=420)
