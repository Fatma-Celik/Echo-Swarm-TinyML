\# Echo Swarm 2 - Human Audio Detection



Bu repo, Echo Swarm 2 projesinde geliştirilen insan sesi / insan dışı ses ayrımı deneylerini, eğitilmiş modeli, örnek test seslerini ve sonuç görsellerini içerir.



\## Amaç



Kısa ses pencereleri üzerinden HUMAN / NON\_HUMAN ayrımı yapan hafif bir ses sınıflandırma modeli geliştirmek ve bu modeli daha sonra ESP32 tabanlı MVP sistemine taşımaktır.



\## En Önemli Model



`models/merged\_human\_nonhuman\_rubble\_best.pt`



Bu model, boğuk ve enkaz benzeri koşullarda insan sesini kaçırmama hedefiyle geliştirilmiş rubble-robust modeldir.



\## Kurulum



```powershell

python -m venv .venv

.venv\\Scripts\\activate

pip install -r requirements.txt


## Demo Inference

Veri setlerini indirmeden, repo icindeki egitilmis model ve demo WAV dosyalariyla hizli test:

```powershell
python src\infer_demo.py
```

Belirli bir WAV dosyasi ile test:

```powershell
python src\infer_demo.py --wav demo_samples\demo_samples\nigens_quick_test\human\human_01_femaleSpeech.wav
python src\infer_demo.py --wav demo_samples\demo_samples\nigens_quick_test\non_human\nonhuman_01_alarm.wav
python src\infer_demo.py --wav demo_samples\demo_samples\nigens_rubble_test\human\human_01_femaleSpeech_rubble.wav
```

Cikti olarak `Prediction`, `Human probability`, `Non-human probability` ve `Decision threshold` degerleri verilir.
