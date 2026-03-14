# Pharmacisco Kullanım Kılavuzu

Pharmacisco, eczaneler için ilaç kullanım talimatlarını hastaların anlayabileceği görsel etiketlere dönüştüren ve bu etiketleri termal yazıcılardan pratik bir şekilde basılmasını sağlayan entegre bir otomasyon çözümüdür.

---

## 🚀 1. Kurulum ve İlk Çalıştırma

### 1.1 Uygulamayı Başlatma
* Uygulamamızı kurduktan sonra masaüstünüzdeki **Pharmacisco** simgesine tıklayarak başlatın.
* **Lisans Doğrulaması:** Program ilk açıldığında tarafınıza iletilen "Müşteri Adı" ve "Lisans Anahtarı" (License Key) girilmelidir. Lütfen ilk aktivasyon sırasında bilgisayarınızın internete bağlı olduğundan emin olun.
* **Eczane Profil Ayarları:** Aktivasyon sonrasında sizden Eczane Adı, Telefon, Adres gibi bilgileri girmeniz istenecektir. Bu bilgiler yazdırılan etiketlerin alt kısmında hastaya gösterilecek olan iletişim bilgileridir (Bu bilgileri daha sonra **Ayarlar** menüsünden değiştirebilirsiniz).

### 1.2 Chrome Eklentesinin (Extension) Kurulması
Medula veya e-Nabız sistemlerinden verileri doğrudan çekebilmek için Pharmacisco Chrome Eklentisi gerekmektedir:
1. Google Chrome (veya Microsoft Edge/Brave) tarayıcınızı açın.
2. Adres çubuğuna `chrome://extensions/` yazın.
3. Sağ üst köşeden **"Geliştirici Modu" (Developer Mode)** seçeneğini açın.
4. **"Sıkıştırılmamış Öğeyi Yükle" (Load Unpacked)** butonuna tıklayın ve uygulamanızın bulunduğu dizindeki `chrome_extension` klasörünü seçin.
5. Pharmacisco ikonu (şırınga veya hap simgesi) tarayıcı çubuğunuza yerleşecektir. Artık Medula entegrasyonuna hazırsınız!

---

## 🛠️ 2. Menüler ve İşlevleri

Pharmacisco, sol pencerendeki dikey menü paneli üzerinden farklı işlemleri saniyeler içinde halletmenizi sağlar:

### 2.1 🏷️ Manuel Etiket 
Elinizdeki ilacı veya reçeteyi fiziksel olarak klavyeden girerek etiket basmanızı sağlar.
* **Kullanımı:** Barkod okutucu ile "İlaç Arama" kutusuna okutma yaptığınızda veya elle ismini yazdığınızda, ilaç veritabanından çekilir. Ekranda kaç günde kaç doz kullanılacağı (`Günde`, `Kez`, `Doz` gibi parametreler) pratik butonlarla (Tok/Aç) seçilip `[ Yazdır ]` butonuna basılır. Etiketin sağ tarafta gerçek zamanlı bir önizlemesi mevcuttur.

### 2.2 💊 İlaç Yönetimi (TR) & İlaç Yönetimi (EN)
Sistemin beynidir. İlaç bilgilerinin, kullanım şekillerinin ve uyarıların bulunduğu yerel veritabanınızdır.
* **TR (Türkçe) Yönetimi:** İlaçların ana kayıtlarının yapıldığı sekmedir. Yeni ilaç ekleyebilir, mevcutları silebilir veya doz bilgilerini değiştirebilirsiniz. `Tercüme Yenile` butonu sayesinde Türkçe olarak girdiğiniz metinler, **otomatik olarak** Google altyapısıyla İngilizce, Rusça, Arapça vb. dillere çevrilir. (Kısa süre içinde aktif olması beklenmektedir).
* **EN (İngilizce) Yönetimi:** Eğer otomatik oluşturulan İngilizce içerikler (Kısa Talimat EN, Detaylı Tarif EN) tıbbi olarak yanlış geldiyse, doğrudan bu ekrandan **sadece İngilizce çeviriyi** düzeltip kaydedebilirsiniz.

