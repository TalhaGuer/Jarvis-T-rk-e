import os
import sys
import codecs
import json
import queue
import time
import re
import threading
import webbrowser
import requests
from datetime import datetime
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import pyautogui
import urllib.parse
import webview

# Türkçe karakter ve konsol kodlama bozulmalarını engelle
try:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
except Exception:
    pass

MODEL_PATH = "model"

if not os.path.exists(MODEL_PATH):
    print(f"HATA: Model klasörü bulunamadı: {MODEL_PATH}", file=sys.stderr)
    sys.exit(1)

model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

q = queue.Queue()
window_instance = None

def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def log_gonder(mesaj):
    print(mesaj, flush=True)
    if window_instance:
        try:
            window_instance.evaluate_js(f"arayuzuGuncelle('{mesaj}')")
        except:
            pass

def yerel_metin_temizle(ham_metin):
    temiz = ham_metin.lower().strip()
    temiz = re.sub(r'[^\w\s]', '', temiz)
    
    sozluk = {
        "carvis": "jarvis", "servis": "jarvis", "ceviz": "jarvis",
        "caniviz": "jarvis", "yarvis": "jarvis", "spotifay": "spotify",
        "spotay": "spotify", "sportify": "spotify", "potifay": "spotify"
    }
    for yanlis, dogru in sozluk.items():
        temiz = temiz.replace(yanlis, dogru)
    return temiz

def youtube_ac_ve_cal(aranan_video=""):
    try:
        if aranan_video:
            log_gonder(f"YouTube'da aratılıyor: {aranan_video}")
            encoded_query = urllib.parse.quote(aranan_video)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(url)
            time.sleep(3.0)
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.press('enter')
        else:
            log_gonder("YouTube açılıyor...")
            webbrowser.open("https://www.youtube.com")
    except Exception as e:
        log_gonder(f"YouTube hatası: {e}")

# Yerel Yapay Zeka (Ollama - Phi3 ile hızlı ve güvenli)
def yapay_zekaya_sor(soru):
    log_gonder(f"Düşünüyor: {soru}")
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "phi3",
            "prompt": soru,
            "stream": False
        }, timeout=90) # Zaman aşımı süresi uzatıldı
        
        if response.status_code == 200:
            cevap = response.json().get("response", "").strip()
            log_gonder(f"Cevap: {cevap}")
        else:
            log_gonder("Yapay zeka yanıt veremedi.")
    except requests.exceptions.ConnectionError:
        log_gonder("Hata: Ollama arka planda çalışmıyor! ('ollama serve' yazın)")
    except requests.exceptions.Timeout:
        log_gonder("Hata: Yapay zeka çok uzun sürdü (Zaman aşımı).")
    except Exception as e:
        log_gonder(f"AI Hatası: {e}")

