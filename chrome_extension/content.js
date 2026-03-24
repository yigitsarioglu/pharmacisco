// This script runs on the page when triggered

function scrapeData() {
    let data = {
        patient_name: "Bilinmeyen Hasta",
        drugs: []
    };

    try {
        // 1. Hasta Adı / Soyadı Çıkarımı
        // Medula'da Reçete Sahibi Adı: f:t15 ve f:t16 id'li span'lerde tutulur.
        let nameSpan1 = document.getElementById("f:t15");
        let nameSpan2 = document.getElementById("f:t16");
        
        // Eğer f:t15 yoksa (Teslim alan farklı vs), f:text40 ve f:text39'a da bakabiliriz.
        if (!nameSpan1) {
            nameSpan1 = document.getElementById("f:text40");
            nameSpan2 = document.getElementById("f:text39");
        }

        if (nameSpan1 && nameSpan2) {
            data.patient_name = (nameSpan1.innerText.trim() + " " + nameSpan2.innerText.trim()).trim();
        }

        // 2. İlaçlar, Barkodlar ve Kullanım Dozajları (f:tbl1)
        // Tablodaki her satırın indeksini dolaşıyoruz (0'dan başlayarak boş satır bulana kadar)
        let i = 0;
        while (true) {
            let barcodeInput = document.getElementById(`f:tbl1:${i}:t1`);
            
            // Eğer Barkod inputu yoksa ilaç listesinin sonuna gelmişizdir.
            if (!barcodeInput) break;

            let barcode = barcodeInput.value ? barcodeInput.value.trim() : "";
            
            // Barkod hücresi boşsa, liste burada bitiyordur (silinmiş/boş bırakılmış satırlar olabilir)
            if (barcode === "") {
                i++;
                continue;
            }

            let nameSpan = document.getElementById(`f:tbl1:${i}:t6`);
            let name = nameSpan ? nameSpan.innerText.trim() : "Bilinmeyen İlaç";

            // Kullanım (Periyot / Doz) Çıkarımı
            // Örnek: t5 (Periyot Miktarı: 1), m1 (Periyot Tipi: Günde), t3 (Hangi sıklıkla: 2), t4 (Doz: 1,0)
            let periodAmountInput = document.getElementById(`f:tbl1:${i}:t5`);
            let periodTypeSelect = document.getElementById(`f:tbl1:${i}:m1`);
            let freqInput = document.getElementById(`f:tbl1:${i}:t3`);
            let doseInput = document.getElementById(`f:tbl1:${i}:t4`);
            let expiryInput = document.getElementById(`f:tbl1:${i}:t10`); // Bitiş Tarihi

            let usageStr = "";
            let periodAmount = "1";
            let periodType = "Günde";
            let freqStr = "1";
            let doseStr = "1.0";
            let expiryDate = "";

            if (expiryInput) {
                expiryDate = expiryInput.innerText.trim() || expiryInput.value || "";
            }

            if (periodAmountInput && periodTypeSelect && freqInput && doseInput) {
                periodAmount = periodAmountInput.value || "1";
                // Select elementinden seçili metni bulalım
                if (periodTypeSelect.selectedIndex >= 0) {
                    periodType = periodTypeSelect.options[periodTypeSelect.selectedIndex].text;
                }
                
                freqStr = freqInput.value || "1";       // Kaç kere (Örn: 2)
                doseStr = doseInput.value || "1.0";     // Kaç adet (Örn: 1,0)
                
                // Virgüllü ise daha temiz gözükmesi için örneğin 1,0 -> 1 yapabiliriz, ama şimdilik orijinal metni koruyoruz.
                usageStr = `${periodAmount} ${periodType} ${freqStr} x ${doseStr} doz`;
            }

            // Listeye it
            data.drugs.push({
                name: name,
                barcode: barcode,
                usage: usageStr,
                freq: freqStr,
                dose: doseStr,
                period_type: periodType,
                expiry_date: expiryDate
            });

            i++;
        }

    } catch (e) {
        console.error("Scraping error:", e);
    }

    // Eğer DOM bazlı aramada hiçbir şey bulunamazsa, eski usul regex fallback yapılabilir, 
    // Ancak orijinal Medula sayfasında yukarıdaki ID'ler standarttır.

    return data;
}

// Automatically trigger scrapeData and return
scrapeData();
