import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.EXPO_PUBLIC_SUPABASE_URL || 'https://trtvkyvtbrrftrachtez.supabase.co';
const SUPABASE_ANON_KEY = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRydHZreXZ0YnJyZnRyYWNodGV6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzODgxODMsImV4cCI6MjA4OTk2NDE4M30.G8pbP_eeE_WhBkAUTTG_4AakZRKDcyiUsAYsXOhD2XA';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function testSignup() {
  const email = '5554443322@pharmacisco.local';
  console.log('Testing signup for', email);
  
  const { data, error } = await supabase.auth.signUp({
    email,
    password: 'password123',
    options: {
      data: {
        national_id: '5554443322',
      }
    }
  });

  if (error) {
    console.error('SIGNUP ERROR:', error.status, error.message);
  } else {
    console.log('SIGNUP SUCCESS:', data);
  }
}

testSignup();
