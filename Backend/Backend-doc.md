# Dokumentation - main.py

## Übersicht
Diese Flask-Webanwendung stellt ein Backend für ein Spiel-Simulationssystem bereit. Es ermöglicht die Registrierung und Authentifizierung von Benutzergruppen, die Verwaltung von Spielen und Spielrunden sowie die Durchführung verschiedener spielbezogener Aktionen.

### Hauptkomponenten
- **Flask**: Ein Mikro-Webframework für Python.
- **SQLAlchemy**: SQL Toolkit und Object-Relational Mapper (ORM).
- **Flask JWT Extended**: JWT-Erweiterung für Flask zur Handhabung von Web Token für Authentifizierung.
- **Pandas**: Eine Bibliothek für Datenanalyse und -manipulation.
- **Marshmallow**: ORM/ODM-Framework zur Serialisierung und Deserialisierung von Objekten.

## Datenmodelle

### Klasse `Team`
- **Funktion**: Definiert ein Team mit Namen und Passwort.
- **Attribute**: `name`, `password`.

### Klasse `Game`
- **Funktion**: Beschreibt ein Spiel mit verschiedenen Attributen.
- **Attribute**: `id`, `name`, `status`, `num_companies`, `num_periods`, `offset`, `num_markets`, `num_cells`, `market_0_activation` etc.

### Klasse `Turn`
- **Funktion**: Stellt eine Spielrunde dar.
- **Attribute**: `id`, `game_id`, `turn_number`, `submission_time`, `team_name`, `inputSolidVerkaufspreisInland` etc.

## Endpunkte

### Endpunkt: `frontend_files`
- **URL**: `/<path:filename>`
- **Methode**: `GET`
- **Beschreibung**: Dient zur Auslieferung von Frontend-Dateien.

### Endpunkt: `register_team`
- **URL**: `/team`
- **Methode**: `POST`
- **Beschreibung**: Registriert ein neues Team.

### Endpunkt: `login`
- **URL**: `/login`
- **Methode**: `POST`
- **Beschreibung**: Handhabt den Login-Prozess für Teams.

### Endpunkt: `gamemaster`
- **URL**: `/gamemaster`
- **Methode**: `GET`
- **Beschreibung**: Bereitstellung von Spielmaster-spezifischen Daten.

### Endpunkt: `register_team_by_gamemaster`
- **URL**: `/gamemaster/register_team`
- **Methode**: `POST`
- **Beschreibung**: Ermöglicht dem Spielmaster, ein Team zu registrieren.

### Endpunkt: `register_game`
- **URL**: `/gamemaster/register_game`
- **Methode**: `POST`
- **Beschreibung**: Ermöglicht dem Spielmaster, ein Spiel zu registrieren.

### Endpunkt: `update_game`
- **URL**: `/game/<int:game_id>`
- **Methode**: `PUT`
- **Beschreibung**: Aktualisiert Spielinformationen.

### Endpunkt: `get_games`
- **URL**: `/games`
- **Methode**: `GET`
- **Beschreibung**: Ruft Informationen über alle Spiele ab.

### Endpunkt: `get_teams`
- **URL**: `/teams`
- **Methode**: `GET`
- **Beschreibung**: Ruft Informationen über alle Teams ab.

### Endpunkt: `delete_team`
- **URL**: `/teams/<string:team_name>`
- **Methode**: `DELETE`
- **Beschreibung**: Löscht ein spezifisches Team.

### Endpunkt: `change_team_password`
- **URL**: `/teams/<string:team_name>/change_password`
- **Methode**: `PUT`
- **Beschreibung**: Ändert das Passwort eines Teams.

### Endpunkt: `add_turn`
- **URL**: `/turn`
- **Methode**: `POST`
- **Beschreibung**: Fügt eine neue Spielrunde hinzu.

### Endpunkt: `upload_file`
- **URL**: `/upload`
- **Methode**: `POST`
- **Beschreibung**: Ermöglicht das Hochladen einer Datei.

### Endpunkt: `save_file`
- **URL**: `/save`
- **Methode**: `POST`
- **Beschreibung**: Speichert Daten in einer Datei und sendet diese zurück.

