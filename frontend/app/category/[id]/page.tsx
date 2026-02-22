'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api, money } from '@/lib/api';

export default function CategoryPage({ params }: { params: { id: string } }) {
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    api(`/catalog/products/?category=${params.id}`).then(setProducts);
  }, [params.id]);

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold tracking-tight">Kategoriya mahsulotlari</h1>
        <span className="chip">{products.length} ta</span>
      </div>
      <div className="grid md:grid-cols-2 gap-3">
        {products.map((p) => (
          <Link key={p.id} href={`/product/${p.id}`} className="rounded-xl border border-slate-200 p-4 hover:shadow-md transition">
            <p className="font-semibold">{p.name}</p>
            {p.best_price && <p className="text-sm mt-2 muted">{money(p.best_price)}</p>}
          </Link>
        ))}
      </div>
    </div>
  );
}
