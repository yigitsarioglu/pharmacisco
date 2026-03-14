Nasl Çözülür? (InnoSetup Doğru Ayarı)
Eğer Inno Setup'ı Sihirbaz (Wizard) üzerinden kullanıyorsanız:

Application Files (Uygulama Dosyaları) adımına geldiğinizde en üstte Main Executable olarak dist\Pharmacisco\Pharmacisco.exe dosyasını gösterin.
Nghemen altındaki listede "Add folder..." (Klasör Ekle) adında bir buton göreceksiniz. Oraya tıklayın.
Çıkan ekranda projenizin altındaki dist\Pharmacisco klasörünün kendisini (ana klasörü) seçin.
Çıkan soruda "Alt klasörleri de dahil edeyim mi? (Include subfolders?)" diye soracaktır. Kesinlikle Evet (Yes) diyin.
Bittiğinde alttaki kutuda C:\...dist\Pharmacisco\* şeklinde gözükecektir. Artık Setup alabilirsiniz


-----
notes: en son olak scripte şu alttakini ekleyin. yoksa lisans aktivasyonunu engelliyor. (böylece kurulan klasör "Okuma-Yazma" izinli çıkacak ve programınız Lisans aktivasyonu sırasında "İzin engellendi" hatası vermeyecek.)

[Dirs]
Name: "{app}"; Permissions: users-modify


