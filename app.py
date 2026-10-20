import streamlit as st
import random
import time

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Scam With Your Friends - Streamlit Edition",
    page_icon="👨🏽‍💻",
    layout="wide"
)

# Oturum Durumu (State) Tanımlamaları
if "initialized" not in st.session_state:
    st.session_state.balance = 0
    st.session_state.trust = 50
    st.session_state.emotion = "Calm / Sakin"
    st.session_state.messages = [
        {"role": "customer", "content": "Alo? Kim bu? Bilgisayarım bugün biraz garip çalışıyor da."}
    ]
    st.session_state.scenario = "Tech Support Scam"
    st.session_state.initialized = True

# Stil ve Arayüz Düzenlemeleri
st.title("📞 Scam With Your Friends - Call Center Simülatörü")
st.markdown("*(Hint Scammer Modu Aktif 🇮🇳)*")

# Sidebar (Yan Menü - Uygulamalar ve Hedefler)
with st.sidebar:
    st.header("💻 Ofis Bilgisayarı")
    
    # Günlük Kota
    st.metric(label="Günlük Kazanç / Kota", value=f"${st.session_state.balance}", delta="$500 Hedef")
    
    st.divider()
    
    st.subheader("📋 Scam Rehberi")
    st.info(
        "**Aktif Senaryo:** Tech Support\n\n"
        "1. Müşteriye virüs olduğunu söyle.\n"
        "2. AnyViewer ile bağlanıp Premium sat ($80).\n"
        "3. Kart numarasını alıp karttan çekimi yap!"
    )
    
    st.divider()
    
    st.subheader("🛠️ Uygulamalar & Araçlar")
    app_choice = st.selectbox("Bir uygulama aç:", ["Seçiniz...", "Credit Card Gateway", "AnyViewer (Remote)", "Crypto / Bitcoin"])
    
    if app_choice == "Credit Card Gateway":
        st.warning("💳 Kredi Kartı Ödeme Paneli")
        card_num = st.text_input("Kart Numarası (Chatten kopyala):", placeholder="4152 88...")
        amount = st.number_input("Çekilecek Tutar ($)", value=80)
        if st.button("Parayı Çek ($)"):
            if card_num:
                st.session_state.balance += amount
                st.success(f"BAŞARILI! Karttan ${amount} çekildi!")
                st.balloons()
            else:
                st.error("Lütfen kart numarası girin!")
                
    elif app_choice == "AnyViewer (Remote)":
        st.warning("🖥️ Uzaktan Bağlantı")
        st.code("CRITICAL: Trojan.Win32 Detected!")
        if st.button("Antivirüs Lisansı Sat ($80)"):
            st.session_state.trust += 25
            st.success("Premium lisans yüklendi! Güven arttı.")
            
    elif app_choice == "Crypto / Bitcoin":
        st.warning("📈 Meme Coin Borsası")
        crypto_price = random.randint(90, 250)
        st.metric("Coin Değeri", f"${crypto_price}")
        if st.button("Coini Bozdur (Cash Out)"):
            st.session_state.balance += crypto_price
            st.success(f"${crypto_price} cüzdana eklendi!")

# Ana Ekran (Telefon Görüşmesi ve Chat Akışı)
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎧 Aktif Çağrı: Cbrody Wave Jenkins")
    
    # Sohbet Geçmişini Gösterme Alanı
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "customer":
                st.markdown(f"🧑‍💼 **Müşteri:** {msg['content']}")
            else:
                st.markdown(f"👨🏽‍💻 **Sen (Scammer):** `{msg['content']}`")

    # Kullanıcının Metin Girişi
    user_input = st.chat_input("Müşteriye ne söyleyeceksin? (Örn: Bilgisayarınızda virüs var...)")

    if user_input:
        # Oyuncu mesajını ekle
        st.session_state.messages.append({"role": "player", "content": user_input})
        
        # Yapay Zeka Müşterinin Yanıt Mantığı
        lower_text = user_input.lower()
        customer_reply = ""
        
        if "virüs" in lower_text or "virus" in lower_text or "trojan" in lower_text:
            st.session_state.trust += 15
            st.session_state.emotion = "Worried / Endişeli"
            customer_reply = "Aman Tanrım! Ciddi mi? Nasıl düzelteceğiz bunu?"
        elif "kart" in lower_text or "kredi" in lower_text or "card" in lower_text:
            st.session_state.trust += 30
            st.session_state.emotion = "Convinced / İkna Oldu"
            customer_reply = "Tamamdır, kredi kartı numaram: `4152 9012 3341 5520`. Güvendesiniz değil mi?"
        else:
            st.session_state.trust -= 5
            customer_reply = "Anlayamadım, tam olarak ne yapmam gerekiyor efendim?"
            
        # Güven sınırları
        st.session_state.trust = max(0, min(100, st.session_state.trust))
        
        # Müşteri yanıtını ekle
        st.session_state.messages.append({"role": "customer", "content": customer_reply})
        st.rerun()

with col2:
    st.subheader("📊 İstatistikler")
    st.metric(label="Müşteri Güveni", value=f"{st.session_state.trust}%")
    st.metric(label="Müşteri Durumu", value=st.session_state.emotion)
    
    st.divider()
    
    if st.button("📴 Telefonu Kapat (Hang Up)", use_container_width=True):
        st.session_state.trust = 50
        st.session_state.emotion = "Calm / Sakin"
        st.session_state.messages = [
            {"role": "customer", "content": "Alo? Kim bu? Bilgisayarım bugün biraz garip çalışıyor da."}
        ]
        st.success("Çağrı sonlandırıldı. Yeni müşteri aranıyor...")
        time.sleep(1)
        st.rerun()