### Endpunkt: `get_games_for_team`
- **URL**: `/games-for-team`
- **Methode**: `GET`
- **Beschreibung**: Ruft Spiele für ein spezifisches Team ab.

### Endpunkt: `check_lock_status`
- **URL**: `/check-lock-status`
- **Methode**: `GET`
- **Beschreibung**: Überprüft den Sperrstatus für ein Team in einem Spiel.

### Endpunkt: `lock_team`
- **URL**: `/lock-team`
- **Methode**: `POST`
- **Beschreibung**: Sperrt ein Team in einem Spiel.

### Endpunkt: `unlock_team`
- **URL**: `/unlock-team`
- **Methode**: `POST`
- **Beschreibung**: Entsperrt ein Team in einem Spiel.

### Endpunkt: `submit_turn`
- **URL**: `/submit-turn`
- **Methode**: `POST`
- **Beschreibung**: Ermöglicht die Einreichung einer Spielrunde durch ein Team.

### Endpunkt: `next_round`
- **URL**: `/next_round`
- **Methode**: `POST`
- **Beschreibung**: Startet die nächste Runde in einem Spiel.

## Server
Der Server wird gestartet, wenn das Script als Hauptprogramm ausgeführt wird.


</br></br></br></br></br></br></br></br>


# Dokumentation returnReports.py

## Überblick
Dieses Python-Skript ist für ein komplexes Unternehmenssimulationsmodell entwickelt. Es umfasst zwei Hauptklassen, `InputHandler` und `DataProcessor`, die für die Interaktion mit einer Datenbank und die darauf folgende Verarbeitung von Unternehmensdaten zuständig sind.

## Verwendete Bibliotheken und Module
- **IPython**: Ermöglicht erweiterte Interaktionen innerhalb von Jupyter-Notebooks.
- **sys**: Wird genutzt, um auf Python-Interpreter-bezogene Funktionen zuzugreifen.
- **time**: Bietet Funktionen zur Handhabung von Zeit, einschließlich Messungen und Verzögerungen.
- **numpy (np)**: Ermöglicht umfangreiche numerische Operationen, insbesondere auf Arrays und Matrizen.
- **openpyxl**: Wird zum Lesen und Schreiben von Excel-Dateien verwendet.
- **xlwings (xw)**: Dient zur direkten Interaktion mit Excel-Dateien und -Programmen.
- **MK_GMS_Pro_Modules (mod)**: Ein benutzerdefiniertes Modul, wahrscheinlich mit spezialisierten Funktionen für das Geschäftsszenario.
- **SQLAlchemy**: Ein mächtiges SQL-Toolkit und ORM, das die Interaktion mit relationalen Datenbanken erleichtert.

## Klasse: InputHandler
### Beschreibung
Diese Klasse ist verantwortlich für das Laden und Verarbeiten von Eingabedaten aus einer Datenbank.

### Konstruktor: `__init__(self, db_url)`
Initialisiert eine Datenbankverbindung.
- `db_url`: Eine Zeichenkette, die die Datenbank-URL angibt.

### Methode: `load_decision_data(self, game_id, team, period)`
Lädt spezifische Daten basierend auf Spiel-ID, Team und Periode.
- `game_id`: Die eindeutige Identifikationsnummer des Spiels.
- `team`: Der Name oder die Identifikation des Teams.
- `period`: Die spezifische Periode im Spiel.

## Klasse: DataProcessor
### Beschreibung
Verarbeitet und analysiert Entscheidungsdaten und erzeugt daraus Berichte.

### Konstruktor: `__init__(self, db_url, MAIN_DIR)`
Initialisiert wichtige Einstellungen und Datenbankverbindungen.
- `db_url`: URL der Datenbank.
- `MAIN_DIR`: Der Hauptverzeichnispfad für die Dateiverwaltung.

