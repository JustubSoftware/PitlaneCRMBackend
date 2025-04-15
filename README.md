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

## API-Endpunkte

Dieser Abschnitt beschreibt die verfügbaren API-Endpunkte zur Verwaltung des Werkstatt-CRMs.

### Kunden

*   `GET /api/customers/`: Ruft eine Liste aller Kunden ab.
*   `POST /api/customers/`: Erstellt einen neuen Kunden.
*   `GET /api/customers/{customer_id}/`: Ruft einen bestimmten Kunden anhand seiner ID ab.
*   `PUT /api/customers/{customer_id}/`: Aktualisiert einen bestimmten Kunden anhand seiner ID.
*   `DELETE /api/customers/{customer_id}/`: Löscht einen bestimmten Kunden anhand seiner ID.

### Fahrzeuge

*   `GET /api/vehicles/`: Ruft eine Liste aller Fahrzeuge ab.
*   `POST /api/vehicles/`: Erstellt ein neues Fahrzeug.
*   `GET /api/vehicles/{vehicle_id}/`: Ruft ein bestimmtes Fahrzeug anhand seiner ID ab.
*   `PUT /api/vehicles/{vehicle_id}/`: Aktualisiert ein bestimmtes Fahrzeug anhand seiner ID.
*   `DELETE /api/vehicles/{vehicle_id}/`: Löscht ein bestimmtes Fahrzeug anhand seiner ID.
*   `GET /api/vehicles/customer/{customer_id}`: Ruft alle Fahrzeuge für einen bestimmten Kunden ab.

### Mechaniker

*   `GET /api/mechanics/`: Ruft eine Liste aller Mechaniker ab.
*   `POST /api/mechanics/`: Erstellt einen neuen Mechaniker.
*   `GET /api/mechanics/{mechanic_id}/`: Ruft einen bestimmten Mechaniker anhand seiner ID ab.
*   `PUT /api/mechanics/{mechanic_id}/`: Aktualisiert einen bestimmten Mechaniker anhand seiner ID.
*   `DELETE /api/mechanics/{mechanic_id}/`: Löscht einen bestimmten Mechaniker anhand seiner ID.
*   `GET /api/mechanics/available`: Ruft alle verfügbaren Mechaniker ab.

### Teile

*   `GET /api/parts/`: Ruft eine Liste aller Teile ab.
*   `POST /api/parts/`: Erstellt ein neues Teil.
*   `GET /api/parts/{part_id}/`: Ruft ein bestimmtes Teil anhand seiner ID ab.
*   `PUT /api/parts/{part_id}/`: Aktualisiert ein bestimmtes Teil anhand seiner ID.
*   `DELETE /api/parts/{part_id}/`: Löscht ein bestimmtes Teil anhand seiner ID.
*   `GET /api/parts/search?query={suchbegriff}`: Sucht Teile anhand eines Suchbegriffs.

### Dienstleistungen

*   `GET /api/services/`: Ruft eine Liste aller Dienstleistungen ab.
*   `POST /api/services/`: Erstellt eine neue Dienstleistung.
*   `GET /api/services/{service_id}/`: Ruft eine bestimmte Dienstleistung anhand ihrer ID ab.
*   `PUT /api/services/{service_id}/`: Aktualisiert eine bestimmte Dienstleistung anhand ihrer ID.
*   `DELETE /api/services/{service_id}/`: Löscht eine bestimmte Dienstleistung anhand ihrer ID.

### Aufträge

*   `GET /api/orders/`: Ruft eine Liste aller Aufträge ab.
*   `POST /api/orders/`: Erstellt einen neuen Auftrag.
*   `GET /api/orders/{order_id}/`: Ruft einen bestimmten Auftrag anhand seiner ID ab.
*   `PUT /api/orders/{order_id}/`: Aktualisiert einen bestimmten Auftrag anhand seiner ID.
*   `DELETE /api/orders/{order_id}/`: Löscht einen bestimmten Auftrag anhand seiner ID.

### Auftragsstatus

*   `GET /api/orderstatuses/`: Ruft eine Liste aller Auftragsstatus ab.
*   `POST /api/orderstatuses/`: Erstellt einen neuen Auftragsstatus.
*   `GET /api/orderstatuses/{orderstatus_id}/`: Ruft einen bestimmten Auftragsstatus anhand seiner ID ab.
*   `PUT /api/orderstatuses/{orderstatus_id}/`: Aktualisiert einen bestimmten Auftragsstatus anhand seiner ID.
*   `DELETE /api/orderstatuses/{orderstatus_id}/`: Löscht einen bestimmten Auftragsstatus anhand seiner ID.
*   `GET /api/orders/{order_id}/statuses`: Ruft alle Statusänderungen für einen bestimmten Auftrag ab.

