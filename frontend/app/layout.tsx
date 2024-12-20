import Navbar from "@/components/navbar";
import "@/styles/globals.css";
import type { AppProps } from "next/app";


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
      >
        <Navbar />
        {children}
      </body>
    </html>
  );
}
