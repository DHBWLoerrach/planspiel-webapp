index.htm:

### `Event Listener für das Login-Formular`
- **Funktion:** Verarbeitet die Einreichung des Login-Formulars.
- **Aktion:** Verhindert die Standardaktion des Formulars, liest Benutzername und Passwort aus den Eingabefeldern aus und sendet diese in einem POST-Request an den Server.
- **Zweck:** Authentifiziert den Benutzer gegenüber dem Server und leitet ihn basierend auf seiner Rolle (Game Master oder Spieler) auf die entsprechende Seite weiter.



player.htm:

### `fetchGamesForTeam`
- **Funktion:** Lädt verfügbare Spiele für das Team vom Server.
- **Aktion:** Sendet eine GET-Anfrage an den Server, um die Spiele zu erhalten.
- **Zweck:** Stellt die Spiele bereit, die dem Team zugeordnet sind, und ermöglicht die Auswahl für den Benutzer.

### `selectGamePrompt`
- **Funktion:** Zeigt ein Auswahlfenster für verfügbare Spiele.
- **Aktion:** Füllt das `gameSelect` Dropdown mit den geladenen Spielen.
- **Zweck:** Ermöglicht dem Benutzer, ein Spiel aus der Liste der verfügbaren Spiele auszuwählen.

### `showModal`
- **Funktion:** Zeigt ein modales Fenster an.
- **Aktion:** Setzt die `display`-Eigenschaft des spezifizierten Modal-Elements auf `block`.
- **Zweck:** Zeigt ein Modal-Fenster auf der Benutzeroberfläche an, z.B. zur Spielauswahl.

### `gameSelectionMade`
- **Funktion:** Verarbeitet die Auswahl eines Spiels durch den Benutzer.
- **Aktion:** Liest die ausgewählte Spiel-ID und speichert das ausgewählte Spiel.
- **Zweck:** Legt das aktuell ausgewählte Spiel fest und aktualisiert die Anzeige entsprechend.

### `hideModal`
- **Funktion:** Versteckt das angegebene modale Fenster.
- **Aktion:** Setzt die `display`-Eigenschaft des Modal-Elements auf `none`.
- **Zweck:** Verbirgt das Modal-Fenster, nachdem der Benutzer eine Auswahl getroffen hat oder das Fenster schließen möchte.

### `selectGame`
- **Funktion:** Speichert das ausgewählte Spiel und aktualisiert die Anzeige.
- **Aktion:** Speichert das ausgewählte Spiel im lokalen Speicher und zeigt dessen aktuelle Periode an.
- **Zweck:** Aktualisiert die Benutzeroberfläche mit Informationen zum ausgewählten Spiel.

### `initializeInputListeners`
- **Funktion:** Initialisiert Event Listener für Eingabefelder zur Summenberechnung.
- **Aktion:** Fügt `input` Event Listener zu allen numerischen Eingabefeldern hinzu.
- **Zweck:** Aktualisiert zusammengefasste Werte basierend auf den Eingaben der Benutzer in Echtzeit.

### `findSumIdForInput`
- **Funktion:** Ermittelt die Summen-ID für ein Eingabefeld.
- **Aktion:** Durchsucht `sumConfig`, um die entsprechende Summen-ID zu finden.
- **Zweck:** Hilft bei der Bestimmung, welche Summenwerte aktualisiert werden müssen, wenn Benutzereingaben ändern.

### `updateSum`
- **Funktion:** Aktualisiert die Summenwerte basierend auf Eingaben.
- **Aktion:** Berechnet neue Summenwerte und aktualisiert das entsprechende Element.
- **Zweck:** Hält zusammengefasste Informationen auf der Benutzeroberfläche konsistent mit den Benutzereingaben.

### `submitFormData`
- **Funktion:** Sammelt und übermittelt Formulardaten an den Server.
- **Aktion:** Sammelt Daten aus Formulareingaben und sendet diese in einem POST-Request.
- **Zweck:** Übermittelt die Eingaben des Benutzers für das aktuelle Spiel zur Verarbeitung an den Server.

### `checkLockStatus`
- **Funktion:** Überprüft den Sperrstatus des Teams für das aktuelle Spiel.
- **Aktion:** Sendet eine GET-Anfrage, um den Sperrstatus des Teams zu überprüfen.
- **Zweck:** Verhindert, dass der Benutzer Änderungen vornimmt, wenn das Team für das aktuelle Spiel gesperrt ist.



gamemaster.htm:

### `deleteGame`
- **Funktion:** Löscht ein Spiel basierend auf seiner ID.
- **Aktion:** Sendet eine DELETE-Anfrage an den Server mit der spezifischen Spiel-ID.
- **Zweck:** Ermöglicht dem Benutzer, ein Spiel aus der Liste der aktiven Spiele zu entfernen.

### `deleteTeam`
- **Funktion:** Löscht ein Team basierend auf seiner ID.
- **Aktion:** Sendet eine DELETE-Anfrage an den Server mit der spezifischen Team-ID.
- **Zweck:** Ermöglicht dem Benutzer, ein Team aus der Liste zu entfernen.

### `toggleDisplay`
- **Funktion:** Umschalten der Anzeige von Elementen.
- **Aktion:** Wechselt die CSS-Eigenschaft `display` zwischen `none` und `block`.
- **Zweck:** Ermöglicht das Ein- und Ausblenden von Formularen für die Registrierung von Teams und Spielen.

### `fetchTeamsAndGames`
- **Funktion:** Lädt Teams und Spiele vom Server und zeigt sie an.
- **Aktion:** Sendet GET-Anfragen, um Teams und Spiele zu laden, und aktualisiert die UI entsprechend.
- **Zweck:** Stellt aktuelle Daten zu Teams und Spielen bereit und zeigt diese in Tabellenform an.

### `addGameRow`
- **Funktion:** Fügt der Tabelle der Spiele eine neue Zeile hinzu.
- **Aktion:** Erstellt und füllt eine neue Tabellenzeile mit Spielinformationen und fügt Aktionsschaltflächen hinzu.
- **Zweck:** Ermöglicht die Anzeige von Spielinformationen und bietet Interaktionsmöglichkeiten wie das Starten der nächsten Runde oder das Löschen des Spiels.

### `addTeamRow`
- **Funktion:** Fügt der Teamtabelle eine neue Zeile hinzu.
- **Aktion:** Erstellt und füllt eine neue Tabellenzeile mit Teaminformationen und fügt Aktionsschaltflächen hinzu.
- **Zweck:** Ermöglicht die Anzeige von Teaminformationen und bietet Interaktionsmöglichkeiten wie das Ändern des Passworts oder das Löschen des Teams.

### `changeTeamPassword`
- **Funktion:** Ermöglicht das Ändern des Passworts für ein Team.
- **Aktion:** Zeigt ein Prompt für die Eingabe eines neuen Passworts an und sendet es in einem PUT-Request.
- **Zweck:** Ermöglicht dem Benutzer, das Passwort eines Teams zu aktualisieren.

### `$(document).ready` für Select2
- **Funktion:** Initialisiert Select2 für Dropdown-Listen.
- **Aktion:** Wählt die Elemente `#newGameTeams` und `#marketActivations` und wendet Select2 auf sie an.
- **Zweck:** Verbessert die Benutzerfreundlichkeit der Dropdown-Listen durch das Hinzufügen von Such- und Filterfunktionen.
