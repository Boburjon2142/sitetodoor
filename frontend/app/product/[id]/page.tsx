'use client';

import { useEffect, useState } from 'react';
import { api, getToken, money } from '@/lib/api';

export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<any>(null);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    api(`/catalog/products/${params.id}/`).then(setProduct);
  }, [params.id]);

  const addToCart = async (offerId: number) => {
    try {
      await api('/cart/items/', {
        method: 'POST',
        token: getToken(),
        body: { supplier_offer_id: offerId, quantity: 1 },
      });
      setMsg('Savatga qo`shildi');
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  if (!product) return <div className="card">Yuklanmoqda...</div>;

  return (
    <div className="space-y-4">
      <div className="card-hero">
        <h1 className="text-2xl font-bold">{product.name}</h1>
        <p className="text-sm muted mt-1">{product.description}</p>
      </div>
      <div className="card overflow-x-auto">
        <h2 className="font-semibold mb-3 text-lg">Supplier taqqoslash</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b border-slate-200">
              <th>Supplier</th>
              <th>Narx</th>
              <th>ETA</th>
              <th>Rating</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {product.offers.map((offer: any) => (
              <tr key={offer.id} className="border-b border-slate-100">
                <td className="py-2">{offer.supplier_name}</td>
                <td className="font-semibold">{money(offer.price)}</td>
                <td>{offer.delivery_eta_hours} soat</td>
                <td>{offer.supplier_rating || 0} / 5</td>
                <td>
                  <button className="btn" onClick={() => addToCart(offer.id)}>Savatga</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {msg && <p className="mt-3 muted">{msg}</p>}
      </div>
    </div>
  );
}
