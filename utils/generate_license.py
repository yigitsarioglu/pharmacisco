import secrets
import datetime
from supabase import create_client

SUPABASE_URL = "https://aeeliekwqlruiacxeluv.supabase.co"
SUPABASE_KEY = "sb_publishable_lpWnp-XzPJdjnqwmCLt2fA_cT7FcxCb"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_key():
    return "ECZ-" + secrets.token_hex(4).upper()

def create_license(customer, months):
    print(f"\n[{customer}] için {months} aylik lisans olusturuluyor...")
    
    key = generate_key()
    expiry = datetime.date.today() + datetime.timedelta(days=30*months)

    data = {
        "license_key": key,
        "customer_name": customer,
        "expiry_date": str(expiry)
    }

    try:
        response = supabase.table("licenses").insert(data).execute()
        print("\n==================================")
        print("✅ LISANS BASARIYLA OLUSTURULDU!")
        print("==================================")
        print(f"Musteri Adi : {customer}")
        print(f"Bitis Tarihi: {expiry}")
        print(f"LISANS KODU : {key}")
        print("==================================\n")
        print(f"Lütfen '{key}' kodunu musteriye iletin.\n")
    except Exception as e:
        print(f"Hata olustu! Supabase tablonuz (licenses) hazir olmayabilir veya internetiniz kopmus olabilir.\nDetay: {e}")

if __name__ == "__main__":
    print("--- PHARMACISCO LISANS URETICI ---")
    customer_name = input("Musteri (Eczane) Adini girin: ")
    try:
        months_str = input("Kac aylik lisans verilecek? (Orn: 6 veya 12): ")
        months = int(months_str)
        create_license(customer_name, months)
    except ValueError:
        print("Lutfen aykismina sadece rakam girin (Orn: 6)!")