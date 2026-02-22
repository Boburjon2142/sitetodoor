'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import AuthPanel from '@/components/AuthPanel';
import { api, money } from '@/lib/api';

export default function HomePage() {
  const [categories, setCategories] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [q, setQ] = useState('');

  const load = async (search = '') => {
    const [c, p] = await Promise.all([
      api('/catalog/categories/'),
      api(`/catalog/products/${search ? `?q=${encodeURIComponent(search)}` : ''}`),
    ]);
    setCategories(c);
    setProducts(p);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-6">
      <section className="grid lg:grid-cols-[1.35fr_1fr] gap-4">
        <div className="card-hero">
          <p className="chip mb-3">Qurilish Marketplace</p>
          <h1 className="text-3xl font-bold tracking-tight mb-3">Qurilish materiallari endi bitta platformada</h1>
          <p className="muted mb-5">Narxlarni solishtiring, yetkazib berishni tanlang, jarayonni uzluksiz davom ettiring.</p>
          <div className="flex flex-col sm:flex-row gap-2">
            <input className="field flex-1" placeholder="Masalan: M400 sement, armatura 12mm" value={q} onChange={(e) => setQ(e.target.value)} />
            <button className="btn" onClick={() => load(q)}>Qidirish</button>
          </div>
        </div>
        <AuthPanel />
      </section>

      <section className="card">
        <h2 className="font-semibold mb-3 text-lg">Top kategoriyalar</h2>
        <div className="flex gap-3 flex-wrap">
          {categories.map((cat) => (
            <Link key={cat.id} href={`/category/${cat.id}`} className="chip hover:brightness-95">
              {cat.name}
            </Link>
          ))}
        </div>
      </section>

      <section className="card">
        <h2 className="font-semibold mb-3 text-lg">Mahsulotlar</h2>
        <div className="grid md:grid-cols-2 gap-3">
          {products.map((p) => (
            <Link key={p.id} href={`/product/${p.id}`} className="rounded-xl border border-slate-200 p-4 transition hover:-translate-y-0.5 hover:shadow-md">
              <p className="font-semibold">{p.name}</p>
              <p className="text-sm muted">{p.category_name}</p>
              {p.best_price && <p className="text-sm mt-2 font-medium">Eng yaxshi narx: {money(p.best_price)}</p>}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
