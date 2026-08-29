import "./globals.css";

export const metadata = {
  title: 'Technocore Contributor',
  description: 'Technocore onboarding application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
