'use client';

import { useState } from 'react';
import { api, getToken } from '@/lib/api';

export default function DriverPage() {
  const [orderId, setOrderId] = useState('1');
  const [message, setMessage] = useState('');

  const accept = async () => {
    try {
      await api(`/tracking/driver/orders/${orderId}/accept/`, { method: 'POST', token: getToken() });
      setMessage('Buyurtma qabul qilindi');
    } catch (e: any) {
      setMessage(e.message);
    }
  };

  const sendLocation = async () => {
    try {
      await api('/tracking/driver/location/', {
        method: 'POST',
        token: getToken(),
        body: { order: Number(orderId), latitude: 41.3001, longitude: 69.2501 },
      });
      setMessage('Lokatsiya yuborildi');
    } catch (e: any) {
      setMessage(e.message);
    }
  };

  const complete = async () => {
    try {
      await api(`/tracking/driver/orders/${orderId}/complete/`, { method: 'POST', token: getToken() });
      setMessage('Buyurtma yopildi');
    } catch (e: any) {
      setMessage(e.message);
    }
  };

  return (
    <div className="card space-y-3">
      <h1 className="text-2xl font-bold tracking-tight">Driver panel</h1>
      <input className="field" value={orderId} onChange={(e) => setOrderId(e.target.value)} />
      <div className="flex flex-wrap gap-2">
        <button className="btn" onClick={accept}>Accept</button>
        <button className="btn" onClick={sendLocation}>Location</button>
        <button className="btn" onClick={complete}>Delivered</button>
      </div>
      {message && <p className="muted">{message}</p>}
    </div>
  );
}
