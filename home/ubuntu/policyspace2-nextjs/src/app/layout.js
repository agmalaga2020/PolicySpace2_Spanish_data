import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'PolicySpace2 - Adaptación al Contexto Español',
  description: 'Herramientas para adaptar PolicySpace2 al contexto español, permitiendo obtener datos españoles equivalentes a los utilizados en el proyecto original brasileño.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
