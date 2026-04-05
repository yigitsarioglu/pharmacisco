import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';
import { Platform, Alert } from 'react-native';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});

export async function registerForPushNotificationsAsync() {
  if (Platform.OS === 'web') {
    window.alert('Tarayıcı desteklenmiyor: Push bildirimler sadece mobil cihazlarda tam çalışır.');
    return;
  }
  let token;
  if (Device.isDevice) {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== 'granted') {
      Alert.alert('Hata', 'Bildirim izni alınamadı!');
      return;
    }
    token = (await Notifications.getExpoPushTokenAsync()).data;
    Alert.alert('Başarılı', 'Bildirimler aktifleştirildi, ilaç saatlerinde cihazınıza uyarı gelecek!');
  } else {
    Alert.alert('Uyarı', 'Fiziksel bir cihaz kullanmalısınız (Simülatörlerde bildirim gelmeyebilir).');
  }
  return token;
}

export async function scheduleMedicationAlarm(title: string, body: string, time: string, weekdays: number[]) {
  if (Platform.OS === 'web') return;

  const [hh, mm] = time.split(':').map(Number);

  for (const day of weekdays) {
    // Expo triggers uses: 1 = Sunday, 2 = Monday ... 7 = Saturday
    // Database ISO used: 1 = Monday, ... 7 = Sunday
    const expoWeekday = day === 7 ? 1 : day + 1;
    await Notifications.scheduleNotificationAsync({
      content: {
        title,
        body,
        sound: true,
      },
      trigger: {
        hour: hh,
        minute: mm,
        weekday: expoWeekday,
        repeats: true,
      } as Notifications.NotificationTriggerInput,
    });
  }
}
