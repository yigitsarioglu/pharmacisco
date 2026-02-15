import json
import os
import sys

# Add project root to path to import drug_db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.drug_db import DrugDatabase

def import_drugs():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'ilac.json')
    
    print(f"Reading {json_path}...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: database/ilac.json not found.")
        return

    # Find the table data
    drug_list = []
    for item in data:
        if item.get('type') == 'table' and item.get('name') == 'ilac':
            drug_list = item.get('data', [])
            break
    
    if not drug_list:
        print("No drug data found in JSON.")
        return

    print(f"Found {len(drug_list)} drugs. Starting import...")
    
    db = DrugDatabase()
    count = 0
    duplicates = 0
    errors = 0

    for drug in drug_list:
        barcode = drug.get('barcode', '').strip()
        name = drug.get('Product_Name', '').strip()
        category = drug.get('Category_2', '').strip()
        description = drug.get('Description', '').strip()
        
        # Basic validation
        if not barcode or not name:
            continue

        # Prepare fields
        # Short instruction: First 100 chars of description or empty
        short_inst = description[:100] + "..." if len(description) > 100 else description
        full_inst = description
        preg_cat = "" # User requested to leave empty

        # Add to DB
        success = db.add_drug(
            barcode=barcode,
            name=name,
            category=category,
            preg_cat=preg_cat,
            short_inst=short_inst,
            full_inst=full_inst
        )

        if success:
            count += 1
            if count % 100 == 0:
                print(f"Imported {count} drugs...", end='\r')
        else:
            duplicates += 1

    print(f"\nImport Completed.")
    print(f"Successfully Imported: {count}")
    print(f"Duplicates/Skipped: {duplicates}")

if __name__ == "__main__":
    import_drugs()
