import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NextWord AI",
  description: "Predict your next word using deep learning and LSTM neural networks.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}