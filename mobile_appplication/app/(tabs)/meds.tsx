import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity, Alert, ActivityIndicator, Platform } from 'react-native';
import { supabase } from '../../utils/supabase';
import { useTranslation } from 'react-i18next';
import { Trash2, Plus, Minus } from 'lucide-react-native';
import { scheduleMedicationAlarm } from '../../utils/notifications';

const DAYS = [
  { label: 'Pzt', value: 1 },
  { label: 'Sal', value: 2 },
  { label: 'Çar', value: 3 },
  { label: 'Per', value: 4 },
  { label: 'Cum', value: 5 },
  { label: 'Cmt', value: 6 },
  { label: 'Paz', value: 7 },
];

export default function MedsScreen() {
  const { t } = useTranslation();
  const [meds, setMeds] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  
  // Form states
  const [name, setName] = useState('');
  const [dosage, setDosage] = useState('');
  const [times, setTimes] = useState<string[]>(['09:00']);
  
  const currentIsoDay = new Date().getDay() === 0 ? 7 : new Date().getDay();
  const [selectedDays, setSelectedDays] = useState<number[]>([currentIsoDay]);

  const toggleDay = (d: number) => {
    if (selectedDays.includes(d)) {
      setSelectedDays(prev => prev.filter(x => x !== d));
    } else {
      setSelectedDays(prev => [...prev, d]);
    }
  };

  const addTimeField = () => setTimes(prev => [...prev, '12:00']);

  const updateTime = (text: string, index: number) => {
    const newTimes = [...times];
    newTimes[index] = text;
    setTimes(newTimes);
  };

  const removeTimeField = (index: number) => {
    setTimes(prev => prev.filter((_, i) => i !== index));
  };

  const fetchMeds = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    const { data, error } = await supabase
      .from('medications')
      .select('*')
      .order('created_at', { ascending: false });

    if (!error && data) {
      setMeds(data);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchMeds();
  }, []);

  const handleAddMeds = async () => {
    if (!name || !dosage) return;
    
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // Insert Medication
    const { data: med, error } = await supabase.from('medications').insert({
      user_id: user.id,
      name,
      dosage,
      created_by: 'user'
    }).select().single();

    if (error) {
      Alert.alert('Error', error.message);
      return;
    }

    // Loop through defined times and insert a distinct schedule for each
    for (const tVal of times) {
      const formattedTime = tVal.includes(':') && tVal.length === 5 ? `${tVal}:00` : '09:00:00';
      await supabase.from('schedules').insert({
        medication_id: med.id,
        time: formattedTime,
        repeat_type: 'weekly',
        days_of_week: selectedDays.length > 0 ? selectedDays : null
      });

      if (selectedDays.length > 0) {
        scheduleMedicationAlarm("İlaç Vakti!", `${name} (${dosage}) almayı unutmayın.`, formattedTime, selectedDays);
      }
    }

    setName('');
    setDosage('');
    setTimes(['09:00']);
    fetchMeds(); // Refresh list
  };

  const handleDeleteMeds = async (id: string) => {
    if (Platform.OS === 'web') {
      const confirmed = window.confirm(t('meds.delete_confirm'));
      if (confirmed) {
        await supabase.from('medications').delete().match({ id });
        fetchMeds();
      }
    } else {
      Alert.alert(t('meds.delete_confirm'), '', [
        { text: 'İptal', style: 'cancel' },
        { 
          text: 'Sil', 
          style: 'destructive', 
          onPress: async () => {
            await supabase.from('medications').delete().match({ id });
            fetchMeds();
          } 
        }
      ]);
    }
  };

  const renderItem = ({ item }: { item: any }) => (
    <View style={styles.card}>
      <View style={styles.cardContent}>
        <Text style={styles.medName}>{item.name}</Text>
        <Text style={styles.medDosage}>{item.dosage}</Text>
        <Text style={styles.medSource}>Added by: {item.created_by}</Text>
      </View>
      <TouchableOpacity onPress={() => handleDeleteMeds(item.id)} style={styles.deleteBtn}>
        <Trash2 color="#EF4444" size={20} />
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.form}>
        <Text style={styles.sectionTitle}>{t('meds.manually_add')}</Text>
        <TextInput
          style={styles.input}
          placeholder={t('meds.name')}
          value={name}
          onChangeText={setName}
        />
        <TextInput
          style={styles.input}
          placeholder={t('meds.dosage')}
          value={dosage}
          onChangeText={setDosage}
        />
        <View style={styles.timesHeader}>
          <Text style={styles.timesLabel}>İlaç Saatleri</Text>
          <TouchableOpacity onPress={addTimeField} style={styles.addTimeBtn}>
             <Plus color="#0066FF" size={20} />
             <Text style={styles.addTimeText}>Saat Ekle</Text>
          </TouchableOpacity>
        </View>

        {times.map((tVal, idx) => (
           <View key={idx} style={styles.timeRow}>
             <TextInput
                style={[styles.input, { flex: 1, marginBottom: 0 }]}
                placeholder="Örn: 09:00"
                value={tVal}
                onChangeText={(val) => updateTime(val, idx)}
                maxLength={5}
                keyboardType="numbers-and-punctuation"
             />
             {times.length > 1 && (
               <TouchableOpacity onPress={() => removeTimeField(idx)} style={styles.removeTimeBtn}>
                  <Minus color="#EF4444" size={24} />
               </TouchableOpacity>
             )}
           </View>
        ))}

        <View style={styles.daysContainer}>
          {DAYS.map(day => (
            <TouchableOpacity 
              key={day.value} 
              style={[styles.dayCircle, selectedDays.includes(day.value) && styles.dayCircleSelected]}
              onPress={() => toggleDay(day.value)}
            >
              <Text style={[styles.dayText, selectedDays.includes(day.value) && styles.dayTextSelected]}>{day.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
        <TouchableOpacity style={styles.addButton} onPress={handleAddMeds}>
          <Text style={styles.addButtonText}>{t('meds.add_btn')}</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={meds}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  form: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#111827'
  },
  input: {
    backgroundColor: '#F8F9FA',
    borderWidth: 1,
    borderColor: '#ced4da',
    borderRadius: 8,
    padding: 12,
    marginBottom: 10,
  },
  addButton: {
    backgroundColor: '#0066FF',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  list: { padding: 20 },
  card: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.05,
    elevation: 2,
    shadowOffset: { width: 0, height: 2 },
  },
  cardContent: { flex: 1 },
  medName: { fontSize: 16, fontWeight: 'bold', color: '#111827' },
  medDosage: { fontSize: 14, color: '#6c757d', marginVertical: 4 },
  medSource: { fontSize: 12, color: '#adb5bd', fontStyle: 'italic' },
  deleteBtn: { padding: 10 },
  daysContainer: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 15 },
  dayCircle: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f1f5f9', justifyContent: 'center', alignItems: 'center' },
  dayCircleSelected: { backgroundColor: '#0066FF' },
  dayText: { fontSize: 13, color: '#6c757d', fontWeight: 'bold' },
  dayTextSelected: { color: '#FFFFFF' },
  timesHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10, marginTop: 5 },
  timesLabel: { fontSize: 14, color: '#343a40', fontWeight: '600' },
  addTimeBtn: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#e0f2fe', paddingVertical: 6, paddingHorizontal: 10, borderRadius: 6 },
  addTimeText: { color: '#0066FF', marginLeft: 4, fontWeight: '600', fontSize: 13 },
  timeRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  removeTimeBtn: { padding: 10, marginLeft: 5 }
});
