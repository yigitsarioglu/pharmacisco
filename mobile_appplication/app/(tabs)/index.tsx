import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, RefreshControl } from 'react-native';
import { useTranslation } from 'react-i18next';
import { supabase } from '../../utils/supabase';
import { CheckCircle2, Circle, UserCircle, Bell, BellDot } from 'lucide-react-native';
import { registerForPushNotificationsAsync } from '../../utils/notifications';
import { useFocusEffect } from 'expo-router';

export default function DashboardScreen() {
  const { t } = useTranslation();
  const [schedules, setSchedules] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState('User');

  const fetchTodaySchedules = async () => {
    setLoading(true);
    const { data: userData } = await supabase.auth.getUser();
    if (userData.user) {
      // Prioritize full_name from metadata, fallback to TC
      const meta = userData.user.user_metadata;
      setUserName(meta?.full_name || meta?.national_id || userData.user.email?.split('@')[0] || 'User');
    }

    const todayStr = new Date().toISOString().split('T')[0];

    // Get schedules + medication details
    const { data: sData, error: sErr } = await supabase
      .from('schedules')
      .select(`
        id, time,
        medications ( id, name, dosage ),
        doses ( status, scheduled_date )
      `)
      .order('time', { ascending: true });

    if (!sErr && sData) {
      // Filter for today's status manually to guarantee accurate representation
      const isoDay = new Date().getDay() === 0 ? 7 : new Date().getDay();
      
      const processed = sData
        .filter((s: any) => !s.days_of_week || s.days_of_week.includes(isoDay))
        .map((s: any) => {
          const todayDose = s.doses?.find((d: any) => d.scheduled_date === todayStr);
          return {
            ...s,
            isTaken: todayDose?.status === 'taken',
          };
        });
      setSchedules(processed);
    }
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchTodaySchedules();
    }, [])
  );

  const toggleTakeStatus = async (scheduleId: string, currentStatus: boolean) => {
    // Optimistic UI update
    setSchedules(prev => prev.map(s => s.id === scheduleId ? { ...s, isTaken: !currentStatus } : s));
    
    const todayStr = new Date().toISOString().split('T')[0];
    
    if (currentStatus) {
      // Was taken, now un-taking (delete dose or set pending)
      await supabase.from('doses').delete().match({ schedule_id: scheduleId, scheduled_date: todayStr });
    } else {
      // Was not taken, now taking
      await supabase.from('doses').upsert({
        schedule_id: scheduleId,
        scheduled_date: todayStr,
        status: 'taken',
        taken_at: new Date().toISOString()
      }, { onConflict: 'schedule_id, scheduled_date' });
    }
  };

  const renderItem = ({ item }: { item: any }) => (
    <TouchableOpacity 
      style={[styles.card, item.isTaken && styles.cardTaken]}
      onPress={() => toggleTakeStatus(item.id, item.isTaken)}
      activeOpacity={0.7}
    >
      <View style={styles.cardLeft}>
        <Text style={[styles.medTime, item.isTaken && styles.textMuted]}>{item.time.substring(0,5)}</Text>
        <View style={styles.medInfo}>
          <Text style={[styles.medName, item.isTaken && styles.textStrike]}>
            {item.medications?.name}
          </Text>
          <Text style={[styles.medDosage, item.isTaken && styles.textMuted]}>
            {item.medications?.dosage}
          </Text>
        </View>
      </View>
      <View>
        {item.isTaken ? (
          <CheckCircle2 color="#28a745" size={28} />
        ) : (
          <Circle color="#0066FF" size={28} />
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Enhanced Header (Stitch Layout) */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <UserCircle color="#0066FF" size={48} strokeWidth={1.5} />
          <View style={styles.headerText}>
            <Text style={styles.greetingLabel}>Hello,</Text>
            <Text style={styles.greetingName}>{userName}</Text>
          </View>
        </View>
        <TouchableOpacity style={styles.alarmBtn} onPress={registerForPushNotificationsAsync}>
          <BellDot color="#111827" size={26} strokeWidth={2} />
        </TouchableOpacity>
      </View>

      <View style={styles.timelineHeader}>
        <Text style={styles.sectionTitle}>{t('dashboard.today_meds')} (Timeline)</Text>
      </View>
      
      <FlatList
        data={schedules}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        refreshControl={<RefreshControl refreshing={loading} onRefresh={fetchTodaySchedules} />}
        contentContainerStyle={styles.listContainer}
        ListEmptyComponent={
          !loading ? <Text style={styles.emptyText}>{t('dashboard.no_meds')}</Text> : null
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA'
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerText: {
    marginLeft: 12,
  },
  greetingLabel: {
    fontSize: 14,
    color: '#6c757d',
    fontWeight: '500',
  },
  greetingName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#111827',
  },
  alarmBtn: {
    backgroundColor: '#f1f5f9',
    padding: 10,
    borderRadius: 50,
  },
  timelineHeader: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#343a40',
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
    borderLeftWidth: 4,
    borderLeftColor: '#0066FF'
  },
  cardTaken: {
    borderLeftColor: '#28a745',
    backgroundColor: '#f8f9fa',
    opacity: 0.8
  },
  cardLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  medTime: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#0066FF',
    marginRight: 15,
    width: 55,
  },
  medInfo: {
    justifyContent: 'center',
  },
  medName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 2,
  },
  medDosage: {
    fontSize: 14,
    color: '#6c757d',
  },
  textStrike: {
    textDecorationLine: 'line-through',
    color: '#6c757d'
  },
  textMuted: {
    color: '#adb5bd'
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 40,
    color: '#6c757d',
    fontSize: 16,
  }
});
