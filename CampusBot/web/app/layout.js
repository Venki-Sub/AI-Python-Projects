import "./globals.css";
import ChatWidget from "../components/ChatWidget";

export const metadata = {
  title: "École Schulz · CampusBot",
  description: "Le site de l'École Schulz avec son assistant CampusBot.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>
        {children}
        <ChatWidget />
      </body>
    </html>
  );
}
