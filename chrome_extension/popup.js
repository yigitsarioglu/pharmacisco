document.getElementById("btnScan").addEventListener("click", async () => {
    const status = document.getElementById("status");
    status.innerText = "Sayfa taranıyor...";
    status.className = "";

    try {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Execute script
        let results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js']
        });

        // 'results' is array of {frameId, result}
        let data = results[0].result;

        if (!data || data.drugs.length === 0) {
            status.innerText = "İlaç/Barkod bulunamadı.";
            status.className = "error";
            return;
        }

        status.innerText = `Bulunan: ${data.drugs.length} İlaç.\nGönderiliyor...`;

        // Send to Local App
        try {
            let response = await fetch("http://localhost:5500/print", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                status.innerText = "Başarılı! Uygulamaya aktarıldı.";
                status.className = "success";
            } else {
                throw new Error("App Response Error");
            }
        } catch (err) {
            status.innerText = "Hata: Uygulama açık mı?\n(localhost:5500)";
            status.className = "error";
        }

    } catch (err) {
        console.error(err);
        status.innerText = "Komut Hatası: " + err.message;
        status.className = "error";
    }
});
