import React, { useState } from 'react';
import { StyleSheet, View, TextInput, TouchableOpacity, Text, ActivityIndicator } from 'react-native';
import { supabase } from '../../utils/supabase';
import { useTranslation } from 'react-i18next';
import { useRouter } from 'expo-router';

export default function RegisterScreen() {
  const { t } = useTranslation();
  const router = useRouter();

  const [nationalId, setNationalId] = useState('');
  const [phone, setPhone] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  async function handleRegister() {
    if (!nationalId || !phone || !password || !fullName) {
      setErrorMessage(t('register.error_empty'));
      return;
    }

    try {
      // Direct call to Edge Function completely bypassing IP restrictions and rate limits
      const { data, error } = await supabase.functions.invoke('register', {
        body: { national_id: nationalId, phone, full_name: fullName, password }
      });
      
      if (error) {
        setErrorMessage(error.message);
        setLoading(false);
        return;
      }
      
      if (data && data.error) {
        setErrorMessage(data.error);
        setLoading(false);
        return;
      }

      // Automatically sign in the user since the Admin API already verified and created them
      const pseudoEmail = `u${nationalId}@pharmaciscoapp.com`;
      const { error: signInError } = await supabase.auth.signInWithPassword({
        email: pseudoEmail,
        password: password,
      });

      if (signInError) {
        setErrorMessage('Kayıt Başarılı Ancak Giriş Yapılamadı: ' + signInError.message);
      } else {
        // Successful login! Expo router _layout logic handles pushing to (tabs) automatically 
        // since the user session state changes.
        setErrorMessage(t('register.success'));
      }
      
    } catch (err: any) {
      setErrorMessage(err.message || 'Bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t('register.title')}</Text>
      <Text style={styles.subtitle}>{t('register.subtitle')}</Text>
      
      {errorMessage ? (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>{errorMessage}</Text>
        </View>
      ) : null}
      
      <View style={styles.verticallySpaced}>
        <Text style={styles.label}>{t('register.national_id')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={setNationalId}
          value={nationalId}
          placeholder="11 Haneli TC Kimlik No"
          keyboardType="numeric"
        />
      </View>
      
      <View style={styles.verticallySpaced}>
        <Text style={styles.label}>{t('register.phone')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={setPhone}
          value={phone}
          placeholder="05..."
          keyboardType="phone-pad"
        />
      </View>

      <View style={styles.verticallySpaced}>
        <Text style={styles.label}>{t('register.full_name')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={setFullName}
          value={fullName}
          placeholder="Ad Soyad"
        />
      </View>

      <View style={styles.verticallySpaced}>
        <Text style={styles.label}>{t('login.password_label')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={setPassword}
          value={password}
          secureTextEntry={true}
          placeholder="Şifre"
        />
      </View>
      
      <View style={[styles.verticallySpaced, styles.mt20]}>
        <TouchableOpacity style={styles.button} disabled={loading} onPress={handleRegister}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t('register.button')}</Text>}
        </TouchableOpacity>
      </View>

      <View style={styles.verticallySpaced}>
        <TouchableOpacity onPress={() => router.back()} disabled={loading}>
          <Text style={styles.linkText}>{t('register.login_link')}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1, justifyContent: 'center', backgroundColor: '#F8F9FA' },
  errorBox: { padding: 10, backgroundColor: '#fee2e2', borderRadius: 8, marginBottom: 20, borderWidth: 1, borderColor: '#ef4444' },
  errorText: { color: '#ef4444', textAlign: 'center', fontWeight: 'bold' },
  title: { fontSize: 28, fontWeight: 'bold', color: '#0066FF', textAlign: 'center' },
  subtitle: { fontSize: 16, color: '#6c757d', textAlign: 'center', marginBottom: 30 },
  verticallySpaced: { paddingTop: 4, paddingBottom: 4, alignSelf: 'stretch' },
  mt20: { marginTop: 20 },
  label: { fontSize: 14, color: '#343a40', marginBottom: 5, fontWeight: '600' },
  input: { backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#ced4da', borderRadius: 8, paddingHorizontal: 15, paddingVertical: 12, fontSize: 16 },
  button: { backgroundColor: '#0066FF', borderRadius: 8, paddingVertical: 15, alignItems: 'center' },
  buttonText: { color: '#FFFFFF', fontSize: 18, fontWeight: 'bold' },
  linkText: { color: '#0066FF', textAlign: 'center', fontSize: 14, fontWeight: '600', marginTop: 10 }
});
