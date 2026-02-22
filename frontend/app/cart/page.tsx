'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api, getToken, money } from '@/lib/api';

export default function CartPage() {
  const [cart, setCart] = useState<any>(null);

  const load = () => api('/cart/', { token: getToken() }).then(setCart);

  useEffect(() => {
    load();
  }, []);

  if (!cart) return <div className="card">Yuklanmoqda...</div>;

  return (
    <div className="card space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Savat</h1>
        <span className="chip">{cart.items.length} pozitsiya</span>
      </div>
      {cart.items.map((item: any) => (
        <div key={item.id} className="rounded-xl border border-slate-200 p-3 flex justify-between items-center">
          <div>
            <p className="font-semibold">{item.product_name}</p>
            <p className="text-sm muted">{item.supplier_name}</p>
          </div>
          <p className="font-semibold">{money(item.line_total)}</p>
        </div>
      ))}
      <p className="text-lg font-bold">Jami: {money(cart.items_subtotal)}</p>
      <Link href="/checkout" className="btn inline-block">Checkout</Link>
    </div>
  );
}
