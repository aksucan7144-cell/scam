import streamlit as st
import streamlit.components.v1 as components

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Scam With Your Friends - Streamlit Voice Edition",
    page_icon="🎙️",
    layout="wide"
)

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scam With Your Friends</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body { background-color: #0b0f19; font-family: 'Inter', sans-serif; color: #fff; overflow: hidden; height: 100vh; }

        #game-container { display: flex; width: 100vw; height: 100vh; position: relative; background: #090d16; }
        
        .sidebar { width: 340px; background: #1e293b; border-right: 1px solid #334155; display: flex; flex-direction: column; padding: 15px; gap: 12px; overflow-y: auto; height: 100vh; }
        .panel { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px; }
        .panel h3 { font-size: 0.85rem; color: #94a3b8; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        
        .app-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .app-icon {
            background: #334155; border: none; border-radius: 6px; padding: 10px 5px; color: #fff;
            display: flex; flex-direction: column; align-items: center; gap: 5px; cursor: pointer; transition: 0.2s; font-size: 0.7rem;
        }
        .app-icon:hover { background: #475569; transform: scale(1.05); }
        .app-icon i { font-size: 1.2rem; color: #38bdf8; }

        .main-call-area { flex: 1; display: flex; flex-direction: column; background: #0f172a; height: 100vh; }
        .call-header { background: #1e293b; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; }
        .call-stats { display: flex; gap: 15px; font-size: 0.85rem; }
        .stat-bar { background: #334155; padding: 4px 10px; border-radius: 4px; display: flex; gap: 6px; align-items: center; }
        
        .chat-stream { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-family: 'VT323', monospace; font-size: 1.4rem; max-height: calc(100vh - 150px); }
        .chat-msg { padding: 10px 15px; border-radius: 8px; max-width: 75%; line-height: 1.2; word-break: break-all; }
        .chat-msg.customer { background: #334155; color: #f8fafc; align-self: flex-start; }
        .chat-msg.player { background: #047857; color: #ecfdf5; align-self: flex-end; cursor: pointer; }
        .chat-msg.player:hover { outline: 2px dashed #34d399; }
        
        .call-controls { background: #1e293b; padding: 15px 20px; display: flex; gap: 15px; align-items: center; border-top: 1px solid #334155; }
        .mic-btn {
            background: #ef4444; color: #fff; border: none; width: 60px; height: 60px; border-radius: 50%;
            font-size: 1.3rem; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(239,68,68,0.5); transition: 0.2s;
        }
        .mic-btn.active { background: #10b981; box-shadow: 0 0 25px rgba(16,185,129,0.8); animation: pulseMic 1s infinite; }
        @keyframes pulseMic { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        
        .transcript-box { flex: 1; background: #0f172a; border: 1px solid #475569; border-radius: 8px; padding: 10px 15px; font-size: 1rem; color: #38bdf8; font-family: 'VT323', monospace; }
        .hangup-btn { background: #dc2626; color: #fff; border: none; padding: 10px 20px; font-weight: 700; border-radius: 8px; cursor: pointer; }
        .hangup-btn:hover { background: #b91c1c; }

        .modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.65); display: none; align-items: center; justify-content: center; z-index: 2000; }
        .modal-window { background: #1e293b; border: 1px solid #475569; border-radius: 10px; width: 400px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        .modal-head { background: #0f172a; padding: 12px 15px; font-weight: 600; display: flex; justify-content: space-between; border-bottom: 1px solid #334155; }
        .modal-body { padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .modal-body input { background: #0f172a; border: 1px solid #334155; padding: 10px; color: #fff; border-radius: 6px; outline: none; }
        .modal-body button { background: #10b981; border: none; padding: 10px; font-weight: 700; border-radius: 6px; cursor: pointer; color: #0b0f19; }
    </style>
</head>
<body>

    <div id="game-container">
        
        <div class="sidebar">
            <h2 style="color:#10b981; font-family:'VT323'; font-size:1.8rem;"><i class="fa-solid fa-headset"></i> SCAM CALL CENTER</h2>
            
            <div class="panel">
                <h3>💰 DAILY BALANCE</h3>
                <div style="font-family:'VT323'; font-size:2rem; color:#34d399;">$<span id="balance">0</span> / $500</div>
            </div>

            <div class="panel">
                <h3>📋 SCAM OBJECTIVES</h3>
                <p style="font-size:0.8rem; color:#cbd5e1; line-height:1.4;">
                    1. Hold <b>Mic button</b> & speak English.<br>
                    2. Claim PC has virus/trojan.<br>
                    3. Sell Antivirus ($80) via AnyViewer.<br>
                    4. Copy card from chat, charge via Credit Card app!
                </p>
            </div>

            <div class="panel">
                <h3>🛠️ APPLICATIONS</h3>
                <div class="app-grid">
                    <button class="app-icon" onclick="openApp('credit')"><i class="fa-solid fa-credit-card"></i><span>Credit Card</span></button>
                    <button class="app-icon" onclick="openApp('anyviewer')"><i class="fa-solid fa-desktop"></i><span>AnyViewer</span></button>
                    <button class="app-icon" onclick="openApp('crypto')"><i class="fa-brands fa-bitcoin"></i><span>Crypto</span></button>
                    <button class="app-icon" onclick="openApp('giftcard')"><i class="fa-solid fa-gift"></i><span>Gift Cards</span></button>
                    <button class="app-icon" onclick="openApp('scamazon')"><i class="fa-solid fa-box"></i>