### 2.3 🌐 Otomatik Browser
Masaüstü uygulaması ile Google Chrome'un **birlikte (anlık) çalıştığı** devrimsel bir özelliktir. 
* **Nasıl Çalışır?** Medula veya Reçetem sistemi üzerinde reçetenizi açtığınızda arka planda kurduğunuz Chrome eklentisi doktorun yazdığı ilaçları, barkodları ve doz talimatlarını çeker. Siz hiçbir tuşa basmadan, Pharmacisco bu ilaçları yakalar ve "Otomatik Browser" penceresindeki tabloya listeler. 
* **Doktor Talimatı vs Veritabanı:** Sayfanın hemen sol üstünde **"Etikete Yazılacak Talimat Kaynağı"** seçim menüsü vardır. Eğer bunu *Doktor Talimatı (Medula)* yaparsanız, doktor 1x3 yazmış olsa dahi etikette birebir çıkan talimat Medula'dan okunan ham halidir. *Veritabanı: Kısa* veya *Veritabanı: Uzun* seçenekleriyle standart eczane çıktılarınızı verebilirsiniz.
* Tablodan basmak istediğiniz ilaçları seçip hızlıca **Hepsini Yazdır** diyerek zamandan büyük tasarruf edersiniz.

### 2.4 📸 Otomatik (OCR)
Dijital ortamda olmayan, whatsapp'tan fotoğraf olarak gelen veya önünüzdeki fiziki kağıt reçeteler için tasarlanmıştır. Görseldeki metni analiz edip eczacının zaman kaybetmeden ilacı işlemesini sağlar.

### 2.5 ⚙️ Ayarlar
* **Genel Bilgiler:** Eczane Adı, Telefon numarası, Eczacı İsmi bu kısımdan dilediğiniz zaman güncellenebilir.
* **Yazıcı Ayarları:** Etiketlerin çıktığı makine (Termal Printer vb.) bu menüden seçilir. Eğer yazılarınız etiketin dışına taşıyor veya küçük kalıyorsa, **"Etiket Genişliği"** ve **"Etiket Yüksekliği (mm)"** ayarlarını değiştirerek kalibrasyon sağlayabilirsiniz.
* **Lisans Durumu:** Programın geçerlilik süresini (`Geçerlilik Tarihi`) ve kime ait olduğunu görüntüleyebilirsiniz.

---

## 💡 İpuçları & Sorun Giderme

* **Sorun:** Otomatik Browser'a ilaçlar düşmüyor.
  **Çözüm:** 
  1. Pharmacisco programını açtığınızda Sol Tepsisinde "Otomatik Browser" penceresindeyken bağlantının portlarını dinlediğinden emin olun.
  2. Google Chrome eklentilerinden Pharmacisco eklentisinin Açık konumda (Aktif/Toggle mavi) olduğunu kontrol edin. 
  3. Medula sayfasında ilaçlar listelendikten sonra Eklenti butonuna 1 defa basarak aktarım tetiklemesi yapın.
  
* **Sorun:** Yazdırınca boş kağıt çıktı veriyor.
  **Çözüm:** "Ayarlar" sayfasında yanlış bir Default (varsayılan) Windows yazıcısı seçili kalmış olabilir. Ayarlar bölümünden Etiket cihazınızın (Örn: Xprinter, Zebra vb.) adını kesinlikle doğru bir şekilde seçtiğinize emin olun. Boyutların genellikle 60x40mm veya 50x30mm olmasına dikkat edin.

---
Yazılımın tadını çıkarın! Değerli geri dönüşleriniz veya geliştirilmesi gereken özellikler için destek hattımız üzerinden bizlerle de iletişime geçebilirsiniz.
