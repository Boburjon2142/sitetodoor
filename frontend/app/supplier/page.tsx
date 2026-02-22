'use client';

import { useEffect, useState } from 'react';
import { api, getToken } from '@/lib/api';

export default function SupplierPage() {
  const [offers, setOffers] = useState<any[]>([]);
  const [msg, setMsg] = useState('');

  const load = () => api('/catalog/supplier/offers/', { token: getToken() }).then(setOffers).catch(() => setOffers([]));

  useEffect(() => {
    load();
  }, []);

  const createOffer = async () => {
    try {
      await api('/catalog/supplier/offers/', {
        method: 'POST',
        token: getToken(),
        body: {
          product: 1,
          price: '77000.00',
          stock: 100,
          min_order_qty: 1,
          delivery_eta_hours: 8,
          is_active: true,
        },
      });
      setMsg('Taklif qo`shildi');
      load();
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  return (
    <div className="card space-y-3">
      <h1 className="text-2xl font-bold tracking-tight">Supplier dashboard</h1>
      <button className="btn" onClick={createOffer}>Demo offer qo`shish</button>
      {msg && <p className="muted">{msg}</p>}
      {offers.map((o) => (
        <div key={o.id} className="rounded-xl border border-slate-200 p-3">
          Product #{o.product} | Narx: {o.price} | Qoldiq: {o.stock}
        </div>
      ))}
    </div>
  );
}
