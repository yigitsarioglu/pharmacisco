import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import * as Localization from 'expo-localization';
import AsyncStorage from '@react-native-async-storage/async-storage';
import tr from './tr.json';
import en from './en.json';

const resources = {
  tr: { translation: tr },
  en: { translation: en }
};

const LANGUAGE_KEY = 'settings.lang';

const languageDetector = {
  type: 'languageDetector' as const,
  async: true,
  init: () => {},
  detect: async (callback: (lang: string) => void) => {
    try {
      const savedDataJSON = await AsyncStorage.getItem(LANGUAGE_KEY);
      const lng = savedDataJSON ? savedDataJSON : null;
      const selectLanguage = lng || Localization.getLocales()[0].languageCode || 'en';
      callback(selectLanguage);
    } catch (error) {
      console.log('Error reading language', error);
      callback('en');
    }
  },
  cacheUserLanguage: async (lng: string) => {
    try {
      await AsyncStorage.setItem(LANGUAGE_KEY, lng);
    } catch (error) {
      console.log('Error setting language', error);
    }
  }
};

i18n
  .use(languageDetector)
  .use(initReactI18next)
  .init({
    compatibilityJSON: 'v3',
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

export default i18n;
