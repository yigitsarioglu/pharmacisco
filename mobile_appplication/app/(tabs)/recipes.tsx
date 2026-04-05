import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator, RefreshControl } from 'react-native';
import { supabase } from '../../utils/supabase';
import { useTranslation } from 'react-i18next';
import { FileText, Calendar, User as UserIcon } from 'lucide-react-native';
import { useFocusEffect } from 'expo-router';

export default function RecipesScreen() {
  const { t } = useTranslation();
  const [recipes, setRecipes] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchRecipes = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    const { data, error } = await supabase
      .from('prescriptions_raw')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (!error && data) {
      setRecipes(data);
    }
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchRecipes();
    }, [])
  );

  const renderItem = ({ item }: { item: any }) => {
    let payload;
    try {
      payload = typeof item.json_data === 'string' ? JSON.parse(item.json_data) : item.json_data;
    } catch (e) {
      payload = null;
    }

    const date = new Date(item.created_at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });
    
    return (
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <View style={styles.headerLeft}>
            <FileText color="#0066FF" size={24} />
            <Text style={styles.cardTitle}>E-Reçete</Text>
          </View>
          <View style={styles.headerDate}>
            <Calendar color="#6c757d" size={14} />
            <Text style={styles.dateText}>{date}</Text>
          </View>
        </View>
        
        {payload ? (
          <View style={styles.cardBody}>
            <View style={styles.doctorInfo}>
               <UserIcon color="#495057" size={16} />
               <Text style={styles.doctorName}>Dr. {payload.doctor_name || 'Bilinmiyor'}</Text>
            </View>
            <View style={styles.medsList}>
              {payload.medications && payload.medications.map((m: any, idx: number) => (
                <View key={idx} style={styles.medItem}>
                  <View style={styles.medDot} />
                  <Text style={styles.medText}>{m.name} <Text style={styles.medDosage}>({m.dosage})</Text></Text>
                </View>
              ))}
            </View>
          </View>
        ) : (
          <Text style={styles.errorText}>Detay okunamadı (Bozuk Veri Tipi).</Text>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {loading && recipes.length === 0 ? (
        <ActivityIndicator size="large" color="#0066FF" style={styles.loader} />
      ) : (
        <FlatList
          data={recipes}
          keyExtractor={(item) => item.id}
          renderItem={renderItem}
          contentContainerStyle={styles.listContainer}
          refreshControl={<RefreshControl refreshing={loading} onRefresh={fetchRecipes} />}
          ListEmptyComponent={
            <Text style={styles.emptyText}>Henüz hiç reçete bulunmuyor.</Text>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  loader: { marginTop: 50 },
  listContainer: { padding: 20 },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
    borderTopWidth: 4,
    borderTopColor: '#0066FF'
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f1f5f9'
  },
  headerLeft: { flexDirection: 'row', alignItems: 'center' },
  cardTitle: { fontSize: 16, fontWeight: 'bold', color: '#111827', marginLeft: 8 },
  headerDate: { flexDirection: 'row', alignItems: 'center' },
  dateText: { fontSize: 12, color: '#6c757d', marginLeft: 4 },
  cardBody: { marginTop: 4 },
  doctorInfo: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  doctorName: { fontSize: 14, color: '#495057', fontWeight: '500', marginLeft: 6 },
  medsList: { backgroundColor: '#f8f9fa', padding: 12, borderRadius: 8 },
  medItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 6 },
  medDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#0066FF', marginRight: 8 },
  medText: { fontSize: 14, color: '#343a40', flex: 1 },
  medDosage: { color: '#6c757d', fontSize: 12 },
  errorText: { color: '#EF4444', fontSize: 13, marginTop: 10 },
  emptyText: { textAlign: 'center', color: '#6c757d', marginTop: 40, fontSize: 15 }
});