### Methode: `process_decisions(self, game_id, GMS_NAME, GMS_VERSION, SETUP_FILE, NUM_CELLS, UL_CELLS)`
Die Hauptmethode zur Verarbeitung von Geschäftsentscheidungen und Berichtserstellung.
- `game_id`: Die Identifikationsnummer des Spiels.
- `GMS_NAME`: Der Name des Geschäftsmodellsimulationssystems.
- `GMS_VERSION`: Die Version des Geschäftsmodellsimulationssystems.
- `SETUP_FILE`: Eine Konfigurationsdatei für das System.
- `NUM_CELLS`: Die Anzahl der Zellen in der Simulation, möglicherweise für die Anordnung oder Aufteilung von Daten.
- `UL_CELLS`: Ein spezifischer Konfigurationswert, dessen genauer Zweck aus dem Kontext nicht klar ist.

### Datenverarbeitungslogik
- Das Skript startet mit Datenbankabfragen, um Informationen über Teams, Spiele und Perioden zu extrahieren.
- Anschließend werden Szenariodaten geladen und analysiert.
- Es nutzt `openpyxl` und `xlwings` für die Erstellung und das Update von Excel-Berichten.
- Das Skript führt vielfältige Berechnungen durch, um verschiedene Aspekte des Geschäfts wie Produktqualität, Kundenzufriedenheit, Markenstärke, Personalentwicklung und Finanzen zu analysieren.

## Zusammenfassung
Das Skript ist eine umfassende Lösung für die Analyse und Berichterstattung in einem Unternehmenssimulationsspiel. Es kombiniert fortgeschrittene Datenverarbeitungs- und Analysetechniken mit spezialisierten Funktionen für den Umgang mit Excel-Daten und -Interaktionen.


</br></br></br></br></br></br></br></br>


# Dokumentation MK_GMS_Pro_Setup.py
## Einleitung
Diese Dokumentation beschreibt den Aufbau und die Funktionsweise des Vorprogramms der General Management Simulation `MK_GM_Pro`. Ziel des Programms ist das Einrichten einer Unternehmenssimulation und die Bereitstellung relevanter Szenario-Dateien.

## Verwendete Bibliotheken und Module
- **IPython**: Ermöglicht das Ausführen von IPython magic commands zur Umgebungssteuerung.
- **sys**: Zum Hinzufügen von Pfaden zum Systempfad.
- **os**: Für Betriebssystem-Interaktionen wie Verzeichniserstellung.
- **shutil**: Zum Löschen von Verzeichnissen.
- **openpyxl**: Zum Laden von Excel-Arbeitsmappen.
- **numpy (np)**: Für numerische Operationen und Array-Handhabung.
- **MK_GMS_Pro_Modules (mod)**: Importiert benutzerdefinierte Module spezifisch für MK_GM_Pro.

## Konfiguration und Definitionen
### Spielkonfiguration
- `GMS_NAME`: Name des Planspiels.
- `NUM_COMPANIES`: Anzahl der Unternehmen in der Simulation.
- `GMS_VERSION`: Versionsbezeichnung des Planspiels.
- `SETUP_FILE`: Name der Setup-Datei.
- `MAIN_DIR`: Hauptverzeichnis des Planspiels.
- `SUB_DIR`, `SCEN_DIR`, `GMS_DIR`: Spezifizierung von Unterordnern.
- `GMS_directory`: Konstruiertes Verzeichnis für das Planspiel.

### Konstanten
- `MAX_PERIODS`, `NUM_PERIODS`, `OFFSET`: Definition von Simulationsperioden und Offset.
- `NUM_MARKETS`: Anzahl der Märkte.
- `MARKET_0` bis `MARKET_3`, `IDEAL_RD`: Spezifische Marktkonstanten.
- `NUM_CELLS`, `UL_CELLS`: Konfiguration für Werkstätten.
- `COST_INDUSTRY_REPORT`, `COST_MARKET_REPORT`: Kosten für Berichte.

### Verzeichniserstellung
Erstellt und bereinigt notwendige Verzeichnisse für das Planspiel.

## Szenario-Datenverarbeitung
### Szenario-Bereiche
- `info_list`: Definiert wichtige Bereiche in den Excel-Tabellen zur Datenaufnahme.
- `szenario_bereiche`: Erstellt ein Dictionary aus `info_list` für den Zugriff auf spezifische Excel-Bereiche.