### Auftragsdienstleistungen

*   `GET /api/orderservices/`: Ruft eine Liste aller Auftragsdienstleistungen ab.
*   `POST /api/orderservices/`: Erstellt eine neue Auftragsdienstleistung.
*   `GET /api/orderservices/{orderservice_id}/`: Ruft eine bestimmte Auftragsdienstleistung anhand ihrer ID ab.
*   `PUT /api/orderservices/{orderservice_id}/`: Aktualisiert eine bestimmte Auftragsdienstleistung anhand ihrer ID.
*   `DELETE /api/orderservices/{orderservice_id}/`: Löscht eine bestimmte Auftragsdienstleistung anhand ihrer ID.

### Auftragsteile

*   `GET /api/orderparts/`: Ruft eine Liste aller Auftragsteile ab.
*   `POST /api/orderparts/`: Erstellt ein neues Auftragsteil.
*   `GET /api/orderparts/{orderpart_id}/`: Ruft ein bestimmtes Auftragsteil anhand seiner ID ab.
*   `PUT /api/orderparts/{orderpart_id}/`: Aktualisiert ein bestimmtes Auftragsteil anhand seiner ID.
*   `DELETE /api/orderparts/{orderpart_id}/`: Löscht ein bestimmtes Auftragsteil anhand seiner ID.

### Rechnungen

*   `GET /api/invoices/`: Ruft eine Liste aller Rechnungen ab.
*   `POST /api/invoices/`: Erstellt eine neue Rechnung.
*   `GET /api/invoices/{invoice_id}/`: Ruft eine bestimmte Rechnung anhand ihrer ID ab.
*   `PUT /api/invoices/{invoice_id}/`: Aktualisiert eine bestimmte Rechnung anhand ihrer ID.
*   `DELETE /api/invoices/{invoice_id}/`: Löscht eine bestimmte Rechnung anhand ihrer ID.
*   `PUT /api/invoices/{invoice_id}/mark_paid`: Markiert eine Rechnung als bezahlt.
*    `GET /api/invoices/order/{order_id}`: Ruft die Rechnung für einen bestimmten Auftrag ab.

### Zahlungen

*   `GET /api/payments/`: Ruft eine Liste aller Zahlungen ab.
*   `POST /api/payments/`: Erstellt eine neue Zahlung.
*   `GET /api/payments/{payment_id}/`: Ruft eine bestimmte Zahlung anhand ihrer ID ab.
*   `PUT /api/payments/{payment_id}/`: Aktualisiert eine bestimmte Zahlung anhand ihrer ID.
*   `DELETE /api/payments/{payment_id}/`: Löscht eine bestimmte Zahlung anhand ihrer ID.

### Benachrichtigungen

*   `GET /api/notifications/`: Ruft eine Liste aller Benachrichtigungen ab.
*   `POST /api/notifications/`: Erstellt eine neue Benachrichtigung.
*   `GET /api/notifications/{notification_id}/`: Ruft eine bestimmte Benachrichtigung anhand ihrer ID ab.
*   `PUT /api/notifications/{notification_id}/`: Aktualisiert eine bestimmte Benachrichtigung anhand ihrer ID.
*   `DELETE /api/notifications/{notification_id}/`: Löscht eine bestimmte Benachrichtigung anhand ihrer ID.

### Spezialisierte Endpunkte

*   `GET /api/orders/{order_id}/statuses`: Ruft alle Statusänderungen für einen bestimmten Auftrag ab.
*   `GET /api/vehicles/customer/{customer_id}`: Ruft alle Fahrzeuge eines bestimmten Kunden ab.
*   `GET /api/invoices/order/{order_id}`: Ruft die Rechnung für einen bestimmten Auftrag ab (falls vorhanden).
*   `GET /api/parts/search?query={suchbegriff}`: Sucht Teile anhand des Namens oder der Teilenummer.
*   `POST /api/orders/{order_id}/add_service/{service_id}?quantity={menge}`: Fügt eine Dienstleistung zu einem Auftrag hinzu (optionale Menge).
*   `POST /api/orders/{order_id}/add_part/{part_id}?quantity={menge}`: Fügt ein Teil zu einem Auftrag hinzu (optionale Menge).
*   `PUT /api/invoices/{invoice_id}/mark_paid`: Markiert eine Rechnung als bezahlt.
    `GET /api/mechanics/available`: Ruft alle verfügbaren Mechaniker ab.



