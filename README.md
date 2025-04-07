# Django Project: Pitlane CRN Backend

Ein Webanwendungsprojekt basierend auf dem Django-Framework. Dieses Projekt dient als Grundlage für die Entwicklung einer performanten, modularen und erweiterbaren Backend-Applikation mit optionalem Frontend-Anschluss (z. B. Angular oder React).

---

## 🔧 Voraussetzungen

- Python 3.10+
- pip
- Virtualenv (empfohlen)
- PostgreSQL/MySQL/SQLite (je nach Konfiguration)

---

## 🚀 Installation

```bash
# Repository klonen
git clone https://github.com/JustubSoftware/PitlaneCRMBackend.git
cd dein-repo

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# .env Datei anlegen (optional, falls benötigt)
cp .env.example .env

# Migrationen durchführen
python manage.py migrate

# Superuser erstellen (für Admin-Login)
python manage.py createsuperuser

# Server starten
python manage.py runserver
