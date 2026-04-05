# Pharmacisco Pill Reminder Mobile App

This is a React Native mobile application built with [Expo](https://expo.dev) that is designed to integrate with the Pharmacisco Desktop labeling application. It serves as a medication reminder and tracking system for patients.

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (or yarn)
- **Expo Go** app installed on your physical mobile device (available on iOS App Store & Google Play Store)
- Or, Android Studio / Xcode if you want to run it on a computer emulator

### 📦 Installation

1. Navigate to the `mobile_appplication` directory (where this file is located):
   ```bash
   cd "C:\Users\yigit\Documents\2022\github repolar\pharmacisco\mobile_appplication"
   ```

2. Install dependencies (should be installed by default from initial setup, but good to ensure):
   ```bash
   npm install
   ```

### 🏃 Running the Application

Start the Expo development server:
```bash
npx expo start
```

This will start Metro bundler and open a console with a QR code.

- **To run on a physical device:** Open the "Expo Go" app on your phone and scan the QR code.
- **To run on Android Emulator:** Press `a` in the terminal.
- **To run on iOS Simulator (Mac Only):** Press `i` in the terminal.

## 🛠 Testing the Supabase / Desktop Integration

The mobile application pulls its schedules directly from Supabase, which receives data from your Desktop Python app.

1. Create a label in the Desktop App as usual.
2. Ensure the Desktop App successfully sends a `POST` request to our Supabase Edge Function (`/api/prescription/send`).
3. Open the Mobile App on your device. Assuming you are logged in with the matching phone number or national ID, your dashboard will automatically populate with the newly added medication, and its push notifications will be scheduled locally.

## 🧩 Tech Stack
- **Framework:** React Native + Expo (Tabs template)
- **Backend & DB:** Supabase (Auth, Postgres, Realtime, Edge Functions)
- **Styling:** React Native styling (Medical grade White & Blue palette)
- **Notifications:** Expo Push Notifications


////

İstersen oluşturduğum 

mobile_api_client.py
 entegrasyonunu mevcut etiket programındaki 

.py
 koduna nasıl bağlayacağımızı tartışalım (Hangi dosyada entegre etmek istersin?).
Ya da Stitch uygulamasının oluşturduğu bu tasarımlara bakıp ona göre React Native (Expo) kodlarını app/ klasörünün içerisine React (TSX) sayfaları olarak dökmeye başlayalım.