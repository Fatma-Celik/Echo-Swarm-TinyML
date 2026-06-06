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

