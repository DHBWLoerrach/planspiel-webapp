gamemaster-test.htm: 

Funktionen zur Anzeigeumschaltung
- toggleDisplay(elementId): Diese Funktion ändert die Anzeige eines Elements zwischen 'none' (versteckt) und 'block' (sichtbar), abhängig vom aktuellen Zustand. Sie ermöglicht das Ein- und Ausblenden von Formularen auf der Seite durch Klicken auf die entsprechenden Buttons.

Ereignisbehandler für Button-Klicks
- Event Listener für 'registerTeamBtn': Wenn der Button "Register New Team" geklickt wird, ruft dieser Event Listener die toggleDisplay-Funktion auf, um das Formular zur Teamregistrierung anzuzeigen oder zu verbergen.
- Event Listener für 'registerGameBtn': Beim Klicken auf "Register New Game" wird nicht nur das Formular zum Registrieren eines neuen Spiels umgeschaltet, sondern auch die Funktion fetchTeamsAndGames aufgerufen, um vorhandene Teams und Spiele zu laden.

Registrierung neuer Teams und Spiele
- Registrierung eines neuen Teams (Event Listener für 'newTeamForm'): Bei der Einreichung des Formulars zur Teamregistrierung wird ein POST-Request an einen Server gesendet, um das neue Team mit Namen und Passwort zu registrieren. Im Erfolgs- oder Fehlerfall wird eine entsprechende Benachrichtigung angezeigt.
- Registrierung eines neuen Spiels (Event Listener für 'newGameForm'): Ähnlich der Teamregistrierung, aber mit zusätzlichen Daten für das Spiel, wie gewählte Teams, aktive Märkte und spezifische Spieleinstellungen. Nach erfolgreicher Registrierung oder bei einem 
Fehler wird der Benutzer benachrichtigt.

Dynamisches Laden und Anzeigen von Teams und Spielen
- fetchTeamsAndGames(): Lädt die aktuellen Daten der Teams und Spiele vom Server und aktualisiert die Inhalte der entsprechenden Tabellen auf der Seite. Für jedes geladene Team und Spiel werden die Funktionen addTeamRow bzw. addGameRow aufgerufen.
- addGameRow(game, gamesTableBody): Fügt der Tabelle der aktiven Spiele eine neue Zeile hinzu, die Informationen über das Spiel enthält, einschließlich eines Buttons zum Löschen des Spiels.
- addTeamRow(team, teamsTableBody): Fügt der Teamtabelle eine neue Zeile hinzu, mit Informationen zum Team und Buttons zum Löschen des Teams oder zum Ändern des Passworts.

Löschen von Teams und Spielen
- deleteGame(gameId): Sendet einen DELETE-Request an den Server, um ein Spiel zu löschen. Nach erfolgreicher Löschung oder im Fehlerfall wird der Benutzer informiert.
- deleteTeam(teamId): Ähnlich wie deleteGame, aber für das Löschen von Teams. Auch hier wird der Benutzer über den Erfolg oder Misserfolg des Löschvorgangs informiert.

Ändern von Team-Passwörtern
- changeTeamPassword(teamName): Ermöglicht das Ändern des Passworts für ein Team. Der Benutzer wird aufgefordert, ein neues Passwort einzugeben, welches dann per PUT-Request an den Server gesendet wird.

Logout-Funktionalität
- Event Listener für 'logoutBtn': Entfernt den Authentifizierungstoken aus dem lokalen Speicher und leitet den Benutzer zur Login-Seite um.



index.htm

JavaScript-Funktionalität im Login-Code
- Event Listener für das Login-Formular:
Beim Absenden des Formulars (submit) werden Standardaktionen unterbunden (e.preventDefault()).
Die eingegebenen Benutzerdaten (Name und Passwort) werden ausgelesen.
Ein asynchroner POST-Request mit diesen Daten wird an die Login-API gesendet (fetch('http://127.0.0.1:5000/login', {...})).
Auf Basis der Antwort vom Server wird der Zugriffstoken im lokalen Speicher gespeichert und eine Umleitung je nach Benutzerrolle (is_gamemaster) durchgeführt: entweder zur Seite gamemaster-test.htm oder player.htm.
Bei Fehlern im Request-Prozess wird eine Fehlermeldung in der Konsole ausgegeben.



player.htm

Laden und Initialisierung
- window.onload: Liest den gespeicherten Login-Namen aus dem lokalen Speicher und zeigt ihn im entsprechenden HTML-Element an.
- DOMContentLoaded-Listener: Ruft fetchGamesForTeam auf, um verfügbare Spiele zu laden, und initialisiert Event Listener für die UI-Interaktion.

Spiel- und Datenverwaltung
- fetchGamesForTeam(): Lädt verfügbare Spiele für das Team vom Server und zeigt bei mehreren Spielen ein Auswahlfenster an oder wählt automatisch ein Spiel aus, wenn nur eines verfügbar ist.
- selectGamePrompt(games): Zeigt ein Auswahlfenster für verfügbare Spiele.
- showModal(modalId) und hideModal(modalId): Funktionen zum Anzeigen bzw. Verbergen von modalen Fenstern.
- gameSelectionMade(): Wählt das im modalen Fenster ausgewählte Spiel aus und speichert die Auswahl.
- selectGame(game): Speichert das ausgewählte Spiel im lokalen Speicher und zeigt die aktuelle Periode des Spiels an.

Berechnungen und Aktualisierungen
- initializeInputListeners(): Initialisiert Event Listener für Eingabefelder zur Aktualisierung von zusammengefassten Werten.
- findSumIdForInput(inputId): Ermittelt, ob ein Eingabefeld Teil einer Summenberechnung ist.
- updateSum(sumId): Aktualisiert die Summenwerte basierend auf den Eingaben in verbundenen Feldern.

