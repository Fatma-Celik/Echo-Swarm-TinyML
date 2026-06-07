# Echo Swarm: Afet Yönetimi İçin Sürü Zekası Tabanlı Akustik Arama Kurtarma Ağı 🐝📡

Bu proje, deprem sonrası enkaz altında kalan kazazedelerin konumunu, görsel kısıtlılıkların olduğu tozlu ve karanlık ortamlarda akustik verilerle tespit edebilen modüler bir sürü sistem altyapısıdır. 

Geleneksel ve pahalı arama-kurtarma sistemlerinin aksine, kısıtlı işlemcilerde (ESP32) çalışabilen hafif yapay zeka modelleri (TinyML), altyapısız düşük gecikmeli kablosuz haberleşme (ESP-NOW) ve 3 boyutlu konum kestirimi (TDOA) kullanılarak "süper kulak" mantığıyla çalışan dağıtık bir sistem tasarlanmıştır.

<img width="1927" height="816" alt="ChatGPT Image 6 Haz 2026 17_05_24" src="https://github.com/user-attachments/assets/b1f48797-3bda-439c-ba65-5d5524b09114" />

## 🎓 Disiplinler Arası Yaklaşım

  Proje, üç temel mühendislik disiplininin bütünleşik çalışmasıyla bir afet teknolojisi prototipine dönüşmüştür:
* **Bilgisayar Mühendisliği:** İnsan sesi tespiti için TinyML model tasarımı, ESP-NOW sürü haberleşme altyapısı, 3B TDOA konumlandırma algoritmaları ve karar destek mobil arayüzü (Flutter).
* **Mekatronik Mühendisliği:** "Hacıyatmaz" (self-righting) küresel mekanizma tasarımı, ESP32 ve MAX9814 mikrofon dizilimli dairesel PCB mimarisi ve Unity 3B Dijital İkiz simülasyonu.
* **Endüstri Mühendisliği:** Sınırlı sensörlerin enkaz üzerindeki en verimli dağılımı için MCLP (Maximal Covering Location Problem) optimizasyon modeli ve risk analizi.

## 🚀 Sistem Mimarisi

Sistem, dağıtık düğüm mimarisi (Master-Slave) ve yarı-merkezi bir karar yapısı üzerine inşa edilmiştir:

1. **Algılama Katmanı:** Sensörler ortamı dinler ve ses eşiği aşıldığında sistemi uyandırır.
2. **Yapay Zeka Katmanı (Uçta İşleme):** Mikrofonlardan gelen veriler Log-Mel Spektrogram'a dönüştürülür ve hafif CNN modeli ile insan sesi (HUMAN) sınıflandırması yapılır.
3. **İletim Katmanı:** ESP-NOW protokolü ile zaman damgası ve güven skoru içeren "Olay Tetikleyici Paketler" ana düğüme (Master) iletilir.
4. **Karar ve Sunum Katmanı:** Master düğüm TDOA ile konumu hesaplar ve Flutter tabanlı çapraz platformlu mobil arayüze aktarır.


<img width="1393" height="499" alt="image" src="https://github.com/user-attachments/assets/a44b0b32-afe7-409d-9b64-87b98400b9c3" />


## 🧠 Uçta Yapay Zeka (TinyML) & Sinyal İşleme

Ham ses verileri doğrudan işlenmez; hesaplama maliyetini düşürmek ve örüntü tanımayı güçlendirmek amacıyla 1.5 saniyelik pencereler halinde **Log-Mel Spektrogram** dönüşümü uygulanır. 



### "Rubble-Robust" (Enkaza Dayanıklı) Yaklaşım
Arama-kurtarma senaryosunda can kaybı riskini önlemek için en kritik metrik **İnsan Sesini Kaçırmama (HUMAN recall)** oranıdır. Temiz verilerle eğitilen baseline model; düşük geçiren filtreleme, beyaz gürültü ve oda yankısı (reverberation) gibi tekniklerle zorlu saha koşullarına adapte edilmiştir. Eşik değeri canlı tespiti lehine kaydırılarak yanlış pozitif toleransı artırılmış, ancak enkaz altında maksimum doğruluk hedeflenmiştir.

<img width="1404" height="1182" alt="page_10_img_1_X36" src="https://github.com/user-attachments/assets/ecfe68e7-d833-4aa1-9259-b8c58ac1fd60" />

## 📡 Donanım ve ESP-NOW Sürü Haberleşmesi

