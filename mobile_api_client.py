import requests
import json
import logging

# Set up logging for tracking successful sent prescriptions
logging.basicConfig(level=logging.INFO)

# Configuration
SUPABASE_EDGE_FUNCTION_URL = "https://trtvkyvtbrrftrachtez.supabase.co/functions/v1/prescription-send"
API_SECRET_KEY = "PHARMACISCO_SECRET_DESKTOP_KEY_123"

def send_prescription_to_cloud(user_identifier: str, labels_data: list) -> bool:
    """
    Sends prescription labels directly from Pharmacisco Desktop to Supabase Edge Function.
    This creates pushing notifications/schedules automatically on the patient's mobile app.
    
    :param user_identifier: The National ID (TC Kimlik No) or Phone Number of the patient
    :param labels_data: A list of dicts with medication data
    :return: True if successful, False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {API_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "user_identifier": user_identifier,
        "medications": labels_data
    }

    try:
        logging.info(f"Sending prescription data for user: {user_identifier}")
        response = requests.post(SUPABASE_EDGE_FUNCTION_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            logging.info(f"Success: {result.get('message', 'Prescription ingested.')}")
            return True
        elif response.status_code == 404:
            logging.warning("User not found: Patient needs to register on the mobile app first.")
            return False
        else:
            logging.error(f"Failed to send prescription. Server returned {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Network error while sending prescription to cloud: {e}")
        return False

# Example Usage:
if __name__ == "__main__":
    # Suppose we just printed a label for a patient
    sample_patient_id = "12345678901" # National ID
    sample_meds = [
        {
            "name": "Aferin Sinüs 500 Mg",
            "dosage": "1 tablet",
            "notes": "Tok karnına",
            "times": ["09:00", "21:00"],  # Push notifications will ring at 09 and 21
            "start_date": "2024-05-01",
            "end_date": "2024-05-07"
        }
    ]
    
    success = send_prescription_to_cloud(sample_patient_id, sample_meds)
    if success:
        print("Masaüstü programı ilacı başarıyla buluta iletti. Hasta mobil uygulamadan bildirim alacak!")