Datenübermittlung
- submitFormData(): Sammelt alle eingegebenen Daten aus den Formularfeldern und sendet sie in einem POST-Request an den Server.

Sonstiges
- Logout-Button-Event-Listener: Entfernt den Zugriffstoken aus dem lokalen Speicher und leitet den Benutzer zur Login-Seite um.



test1.html

Laden und Initialisierung
- window.onload & DOMContentLoaded: Nicht explizit definiert, aber durch ähnliche Struktur impliziert, dass beim Laden der Seite initialisierende Funktionen aufgerufen werden könnten.

Tab-Verwaltung
- changeTab(evt, tabName): Wechselt den aktiven Tab und den zugehörigen Inhalt basierend auf dem übergebenen Tab-Namen. Andere Tabs werden ausgeblendet, der ausgewählte Tab hervorgehoben.

Formular-Anzeigeumschaltung
- toggleDisplay(elementId): Schaltet die Sichtbarkeit eines Formulars um, basierend auf dessen aktuellem Display-Status.

Event Listener für Button-Klicks
- Register Team Button: Zeigt das Formular zur Teamregistrierung an/aus beim Klick.
- Register Game Button: Zeigt das Formular zur Spielregistrierung an/aus beim Klick und lädt vorhandene Teams.

Select2 Initialisierung
- $(document).ready: Initialisiert Select2 für das <select>-Element, um die Team-Auswahl zu verbessern.

Registrierung neuer Teams und Spiele
- newTeamForm-Event-Listener: Behandelt das Absenden des Teamregistrierungsformulars durch Senden eines POST-Requests.
- newGameForm-Event-Listener: Behandelt das Absenden des Spielregistrierungsformulars.

Datenmanagement
- fetchTeams(): Lädt verfügbare Teams vom Server zur Auswahl beim Registrieren eines neuen Spiels.
- fetchTeamsAndPopulate(): Lädt Teams und fügt sie zur Anzeige hinzu.
- addGameRow(game) & deleteGame(gameId): Funktionen zum Hinzufügen und Löschen von Spielen aus der Tabelle.
- addTeamRow(team) & deleteTeam(teamId): Funktionen zum Hinzufügen und Löschen von Teams aus der Tabelle.

Logout-Funktionalität
- logoutBtn-Event-Listener: Entfernt den Zugriffstoken und leitet zur Login-Seite um.

Erweiterung der Tab-Funktionalität
- fetchSpieleUndErstelleTabs(): Lädt Spieleinformationen und erstellt für jedes Spiel einen Tab sowie einen zugehörigen Inhaltsbereich.
- erstelleTabFuerSpiel(spiel) & erstelleInhaltsbereichFuerSpiel(spiel): Erstellen dynamisch Tabs und Inhalte für jedes geladene Spiel.
- initTabsEventListeners(): Initialisiert Event-Listener für die dynamisch erstellten Tabs, um die Inhaltsanzeige zu wechseln.



Styling: 

Grundlegendes Layout und Styling
- Globale Stile (*): Setzt box-sizing: border-box; für alle Elemente, um Breiten- und Höhenberechnungen inklusive Padding und Border zu vereinfachen. Setzt zudem die Standard-Margin und Padding aller Elemente auf 0.
- Körper (body): Definiert die Schriftart, Hintergrundfarbe, Farbe des Textes sowie Margin und Padding des gesamten Körperbereichs.

Container und Navigation
- Container (container): Erstellt ein flexibles Layout mit einer Mindesthöhe von 100vh (Viewport Height), um sicherzustellen, dass der Container immer mindestens die gesamte Höhe des Viewports einnimmt.
- Menu (menu): Bestimmt das Aussehen der Navigationsleiste inklusive Hintergrundfarbe und flexibler Anordnung der Inhalte.

Tabs und Inhalt
- Tab (tab): Stilisiert die Tabs der Navigation. Definiert unter anderem die Padding, Cursor-Art, Farbe und einen unteren Rand. Über Hover- und Active-Zustände wird die Interaktivität hervorgehoben.
- Inhaltsbereich (tab-content): Stilisiert den Bereich, in dem der Inhalt der verschiedenen Tabs angezeigt wird. Standardmäßig sind alle Inhalte versteckt (display: none;), nur der aktive Inhalt wird angezeigt.

Spezifische Stile
- Buttons: Bestimmt das Aussehen von Buttons, einschließlich Hintergrund- und Textfarbe, Padding, Grenzen, Cursor-Art und Übergangseffekte für das Hover-Verhalten.
- Formulare und Eingabefelder: Definiert das Aussehen von Formularen und deren Eingabefelder. Setzt Farben, Padding, Margin, Hintergrundfarbe, Grenzen und Rundungen.
- Select2-spezifische Stile: Passt die Darstellung von Select2-Auswahlfeldern an, um diese konsistent mit dem dunklen Designthema zu gestalten.

Tabellenstyling
- Tabellen (table): Passt das Aussehen der Tabellen an, einschließlich Breite, Grenzenzusammenfallen, Hintergrundfarbe und Abstand.
- Tabellenkopf- und Zellen (th, td): Stilisiert die Kopf- und Datenzellen der Tabelle, inklusive Grenzen, Padding, Textausrichtung und Farbe.
- Tabellenkopf-Hintergrund (thead): Definiert eine spezifische Hintergrundfarbe für den Kopfbereich der Tabellen.

Sichtbarkeitsklassen
- Versteckt (hidden) und Sichtbar (visible): Hilfsklassen zur Steuerung der Sichtbarkeit von Elementen.