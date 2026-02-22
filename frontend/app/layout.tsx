import './globals.css';
import Link from 'next/link';
import { Sora, IBM_Plex_Sans } from 'next/font/google';

const sora = Sora({ subsets: ['latin'], weight: ['500', '700'] });
const plex = IBM_Plex_Sans({ subsets: ['latin'], weight: ['400', '500', '600'] });

export const metadata = {
  title: 'SITE-TO-DOOR MVP',
  description: 'Qurilish materiallari marketplace',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body className={plex.className}>
        <header className="sticky top-0 z-40 backdrop-blur border-b border-slate-200/70 bg-white/80">
          <div className="container-main py-3 flex gap-4 items-center justify-between">
            <Link href="/" className={`${sora.className} text-lg font-bold tracking-tight text-slate-900`}>
              SITE-TO-DOOR
            </Link>
            <nav className="flex flex-wrap justify-end gap-2 text-sm">
              <Link href="/cart" className="rounded-full bg-slate-100 px-3 py-1.5 hover:bg-slate-200">Savat</Link>
              <Link href="/orders" className="rounded-full bg-slate-100 px-3 py-1.5 hover:bg-slate-200">Buyurtmalar</Link>
              <Link href="/supplier" className="rounded-full bg-slate-100 px-3 py-1.5 hover:bg-slate-200">Supplier</Link>
              <Link href="/driver" className="rounded-full bg-slate-100 px-3 py-1.5 hover:bg-slate-200">Driver</Link>
            </nav>
          </div>
        </header>
        <main className="container-main py-7">{children}</main>
      </body>
    </html>
  );
}
