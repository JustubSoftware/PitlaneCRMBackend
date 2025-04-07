# Django Project: 🚗 Pitlane CRM Backend

**Pitlane** ist ein modular aufgebautes CRM-Backend, entwickelt mit Django. Es stellt die serverseitige Basis für ein Customer-Relationship-Management-System bereit – optimiert für Performance, Erweiterbarkeit und Integration mit modernen Frontends (z. B. Angular, React).

---

## 📦 Features

- Nutzer- und Rollenverwaltung (Admin, Support, Vertrieb)
- Kunden- und Kontaktdatenverwaltung
- API-Schnittstellen für Frontend-Anbindung
- Authentifizierung via JWT oder Session (anpassbar)
- Zentrale Konfiguration mit `.env`
- Erweiterbar um Module wie Terminplanung, Fahrzeughistorie, Angebote u.v.m.

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
