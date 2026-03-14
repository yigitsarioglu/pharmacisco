# PHARMACISCO ECZANE ETİKET PROGRAMI

Çalıştırmak için önce virtual environment'ı aktif edin, daha sonra terminalden bu komutu yazın:

Windows için:
$ .\venv\Scripts\activate

Daha sonra programı başlatın:
$ python main.py 

----------------------------------------------------


Yardımcı komutlar (Venv aktifken çalıştırın):

- otomatik çeviri için: python utils/translate_db.py
- lisans üretmek için: python utils/generate_license.py
- lisans doğrulamak için: python utils/verify_license.p
- veritabanı şeması güncellemesi için: python utils/update_db_schema.py 
- programı derlemek için (exe dosyası oluşturmak için): python utils/build.bat   


Virtual environment kurulumu:
pip install -r requirements.txt