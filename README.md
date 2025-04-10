# Django Project: 🚗 Pitlane CRM Backend

**Pitlane** ist ein modular aufgebautes CRM-Backend, entwickelt mit Django. Es stellt die serverseitige Basis für ein Customer-Relationship-Management-System bereit – optimiert für Performance, Erweiterbarkeit und Integration mit modernen Frontends (z. B. Svelte, Angular, React).

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

```

---

## 🌐 API
Die REST-API basiert auf Django Ninja und bietet:

Schnelle Entwicklung durch Pydantic-basierte Schemas

Eingebaute Validierung und automatische OpenAPI/Swagger-Dokumentation

Integration mit JWT oder Session-Auth möglich

Nach dem Start erreichst du die Swagger-Doku unter:

```bash
http://localhost:8000/api/docs
```
---

## 🧩 Packages aus requirements.txt
Paket	Version	Beschreibung
| Paket              | Version   | Beschreibung                                       |
|--------------------|-----------|----------------------------------------------------|
| `Django`           | 5.2       | Hauptframework für das Backend                     |
| `django-ninja`     | 1.4.1     | Modernes REST-Framework mit Pydantic               |
| `django-environ`   | 0.12.0    | Umgebungsvariablen & `.env`-Konfiguration          |
| `pydantic`         | 2.11.3    | Datenvalidierung & Serialisierung                  |
| `pydantic_core`    | 2.33.1    | Interner Kern von Pydantic                         |
| `annotated-types`  | 0.7.0     | Zusätzliche Metadaten für Typannotationen          |
| `typing-inspection`| 0.4.0     | Werkzeuge zur Analyse von Python-Typen             |
| `typing_extensions`| 4.13.2    | Erweiterung moderner Typ-Features                  |
| `asgiref`          | 3.8.1     | ASGI-Unterstützung für Django                      |
| `sqlparse`         | 0.5.3     | SQL-Parser für Django-Migrationssystem             |
| `tzdata`           | 2025.2    | Zeitzonendaten für Umgebungen ohne Systemdaten     |
| `psycopg2`         | 2.9.10    | PostgreSQL-Treiber für Python                      |
| `mysqlclient`      | 2.2.7     | MySQL-Treiber (nur bei Verwendung von MySQL nötig) |

ℹ️ Je nach verwendeter Datenbank brauchst du nur psycopg2 (für PostgreSQL) oder mysqlclient (für MySQL).

---

## 🛠 Entwicklungsumgebung
Folgende Tools können für die Weiterentwicklung hilfreich sein:

- Visual Studio Code – als IDE

- Postman – für API-Tests

- pgAdmin / MySQL Workbench – zur DB-Verwaltung
