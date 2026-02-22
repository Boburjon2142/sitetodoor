'use client';

import { useEffect, useState } from 'react';
import { api, getToken } from '@/lib/api';

export default function OrderDetailPage({ params }: { params: { id: string } }) {
  const [tracking, setTracking] = useState<any>(null);

  useEffect(() => {
    api(`/tracking/orders/${params.id}/`, { token: getToken() }).then(setTracking);
  }, [params.id]);

  const statusClass =
    tracking?.status === 'delivered'
      ? 'status-delivered'
      : tracking?.status === 'on_the_way'
        ? 'status-onway'
        : 'status-preparing';

  if (!tracking) return <div className="card">Yuklanmoqda...</div>;

  return (
    <div className="space-y-4">
      <div className="card">
        <h1 className="text-2xl font-bold tracking-tight">Buyurtma #{tracking.order_id}</h1>
        <p className="mt-2">
          Holat: <span className={statusClass}>{tracking.status}</span>
        </p>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2 text-lg">Status tarixi</h2>
        {tracking.timeline.map((e: any) => (
          <p key={e.id} className="text-sm muted">{e.status} - {new Date(e.created_at).toLocaleString()}</p>
        ))}
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2 text-lg">Driver lokatsiyasi (MVP)</h2>
        {tracking.last_location ? (
          <p className="text-sm muted">Lat: {tracking.last_location.latitude}, Lng: {tracking.last_location.longitude}</p>
        ) : (
          <p className="text-sm muted">Lokatsiya hali kelmagan</p>
        )}
        <div className="mt-2 h-44 rounded-xl border border-dashed border-slate-300 bg-slate-50 flex items-center justify-center text-sm muted">
          Xarita placeholder (OSM integratsiyasi keyingi bosqich)
        </div>
      </div>
    </div>
  );
}