Altyapısız ve modemsiz ortamlarda düğümlerin birbiriyle hızlı haberleşmesi için **ESP-NOW** protokolü kullanılmıştır.
* C++ `struct` yapıları ve `__attribute__((packed))` kullanılarak payload optimizasyonu yapılmıştır.
* Paket kayıplarını önlemek için ACK (Onay Mekanizması) kodlanmıştır.
* Master düğüm, ilk algılayan veya sese en yakın düğümü belirleyip sonucu tüm ağa `Broadcast` olarak yayınlar.

**Donanım Pin Konfigürasyonu:**
| Bileşen | ESP32-WROOM-32D Pin |
| :--- | :--- |
| Mikrofon Modülü OUT | GPIO32 |
| Kırmızı LED (Kazanan/Ses Tespit) | GPIO26 |
| Sarı LED (Bekleme/Normal Durum) | GPIO27 |

<img width="1689" height="1268" alt="Proje" src="https://github.com/user-attachments/assets/457764e1-fd66-4b73-b534-3a1523f5d10b" />
<img width="1610" height="1209" alt="IMG_20260521_160220" src="https://github.com/user-attachments/assets/ae7c98f1-c6a0-4b55-aa71-9f0a05420a34" />
<img width="1474" height="828" alt="Ekran görüntüsü 2026-05-24 123206" src="https://github.com/user-attachments/assets/570ae6b5-a2c3-40fa-889f-87304c348ad4" />

https://github.com/user-attachments/assets/24017e9e-7946-4c98-887b-c52b082575a6
https://github.com/user-attachments/assets/8d05ecd7-b92d-4070-860c-36bdec64c74e

## 📱 TDOA Konumlandırma ve Karar Destek Arayüzü

Düzensiz sensör yerleşimlerinde ses kaynağının 3 boyutlu konumunu tahmin etmek için **TDOA (Zaman Farkı - Time Difference of Arrival)** modeli geliştirilmiştir. Veriler; saha ekiplerinin takip edebilmesi için harita destekli (OpenStreetMap), anlık sensör durumunu gösteren, çift yönlü sesli iletişim sunan **Flutter** tabanlı mobil uygulamaya aktarılır.
<p align="center">
<img width="615" height="450" alt="image" src="https://github.com/user-attachments/assets/00535a23-b14c-4f3e-a273-d5c7f31bd76d" />
<img width="615" height="454" alt="image" src="https://github.com/user-attachments/assets/fd0ed5a5-fccf-439b-863f-9c4fe957d289" />
<img width="555" height="256" alt="image" src="https://github.com/user-attachments/assets/f1e8ab76-8f12-4e14-89c9-7f5f98914202" />
<img width="614" height="460" alt="image" src="https://github.com/user-attachments/assets/627f3bba-122b-4347-afa5-2808dadac56f" />
<img width="612" height="397" alt="image" src="https://github.com/user-attachments/assets/abce712d-02c3-4243-9bca-6318eeb2afca" />
<img width="615" height="287" alt="image" src="https://github.com/user-attachments/assets/724f1826-dc40-438a-b4dc-8e3bd4585077" />
</p>

---

## 📂 Klasör Yapısı

* `/docs`: Projenin detaylı disiplinler arası final raporları (PDF).
* `/src/1_AI_TinyML`: Veri ön işleme (Log-Mel), model eğitimi (CNN) ve çıkarım (inference) Python scriptleri.
* `/src/2_ESP_NOW_Network`: ESP32 Master ve Slave (Node) cihazları için C++ / Arduino haberleşme kodları.
* `/models`: Eğitilmiş yapay zeka ağırlık dosyaları (özellikle `merged_human_nonhuman_rubble_best.pt`).
* `/demo_samples`: Yapay zeka modelini test etmek için örnek `.wav` formatında temiz ve enkaz boğukluğunda ses dosyaları.

## ⚙️ Kurulum ve Çalıştırma

### 1. Yapay Zeka Modelini Test Etme (Python)
Gerekli kütüphaneleri kurmak ve modeli örnek ses dosyalarıyla denemek için:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Temiz insan sesi testi
python src\1_AI_TinyML\infer_demo.py --wav demo_samples\nigens_quick_test\human\human_01_femaleSpeech.wav

# Enkaz benzeri boğuk insan sesi (Rubble) testi
python src\1_AI_TinyML\infer_demo.py --wav demo_samples\nigens_rubble_test\human\human_01_femaleSpeech_rubble.wav
