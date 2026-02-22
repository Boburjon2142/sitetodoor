'use client';

import { useEffect, useState } from 'react';
import { api, getToken } from '@/lib/api';

export default function CheckoutPage() {
  const [addresses, setAddresses] = useState<any[]>([]);
  const [addressId, setAddressId] = useState('');
  const [payment, setPayment] = useState('cash');
  const [message, setMessage] = useState('');

  useEffect(() => {
    api('/auth/addresses/', { token: getToken() })
      .then((res) => {
        setAddresses(res);
        if (res[0]) setAddressId(String(res[0].id));
      })
      .catch(() => setAddresses([]));
  }, []);

  const createAddress = async () => {
    const res = await api('/auth/addresses/', {
      method: 'POST',
      token: getToken(),
      body: {
        name: 'Obyekt 1',
        city: 'Toshkent',
        street: 'Chilonzor 10',
        latitude: 41.2866,
        longitude: 69.2034,
        is_default: true,
      },
    });
    setAddresses((p) => [res, ...p]);
    setAddressId(String(res.id));
  };

  const checkout = async () => {
    try {
      const res = await api('/cart/checkout/', {
        method: 'POST',
        token: getToken(),
        body: {
          address_id: Number(addressId),
          delivery_slot: new Date(Date.now() + 3600 * 1000).toISOString(),
          payment_method: payment,
        },
      });
      setMessage(`Buyurtma yaratildi: ${res.orders.join(', ')}`);
    } catch (e: any) {
      setMessage(e.message);
    }
  };

  return (
    <div className="card space-y-4">
      <h1 className="text-2xl font-bold tracking-tight">Checkout</h1>
      <div>
        <p className="label">Manzil</p>
        <select className="field" value={addressId} onChange={(e) => setAddressId(e.target.value)}>
          {addresses.map((a) => (
            <option key={a.id} value={a.id}>{a.name} - {a.street}</option>
          ))}
        </select>
        <button className="btn-secondary mt-2" onClick={createAddress}>Demo manzil qo`shish</button>
      </div>
      <div>
        <p className="label">To`lov</p>
        <select className="field" value={payment} onChange={(e) => setPayment(e.target.value)}>
          <option value="cash">Naqd</option>
          <option value="mockpay">MockPay</option>
          <option value="payme">Payme</option>
          <option value="click">Click</option>
          <option value="uzum">Uzum</option>
        </select>
      </div>
      <button className="btn" onClick={checkout}>Buyurtma berish</button>
      {message && <p className="muted">{message}</p>}
    </div>
  );
}
