# Jarvis - Yerel Sesli ve Yazılı Masaüstü Asistanı

Python ve Electron (Node.js) altyapısıyla geliştirilmiş; Vosk ses tanıma kütüphanesi ve Ollama (yerel LLM) desteğiyle tamamen çevrimdışı (lokal) olarak çalışan kişisel masaüstü asistan uygulamasıdır. İnternet bağımlılığı olmadan, verilerinizi dış sunuculara göndermeden bilgisayarınızı kontrol etmenizi ve yapay zeka ile sohbet etmenizi sağlar.

## Özellikler

* **Çift Modlu Etkileşim:** İsterseniz sesli komutlarla (Vosk), isterseniz arayüzdeki modern metin kutusu üzerinden klavyeyle komut/soru iletebilirsiniz.
* **Medya ve Uygulama Yönetimi:** Spotify üzerinden şarkı aratma/çalma, YouTube'da video aratıp oynatma, hesap makinesi çalıştırma ve anlık saat bilgisi alma.
* **Ses ve Oynatma Kısayolları:** Ses açma/kısma, müziği durdurma/başlatma ve sonraki parçaya atlama komutları.
* **Yerel Yapay Zeka Desteği:** Klasik komutlar dışındaki tüm soru ve sohbet taleplerinizi Ollama (`phi3`) üzerinden tamamen yerel olarak yanıtlar.
* **Şık ve Modern Arayüz:** Karanlık temalı, özel animasyonlu ve log takip paneline sahip Electron pencere tasarımı.

---

## Kurulum Adımları

Projeyi bilgisayarınıza kurup çalıştırmak için aşağıdaki adımları sırasıyla takip edebilirsiniz:

### 1. Projeyi Klonlayın veya İndirin

Terminal veya komut istemcisini açarak projeyi bilgisayarınıza indirin ve klasörün içine girin.

### 2. Vosk Ses Modelini Ekleyin

Sesli komut özelliğinin çalışabilmesi için **Vosk** ses tanıma modeline ihtiyacınız var.

1. Vosk Modelleri Sayfasından Türkçe bir model indirin (Örn: `vosk-model-small-tr-...`).
2. İndirdiğiniz klasörün adını `model` olarak değiştirin ve projenin ana dizinine (`jarvis/model`) atın.

### 3. Node.js Bağımlılıklarını Yükleyin

Proje klasöründe terminali açın ve gerekli paketleri yüklemek için `npm install` komutunu çalıştırın.

### 4. Yerel Yapay Zeka İçin Ollama'yı Hazırlayın

Yapay zeka soru-cevap özelliğinin çalışması için bilgisayarınızda Ollama kurulu olmalıdır:

1. Ollama Resmi Sitesi üzerinden uygulama kurulumunu yapın.
2. Terminal üzerinden kullanmak istediğiniz modeli `ollama run phi3` komutuyla indirin.
3. Ollama arka plan servisinin açık olduğundan emin olun.

---

## Uygulamayı Başlatma

Her şey hazır olduktan sonra projeyi başlatmak için ana dizinde `npm start` komutunu çalıştırmanız yeterlidir.
