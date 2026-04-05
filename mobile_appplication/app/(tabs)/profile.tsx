import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { supabase } from '../../utils/supabase';
import { useTranslation } from 'react-i18next';
import { LogOut, Globe, User, Phone, Edit3 } from 'lucide-react-native';

export default function ProfileScreen() {
  const { t, i18n } = useTranslation();
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    async function fetchProfile() {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.id)
        .single();
        
      if (!error && data) {
        setProfile(data);
      }
    }
    fetchProfile();
  }, []);

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) Alert.alert('Error', error.message);
  };

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'tr' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t('profile.title')}</Text>

      {profile && (
        <View style={[styles.section, { marginBottom: 20 }]}>
          <View style={styles.row}>
            <View style={styles.rowLeft}>
              <User color="#0066FF" size={24} />
              <View style={styles.textStack}>
                <Text style={styles.infoLabel}>Ad Soyad</Text>
                <Text style={styles.infoValue}>{profile.full_name || '-'}</Text>
              </View>
            </View>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <View style={styles.rowLeft}>
              <Edit3 color="#0066FF" size={24} />
              <View style={styles.textStack}>
                <Text style={styles.infoLabel}>TC Kimlik Numarası (Değiştirilemez)</Text>
                <Text style={styles.infoValue}>{profile.national_id || '-'}</Text>
              </View>
            </View>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <View style={styles.rowLeft}>
              <Phone color="#0066FF" size={24} />
              <View style={styles.textStack}>
                <Text style={styles.infoLabel}>Telefon Numarası (Değiştirilemez)</Text>
                <Text style={styles.infoValue}>{profile.phone || '-'}</Text>
              </View>
            </View>
          </View>
        </View>
      )}

      <View style={styles.section}>
        <TouchableOpacity style={styles.row} onPress={toggleLanguage}>
          <View style={styles.rowLeft}>
            <Globe color="#0066FF" size={24} />
            <Text style={styles.rowText}>{t('profile.language')} (TR / EN)</Text>
          </View>
          <Text style={styles.currentLang}>{i18n.language.toUpperCase()}</Text>
        </TouchableOpacity>

        <View style={styles.divider} />

        <TouchableOpacity style={styles.row} onPress={handleLogout}>
          <View style={styles.rowLeft}>
            <LogOut color="#EF4444" size={24} />
            <Text style={[styles.rowText, { color: '#EF4444' }]}>{t('profile.logout')}</Text>
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 20,
    marginTop: 10,
  },
  section: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOpacity: 0.05,
    elevation: 2,
    shadowOffset: { width: 0, height: 2 },
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  rowLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rowText: {
    fontSize: 16,
    marginLeft: 15,
    color: '#111827',
    fontWeight: '500'
  },
  textStack: {
    marginLeft: 15,
  },
  infoLabel: {
    fontSize: 12,
    color: '#6c757d',
    marginBottom: 2,
    fontWeight: '600'
  },
  infoValue: {
    fontSize: 16,
    color: '#111827',
    fontWeight: '500'
  },
  currentLang: {
    color: '#6c757d',
    fontWeight: '600'
  },
  divider: {
    height: 1,
    backgroundColor: '#e9ecef',
    marginLeft: 55, // align with text
  }
});
