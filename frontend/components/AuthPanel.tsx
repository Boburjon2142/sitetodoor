'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

export default function AuthPanel() {
  const [phone, setPhone] = useState('998900000001');
  const [code, setCode] = useState('');
  const [msg, setMsg] = useState('');

  const requestOtp = async () => {
    try {
      await api('/auth/otp/request/', { method: 'POST', body: { phone } });
      setMsg('OTP yuborildi (backend log/console dan kodni oling).');
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  const verifyOtp = async () => {
    try {
      const res = await api('/auth/otp/verify/', {
        method: 'POST',
        body: { phone, code, role: 'customer' },
      });
      localStorage.setItem('access', res.access);
      localStorage.setItem('refresh', res.refresh);
      setMsg('Muvaffaqiyatli login qilindi.');
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  return (
    <div className="card space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-lg">Telefon orqali kirish</h3>
        <span className="chip">OTP</span>
      </div>
      <input className="field" value={phone} onChange={(e) => setPhone(e.target.value)} />
      <div className="flex flex-col sm:flex-row gap-2">
        <button className="btn" onClick={requestOtp}>OTP so`rash</button>
        <input className="field flex-1" placeholder="Tasdiqlash kodi" value={code} onChange={(e) => setCode(e.target.value)} />
        <button className="btn" onClick={verifyOtp}>Tasdiqlash</button>
      </div>
      {msg && <p className="text-sm muted">{msg}</p>}
    </div>
  );
}