### Laden und Verarbeiten von Szenario-Daten
Lädt Szenario-Daten aus einer Excel-Datei und speichert diese in einem `szenario` Dictionary.

## Unternehmens-Datenverarbeitung
### Definition der Excel-Zellen
Definiert die relevanten Excel-Zellen für Unternehmensdaten.

### Laden von Unternehmens-Daten
Lädt und verarbeitet spezifische Unternehmensdaten aus einer Excel-Arbeitsmappe.

### Initialisierung von Historien-Arrays
Initialisiert Historien-Arrays für verschiedene Unternehmensaspekte wie Marketing, Fertigung und Finanzen.

### Speichern von Unternehmensdaten
Speichert die bearbeiteten Unternehmensdaten in einem binären Format.

## Schlussfolgerung
Das Vorprogramm für die `MK_GM_Pro` General Management Simulation ist verantwortlich für die Initialisierung und Vorbereitung der Simulationsumgebung, einschließlich des Ladens und Verarbeitens von Szenario- und Unternehmensdaten sowie der Verwaltung von Verzeichnissen.


</br></br></br></br></br></br></br></br>


# Dokumentation MK_GMS_Pro_Modules.py

## Überblick
Dieses Python-Skript ist Teil eines komplexen Simulationsmodells, das verschiedene Aspekte des Unternehmensmanagements umfasst. Es enthält Funktionen für die Handhabung von Marktsimulationen, darunter Absatzmärkte, Kundenzufriedenheit, Produktqualität, Mitarbeitermanagement und Finanzmarktinteraktionen.

## Verwendete Bibliotheken
- **numpy (np)**: Eine zentrale Bibliothek für numerische Berechnungen in Python, insbesondere im Umgang mit Arrays und mathematischen Funktionen.

## Kernfunktionalitäten des Skripts
Das Skript bietet Funktionen zur Simulation und Analyse verschiedener Geschäftsbereiche und Szenarien:

### 1. Excel-Interaktion
Das Skript nutzt Funktionen zum Lesen und Schreiben von Excel-Daten, wobei Bereiche in Excel-Tabellen als Inputs verwendet und Ergebnisse dort eingetragen werden.

### 2. Unternehmenssimulation
Der Kern des Skripts umfasst Modelle zur Simulation verschiedener Unternehmensbereiche:
- **Absatzmärkte (Produktqualität, Marketing-Mix, Kundenzufriedenheit, Markenstärke)**
- **Arbeitsmarkt (Einstellungen, Mitarbeiterproduktivität und -motivation)**
- **Finanzmarkt (Unternehmensrating und Zinsaufschlag)**

### 3. Berechnung von Wirkungszusammenhängen
Für viele Bereiche werden spezielle Funktionen verwendet, um den Einfluss von Entscheidungen auf wichtige Metriken wie Qualität, Kundenzufriedenheit, Mitarbeitermotivation und Finanzkennzahlen zu berechnen.

### 4. Anwendung spezifischer Berechnungsmodelle
Das Skript verwendet verschiedene mathematische und statistische Modelle (z. B. Moving-Average-Prozesse, lineare Interpolationen, ARMA-Prozesse), um realistische Unternehmensdynamiken zu simulieren.

### 5. Kommentierung und Fehlerbehandlung
Der Code enthält umfangreiche Kommentare zur Erklärung der Funktionen und ihrer Anwendungen. Einige Funktionen enthalten grundlegende Fehlerbehandlungen.


</br></br></br></br></br></br></br></br>



# Dokumentation MK_GMS_Pro_ChartsProduction.py

## Übersicht
Das Programm `MK_GMS_Pro` dient zur Auswertung einer Unternehmenssimulation, insbesondere im Bereich Fertigung, Personalwesen und Finanzen. Es analysiert und visualisiert Daten aus einem simulierten Unternehmensumfeld, um Einblicke in verschiedene Geschäftsaspekte zu ermöglichen.

