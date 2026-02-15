// This script runs on the page when triggered

function scrapeData() {
    let data = {
        patient_name: "Bilinmeyen Hasta",
        drugs: []
    };

    // 1. Try to find Patient Name
    // Strategy: Look for specific keywords or just generic 'Adı' labels
    // This part matches the User's OCR image structure somewhat
    // 1. Try to find Patient Name
    // Refined to avoid "Dr. Adı/Soyadı"
    try {
        let bodyText = document.body.innerText;
        // Search specifically for lines starting with Hasta or labels
        // The mock has: "Hasta Adı Soyadı :"
        // The real Medula usually has "Hasta Adı Soyadı" or "TC Kimlik No" nearby.

        // Regex Lookbehind/heuristic:
        // Match "Hasta" followed by optional "Adı/Soyadı" then ":" then capture name
        let nameMatch = bodyText.match(/Hasta\s*(?:Adı|Türü|Bilgisi)?[^:]*[:]\s*([A-ZÇĞİÖŞÜ\s]+)/i);

        // Sometimes it's "Hasta Adı Soyadı : NAME" 
        if (nameMatch) {
            data.patient_name = nameMatch[1].trim();
        } else {
            // Fallback: look for generic "Adı Soyadı" BUT exclude if preceded by "Dr." or "Hekim"
            // This is harder with regex alone on raw text. 
            // Let's assume the previous regex works for "Hasta ... :"
            data.patient_name = "Bilinmeyen Hasta (Bulunamadı)";
        }

        // Cleanup: remove "Normal" or other distraction if it grabbed the wrong field
        if (data.patient_name === "Normal") {
            // It grabbed "Hasta Türü : Normal"
            // Try again for name specifically
            let nameMatch2 = bodyText.match(/Hasta\s*Adı\s*Soyadı\s*[:]\s*([A-ZÇĞİÖŞÜ\s]+)/i);
            if (nameMatch2) data.patient_name = nameMatch2[1].trim();
        }

    } catch (e) {
        console.log("Error extracting name", e);
    }

    // 2. Try to find Drugs (Barcodes)
    // Heuristic: Turkish Pharma barcodes are 13 digits, often starting with 869
    // We walk through all elements/text to find these numbers

    // Strategy: iterate table rows and look at specific CELLS
    let rows = document.querySelectorAll("tr");

    if (rows.length > 0) {
        rows.forEach(row => {
            let cells = row.querySelectorAll("td");
            // We need at least 2 cells (Barcode + Name)
            if (cells.length >= 2) {
                // Find column with barcode
                for (let i = 0; i < cells.length; i++) {
                    let text = cells[i].innerText.trim();
                    // Exact or close match for barcode
                    if (/^869\d{10}$/.test(text)) {
                        let barcode = text;

                        // Assume Drug Name is in the NEXT column (i+1)
                        if (i + 1 < cells.length) {
                            let name = cells[i + 1].innerText.trim();

                            // Small cleanup just in case
                            // Remove any trailing parenthesis if they contain non-name info? 
                            // Usually Medula name is clean in its own cell.

                            data.drugs.push({
                                name: name,
                                barcode: barcode
                            });
                            break; // Found drug in this row, move to next row
                        }
                    }
                }
            } else {
                // Fallback for non-table structure (e.g. divs) or if cells not found
                // Try the text regex approach on the row text if cell approach failed?
                // For now, let's stick to cell-based as it's cleaner for Medula.
            }
        });
    }

    // Fallback: If table approach yielded nothing, Regex the whole body text
    if (data.drugs.length === 0) {
        let bodyText = document.body.innerText;
        let barcodeRegex = /(869\d{10})/g;
        let matches = [...bodyText.matchAll(barcodeRegex)];

        matches.forEach(m => {
            // For each barcode, find surrounding text?? Hard to guess name.
            // Just send barcode and let App resolve name from DB?
            data.drugs.push({
                name: "Veritabanından Bul",
                barcode: m[1]
            });
        });
    }

    return data;
}

scrapeData();
