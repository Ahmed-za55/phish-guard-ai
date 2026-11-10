import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Phish Guard AI",
  description:
    "Check a link, message or email for phishing. Every verdict comes with the reasons behind it, and private mode keeps your details away from the AI provider.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}