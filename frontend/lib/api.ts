export type ApiOptions = {
  method?: string;
  body?: any;
  token?: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1';

export async function api(path: string, options: ApiOptions = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
    cache: 'no-store',
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.error?.message || data?.message || 'API xatolik');
  return data;
}

export function getToken() {
  if (typeof window === 'undefined') return '';
  return localStorage.getItem('access') || '';
}

export function money(value: number | string) {
  return `${Number(value).toLocaleString('uz-UZ')} UZS`;
}