## Simulationsumgebung
- **IPython Magic Commands:** Die ersten Zeilen des Programms verwenden IPython-spezifische Befehle (`%clear` und `%reset`), um die Arbeitsumgebung vorzubereiten.
- **Simulierte Periode und Planspiel-Details:**
  - `PERIOD`: Definiert die simulierte Periode.
  - `GMS_NAME` und `GMS_VERSION`: Name und Version des Planspiels.
  - `SETUP_FILE`: Name der Setup-Datei.
  - `MAIN_DIR`, `SUB_DIR`, `SCEN_DIR`, `GMS_DIR`: Verzeichnispfade für das Planspiel.
- **Verzeichnispfade und Module:**
  - Der Code bereitet Pfade vor und lädt notwendige Python-Module (pandas, numpy, plotnine).

## Datenmanagement
- **Laden von Setup-Daten:** Nutzt NumPy, um Konfigurationsdaten aus einer `.npz`-Datei zu laden.
- **Definition von Konstanten:** Beinhaltet Konstanten wie Anzahl von Unternehmen, Perioden, Märkten und anderen geschäftsspezifischen Metriken.
- **Pfade für Szenarien und Unternehmen:** Erstellt Pfade für das Szenario und jedes beteiligte Unternehmen.
- **Laden von Unternehmensdaten:** Liest weitere Daten aus einer `.npz`-Datei.

## Datenbereitstellung und Visualisierung
- **Auswahl von Daten für Grafiken:** Definiert, welche Daten in Quer- und Längsschnittgrafiken dargestellt werden sollen.
- **Datenbereitstellung:** Organisiert und formatiert Daten für die Visualisierung.
- **Graphenerzeugung:**
  - **Querschnittsdaten (Cross Sectional):** Erzeugt Säulendiagramme für ausgewählte Variablen.
  - **Längsschnittdaten (Time Series):** Erzeugt Liniendiagramme für Zeitreihendaten.



</br></br></br></br></br></br></br></br>


# Dokumentation MK_GMS_Pro_ChartsMarketing.py

## Übersicht
Das Programm `MK_GMS_Pro` speziell für die Marketing-Analyse in einer Unternehmenssimulation konzipiert. Es bietet Einblicke in Marketingkennzahlen verschiedener Märkte.

## Simulationsumgebung
- **IPython Magic Commands:** Der Code beginnt mit IPython-spezifischen Befehlen zur Vorbereitung der Arbeitsumgebung.
- **Simulierte Periode und Planspiel-Details:**
  - `PERIOD`: Bestimmt die aktuelle simulierte Periode.
  - `GMS_NAME`, `GMS_VERSION`: Name und Version des Planspiels.
  - `SETUP_FILE`: Setup-Datei für das Planspiel.
  - `MAIN_DIR`, `SUB_DIR`, `SCEN_DIR`, `GMS_DIR`: Pfade für das Planspiel und seine Ressourcen.
- **Verzeichnispfade und Module:**
  - Definition von Pfaden und Laden von Python-Modulen für Datenanalyse und Visualisierung (pandas, numpy, plotnine).

## Datenmanagement
- **Setup-Daten Laden:** Import von Konfigurationsdaten aus einer `.npz`-Datei.
- **Konstantendefinition:**
  - Anzahl von Unternehmen, Perioden, Märkten und weiteren geschäftsspezifischen Konstanten.
- **Pfaddefinitionen für Szenarien und Unternehmen:** Erstellung von Pfaden für das Szenario und jedes beteiligte Unternehmen.
- **Unternehmensdaten Laden:** Import zusätzlicher Daten aus einer `.npz`-Datei.

## Datenbereitstellung und Visualisierung
- **Auswahl von Daten für Grafiken:** Festlegung, welche Daten in Querschnitt- und Längsschnittgrafiken präsentiert werden.
- **Datenbereitstellung:**
  - Organisation und Formatierung von Marketingdaten (z.B. Verkaufspreise, Absatzzahlen, Kundenzufriedenheit) für die Visualisierung.
- **Graphenerzeugung:**
  - **Querschnittsdaten (Cross Sectional):** Erzeugung von Säulendiagrammen für ausgewählte Variablen auf verschiedenen Märkten.
  - **Längsschnittdaten (Time Series):** Erstellung von Liniendiagrammen für Zeitreihendaten (falls vorhanden).