# Ortak Komut ve Soru İşleme Mantığı
def komutlari_isle(text):
    text = yerel_metin_temizle(text)
    log_gonder(f"İşlenen: {text}")
    
    # 1. Ses Yükselt Komutları
    if any(w in text for w in ["sesi aç", "sesi yükselt", "ses yükselt", "sesi arttır"]):
        log_gonder("Komut: Ses yükseltiliyor")
        for _ in range(5): 
            pyautogui.press('volumeup')
            time.sleep(0.05)

    # 2. Ses Kıs Komutları
    elif any(w in text for w in ["sesi kıs", "sesi azalt", "ses düşür"]):
        log_gonder("Komut: Ses kısılıyor")
        for _ in range(5): 
            pyautogui.press('volumedown')
            time.sleep(0.05)

    # 3. Net Durdur Komutu
    elif any(w in text for w in ["durdur", "beklet", "sus", "duraklat", "stop"]):
        if "devam" not in text:
            log_gonder("Komut: Müzik durduruldu")
            pyautogui.press('playpause')
            time.sleep(0.5)

    # 4. Net Başlat / Devam Et Komutu
    elif any(w in text for w in ["devam et", "oynat", "başlat", "çalsın"]):
        if not any(w in text for w in ["spotify", "şarkı", "müzik", "youtube", "video"]):
            log_gonder("Komut: Müzik devam ettiriliyor")
            pyautogui.press('playpause')
            time.sleep(0.5)

    # 5. Şarkıyı Geç Komutu
    elif any(w in text for w in ["geç", "sonraki", "atla"]):
        log_gonder("Komut: Sonraki şarkıya geçildi")
        pyautogui.press('nexttrack')
        time.sleep(0.5)

    # 6. YouTube Komutları
    elif any(w in text for w in ["youtube", "video", "izle"]):
        if not any(w in text for w in ["spotify", "şarkı"]):
            log_gonder("Komut: YouTube işleniyor...")
            aranan_video = ""
            for keyword in ["youtube aç", "youtube", "video aç", "video", "izle"]:
                if keyword in text:
                    parca = text.split(keyword)[-1].strip()
                    parca = parca.replace("aç", "").replace("izle", "").replace("bana", "").strip()
                    if parca:
                        aranan_video = parca
                        break
            t_yt = threading.Thread(target=youtube_ac_ve_cal, args=(aranan_video,))
            t_yt.start()

    # 7. Spotify Komutları
    elif any(w in text for w in ["spotify", "müzik", "çal", "aç"]):
        if not any(w in text for w in ["not defteri", "tarayıcı", "hesap", "ses", "youtube", "video"]):
            log_gonder("Komut: Spotify açılıyor...")
            aranan_muzik = ""
            for keyword in ["spotify aç", "spotify", "çal", "aç"]:
                if keyword in text:
                    parca = text.split(keyword)[-1].strip()
                    parca = parca.replace("şarkıyı", "").replace("şarkı", "").replace("çal", "").replace("aç", "").strip()
                    if parca:
                        aranan_muzik = parca
                        break
            
            os.system("start spotify")
            time.sleep(2.0)
            if aranan_muzik:
                log_gonder(f"Aratılıyor: {aranan_muzik}")
                encoded_query = urllib.parse.quote(aranan_muzik)
                os.system(f"start spotify:search:{encoded_query}")
                time.sleep(2.5)
                pyautogui.press('enter')
                time.sleep(1.0)
                pyautogui.press('space')
            else:
                pyautogui.press('space')

    # 8. Diğer Araçlar
    elif "saat" in text:
        zaman = datetime.now().strftime("%H:%M")
        log_gonder(f"Saat: {zaman}")
        pyautogui.write(f"Saat: {zaman}", interval=0.05)

    elif "hesap makinesi" in text:
        log_gonder("Hesap Makinesi açılıyor")
        os.system("calc")

    # 9. Hiçbiri Değilse Yapay Zekaya Soru Olarak Gönder
    else:
        threading.Thread(target=yapay_zekaya_sor, args=(text,), daemon=True).start()

class Api:
    def yazili_komut_isle(self, metin):
        threading.Thread(target=komutlari_isle, args=(metin,), daemon=True).start()

def ses_dinleme_motoru():
    log_gonder("Sistem aktif, dinliyor...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                ham_text = result.get("text", "").strip()
                
                if ham_text:
                    text = yerel_metin_temizle(ham_text)
                    log_gonder(f"Duyulan: {text}")
                    
                    if "jarvis" in text:
                        log_gonder("Komut algılandı!")
                        temiz_komut = text.replace("jarvis", "").strip()
                        komutlari_isle(temiz_komut)

if __name__ == '__main__':
    t = threading.Thread(target=ses_dinleme_motoru, daemon=True)
    t.start()

    api = Api()
    html_yolu = os.path.abspath("index.html")
    window_instance = webview.create_window("Jarvis Asistan", f"file:///{html_yolu}", width=460, height=590, resizable=False, js_api=api)
    webview.start()