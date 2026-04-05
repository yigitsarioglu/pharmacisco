import React, { useState } from 'react';
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Alert, ActivityIndicator } from 'react-native';
import { supabase } from '../../utils/supabase';
import { useTranslation } from 'react-i18next';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
  const { t } = useTranslation();
  const router = useRouter();
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // In a real medical app, we might map national_id to a faux email to satisfy standard Supabase Auth
  // For demonstration, we'll treat identifier as an email (since standard password login needs it).
  // E.g., user types '12345678901', we do 'u12345678901@pharmaciscoapp.com'
  const formatEmail = (id: string) => id.includes('@') ? id : `u${id}@pharmaciscoapp.com`;

  async function signInWithEmail() {
    setLoading(true);
    setErrorMessage('');
    const { error } = await supabase.auth.signInWithPassword({
      email: formatEmail(identifier),
      password: password,
    });

    if (error) setErrorMessage(t('login.error_auth') + ' ' + error.message);
    setLoading(false);
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t('login.title')}</Text>
      <Text style={styles.subtitle}>{t('login.subtitle')}</Text>
      
      {errorMessage ? (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>{errorMessage}</Text>
        </View>
      ) : null}
      
      <View style={[styles.verticallySpaced, styles.mt20]}>
        <Text style={styles.label}>{t('login.identifier_label')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={(text) => setIdentifier(text)}
          value={identifier}
          placeholder="TC / Phone"
          autoCapitalize={'none'}
        />
      </View>
      <View style={styles.verticallySpaced}>
        <Text style={styles.label}>{t('login.password_label')}</Text>
        <TextInput
          style={styles.input}
          onChangeText={(text) => setPassword(text)}
          value={password}
          secureTextEntry={true}
          placeholder="Password"
          autoCapitalize={'none'}
        />
      </View>
      
      <View style={[styles.verticallySpaced, styles.mt20]}>
        <TouchableOpacity style={styles.button} disabled={loading} onPress={signInWithEmail}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t('login.button')}</Text>}
        </TouchableOpacity>
      </View>
      
      <View style={styles.verticallySpaced}>
        <TouchableOpacity onPress={() => router.push('/(auth)/register')} disabled={loading}>
          <Text style={styles.linkText}>{t('login.register_link')}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#F8F9FA'
  },
  errorBox: {
    padding: 10,
    backgroundColor: '#fee2e2',
    borderRadius: 8,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#ef4444'
  },
  errorText: {
    color: '#ef4444',
    textAlign: 'center',
    fontWeight: 'bold'
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#0066FF',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#6c757d',
    textAlign: 'center',
    marginBottom: 40,
  },
  verticallySpaced: {
    paddingTop: 4,
    paddingBottom: 4,
    alignSelf: 'stretch',
  },
  mt20: {
    marginTop: 20,
  },
  label: {
    fontSize: 14,
    color: '#343a40',
    marginBottom: 5,
    fontWeight: '600'
  },
  input: {
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#ced4da',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16
  },
  button: {
    backgroundColor: '#0066FF',
    borderRadius: 8,
    paddingVertical: 15,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold'
  },
  linkText: {
    color: '#0066FF',
    textAlign: 'center',
    fontSize: 14,
    fontWeight: '600',
    marginTop: 10
  }
});
