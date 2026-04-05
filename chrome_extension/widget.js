(function() {
    // If widget already exists, toggle its visibility
    const existingWidget = document.getElementById("pharmacisco-floating-widget");
    if (existingWidget) {
        existingWidget.style.display = existingWidget.style.display === "none" ? "block" : "none";
        return;
    }

    // Create Widget Container
    const widget = document.createElement("div");
    widget.id = "pharmacisco-floating-widget";
    widget.style.position = "fixed";
    widget.style.bottom = "20px";
    widget.style.right = "20px";
    widget.style.width = "320px";
    widget.style.zIndex = "999999";
    widget.style.fontFamily = "'Inter', sans-serif";
    widget.style.background = "#f4f6F8";
    widget.style.color = "#333";
    widget.style.boxShadow = "0 10px 25px rgba(0,0,0,0.2)";
    widget.style.borderRadius = "12px";
    widget.style.overflow = "hidden";
    widget.style.transition = "opacity 0.2s ease";

    // Inner HTML Structure
    widget.innerHTML = `
        <div id="pfw-header" style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px; cursor: move; display: flex; justify-content: space-between; align-items: center; user-select: none;">
            <div style="pointer-events: none;">
                <h3 style="margin: 0; font-size: 16px; font-weight: 700;">Pharmacisco</h3>
                <p style="margin: 0; font-size: 11px; opacity: 0.9;">E-Reçeteyi Aktar</p>
            </div>
            <div>
                <button id="pfw-minimize" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; font-weight: bold; outline: none; margin-right: 5px;" title="Küçült/Büyüt">&minus;</button>
                <button id="pfw-close" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; font-weight: bold; outline: none;" title="Kapat">&times;</button>
            </div>
        </div>
        <div id="pfw-content" style="padding: 20px; text-align: center;">
            <button id="pfw-btn" style="width: 100%; padding: 12px; background: white; color: #059669; border: 2px solid #059669; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(5,150,105,0.1); outline: none;">Aktarımı Başlat</button>
            <div id="pfw-status" style="margin-top: 15px; font-size: 13px; min-height: 20px; padding: 10px; border-radius: 6px; font-weight: 600; display: none;"></div>
        </div>
    `;

    // Button Hover Effects
    const pfwBtn = widget.querySelector("#pfw-btn");
    pfwBtn.addEventListener("mouseover", () => {
        pfwBtn.style.backgroundColor = "#059669";
        pfwBtn.style.color = "white";
    });
    pfwBtn.addEventListener("mouseout", () => {
        pfwBtn.style.backgroundColor = "white";
        pfwBtn.style.color = "#059669";
    });

    document.body.appendChild(widget);

    // Draggable Logic
    let isDragging = false;
    let offsetX, offsetY;
    const header = document.getElementById("pfw-header");
    
    header.addEventListener("mousedown", (e) => {
        isDragging = true;
        offsetX = e.clientX - widget.getBoundingClientRect().left;
        offsetY = e.clientY - widget.getBoundingClientRect().top;
    });

    document.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        widget.style.left = (e.clientX - offsetX) + "px";
        widget.style.top = (e.clientY - offsetY) + "px";
        widget.style.bottom = "auto";
        widget.style.right = "auto";
    });

    document.addEventListener("mouseup", () => {
        isDragging = false;
    });

    // Minimize button
    document.getElementById("pfw-minimize").addEventListener("click", () => {
        const content = document.getElementById("pfw-content");
        const btn = document.getElementById("pfw-minimize");
        if (content.style.display === "none") {
            content.style.display = "block";
            btn.innerHTML = "&minus;";
        } else {
            content.style.display = "none";
            btn.innerHTML = "+";
        }
    });

    // Close button
    document.getElementById("pfw-close").addEventListener("click", () => {
        widget.style.display = "none";
    });

    // Scraping Function (from old content.js)
    function scrapeData() {
        let data = { patient_name: "Bilinmeyen Hasta", drugs: [] };
        try {
            let nameSpan1 = document.getElementById("f:t15");
            let nameSpan2 = document.getElementById("f:t16");
            if (!nameSpan1) { nameSpan1 = document.getElementById("f:text40"); nameSpan2 = document.getElementById("f:text39"); }
            if (nameSpan1 && nameSpan2) { data.patient_name = (nameSpan1.innerText.trim() + " " + nameSpan2.innerText.trim()).trim(); }

            let i = 0;
            while (true) {
                let barcodeInput = document.getElementById(`f:tbl1:${i}:t1`);
                if (!barcodeInput) break;
                let barcode = barcodeInput.value ? barcodeInput.value.trim() : "";
                if (barcode === "") { i++; continue; }

                let nameSpan = document.getElementById(`f:tbl1:${i}:t6`);
                let name = nameSpan ? nameSpan.innerText.trim() : "Bilinmeyen İlaç";

                let periodAmountInput = document.getElementById(`f:tbl1:${i}:t5`);
                let periodTypeSelect = document.getElementById(`f:tbl1:${i}:m1`);
                let freqInput = document.getElementById(`f:tbl1:${i}:t3`);
                let doseInput = document.getElementById(`f:tbl1:${i}:t4`);
                let expiryInput = document.getElementById(`f:tbl1:${i}:t10`);

                let usageStr = "";
                let periodAmount = "1";
                let periodType = "Günde";
                let freqStr = "1";
                let doseStr = "1.0";
                let expiryDate = "";

                if (expiryInput) { expiryDate = expiryInput.innerText.trim() || expiryInput.value || ""; }

                if (periodAmountInput && periodTypeSelect && freqInput && doseInput) {
                    periodAmount = periodAmountInput.value || "1";
                    if (periodTypeSelect.selectedIndex >= 0) { periodType = periodTypeSelect.options[periodTypeSelect.selectedIndex].text; }
                    freqStr = freqInput.value || "1";
                    doseStr = doseInput.value || "1.0";
                    usageStr = `${periodAmount} ${periodType} ${freqStr} x ${doseStr} doz`;
                }

                data.drugs.push({ name: name, barcode: barcode, usage: usageStr, freq: freqStr, dose: doseStr, period_type: periodType, expiry_date: expiryDate });
                i++;
            }
        } catch (e) { console.error("Scraping error:", e); }
        return data;
    }

    // Action Logic
    document.getElementById("pfw-btn").addEventListener("click", async () => {
        const status = document.getElementById("pfw-status");
        status.innerText = "Sayfa taranıyor...";
        status.style.display = "block";
        status.style.background = "#fffbeb";
        status.style.color = "#b45309";
        status.style.border = "1px solid #fcd34d";

        try {
            let data = scrapeData();

            if (!data || data.drugs.length === 0) {
                status.innerText = "İlaç/Barkod bulunamadı.";
                status.style.background = "#fef2f2";
                status.style.color = "#991b1b";
                status.style.border = "1px solid #ef4444";
                return;
            }

            status.innerText = `Bulunan: ${data.drugs.length} İlaç.\nGönderiliyor...`;

            let response = await fetch("http://localhost:5500/print", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                status.innerText = "Başarılı! Uygulamaya aktarıldı.";
                status.style.background = "#ecfdf5";
                status.style.color = "#065f46";
                status.style.border = "1px solid #10b981";
            } else {
                throw new Error("App Response Error");
            }
        } catch (err) {
            status.innerText = "Hata: Uygulama açık mı?\n(localhost:5500)";
            status.style.background = "#fef2f2";
            status.style.color = "#991b1b";
            status.style.border = "1px solid #ef4444";
        }
    });

})();
