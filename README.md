# Planspiel WebApp

## Überblick

Dieses Projekt verwandelt ein lokales Unternehmenssimulationsspiel in eine öffentlich zugängliche Webanwendung. Sie ist sowohl für Spieler als auch für Spielleiter (Game Masters, GMs) konzipiert, um über eine benutzerfreundliche Schnittstelle mit der Spieleumgebung zu interagieren.

## Erstkonfiguration

Um mit dieser Webanwendung zu starten, folgen Sie diesen Schritten:

1. **GitHub Repository Klonen**:
   - Klonen Sie das Repository auf Ihren lokalen Rechner, um Zugriff auf den Quellcode zu erhalten.

2. **Datenbank Einrichten**:
   - Richten Sie die Datenbank ein, mit der die Anwendung interagieren wird. Stellen Sie sicher, dass sie richtig konfiguriert ist und läuft.

3. **Datenbank-URL Konfigurieren**:
   - Ändern Sie die Datenbank-URL im Code, um die Anwendung mit Ihrer Datenbank zu verbinden.

4. **.htm Dateien Öffentlich Zugänglich Machen**:
   - Stellen Sie sicher, dass die .htm Dateien öffentlich zugänglich sind, da sie für die Web-Schnittstelle der Anwendung wesentlich sind.

## Datenbankstruktur

Die Datenbank besteht aus mehreren Tabellen, die für den Betrieb des Unternehmenssimulationsspiels wesentlich sind. Nachfolgend ist die detaillierte Struktur der Haupttabellen aufgeführt:

### "Teams" Tabelle

- **`name`** (String, 100 Zeichen, Primärschlüssel, Einzigartig): Stellt den Namen des Teams dar.
- **`password`** (String, 100 Zeichen): Speichert das Passwort für das Teamkonto.

### "Game" Tabelle

- **`id`** (Integer, Primärschlüssel): Eindeutige Kennung für jedes Spiel.
- **`name`** (String, 100 Zeichen, Einzigartig): Name des Spiels.
- **`status`** (String, 100 Zeichen): Aktueller Status des Spiels.
- **`num_companies`** (Integer): Anzahl der Unternehmen im Spiel.
- **`num_periods`** (Integer): Anzahl der Perioden im Spiel.
- **`offset`** (Integer): Offset-Wert für das Spiel.
- **`num_markets`** (Integer): Anzahl der Märkte im Spiel.
- **`num_cells`** (Integer): Anzahl der Zellen in jedem Markt.
- **`market_0_activation`** bis **`market_3_activation`** (Integer): Aktivierungsstatus verschiedener Märkte.
- **`ideal_rd`** (Integer): Idealer F&E-Wert.
- **`cost_industry_report`**, **`cost_market_report`** (Float): Kosten für verschiedene Berichte.
- **`current_period`** (Integer, Standard=0): Aktuelle Periode des Spiels.

### "Turn" Tabelle

- **`id`** (Integer, Primärschlüssel): Eindeutige Kennung für jeden Zug.
- **`game_id`** (Integer, Fremdschlüssel - `games.id`): Verweis auf das Spiel.
- **`turn_number`** (Integer): Nummer des Zuges.
- **`submission_time`** (DateTime, Standard=Aktueller Zeitstempel): Zeitpunkt der Einreichung für den Zug.
- **Preispolitik, Produktpolitik, Marketing, Vertrieb, Marktforschung, Produktionsplan, Materialbeschaffung, Technische Anlagen, Personalwesen, Finanzwesen Felder**: Verschiedene Felder für Spieldaten (Floats, Strings).



Dieses Projekt ist unter Apache License lizenziert. Bitte sehen Sie die LIZENZDATEI für weitere Details.
