'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api, getToken, money } from '@/lib/api';

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);

  useEffect(() => {
    api('/orders/', { token: getToken() }).then(setOrders).catch(() => setOrders([]));
  }, []);

  return (
    <div className="card space-y-3">
      <h1 className="text-2xl font-bold tracking-tight">Buyurtmalarim</h1>
      {orders.map((order) => (
        <Link key={order.id} href={`/orders/${order.id}`} className="block rounded-xl border border-slate-200 p-3 hover:shadow-md transition">
          <p className="font-semibold">#{order.id} - {order.status}</p>
          <p className="text-sm muted">{money(order.total_amount)}</p>
        </Link>
      ))}
    </div>
  );
}
