# Einrichtung in Power BI Desktop

## Gemeinsame Datenbasis importieren

1. Zuerst `python src/pipeline.py` ausführen oder die mitgelieferte Ergebnis-CSV verwenden.
2. In Power BI Desktop über **Daten abrufen → Text/CSV** die Datei `output/prozessdaten_cluster.csv` wählen. UTF-8 und Komma verwenden.
3. In Power Query `Messung_ID`, `Cluster` und `Ereignisgroesse` auf ganze Zahl setzen; die drei Sensorspalten mit Gebietsschema **Englisch (USA)** als Dezimalzahl einlesen. Das CSV verwendet Dezimalpunkte.
4. `Zeitstempel` als Datum/Uhrzeit/Zeitzone einlesen. Für Diagramme in Power Query auf UTC normalisieren und als Datum/Uhrzeit bereitstellen. Die Vorlage `powerbi/Prozessdaten.pq` übernimmt das. Im Modell heißt das Feld `Zeit_UTC`.
5. Tabelle **Prozessdaten** nennen. Cluster als Kategorie, nicht als summierten Messwert behandeln. Die DAX-Beispiele aus `powerbi/Kennzahlen.dax` hinzufügen.

## Gemeinsame Berichtsseite

Zwei Slicer: **Anlage** und **Cluster**. Dazu Kennzahlen für Messungen und Ereignisse.

### Zeitreihe / Pulse Chart

Sofern ein kompatibler Pulse Chart installiert oder separat erfolgreich gebaut wurde:

| Datenrolle des Pulse Chart | Feld |
|---|---|
| Timestamp / Zeitstempel | `Zeit_UTC`, ohne Datumshierarchie |
| Values / Werte | `Temperatur_C`, Mittelwert |
| Event Title / Ereignistitel | `Ereignistitel` |
| Event Description / Ereignisbeschreibung | `Ereignisbeschreibung` |
| Event Size / Ereignisgröße | `Ereignisgroesse`, Maximum |

**Eine Anlage auswählen**, damit gleichzeitige Messungen verschiedener Anlagen nicht versehentlich gemittelt werden. Bei fehlendem kompatiblem Custom Visual ein natives Liniendiagramm und eine Ereignistabelle mit demselben Anlagenfilter verwenden. CSV-Import erzeugt noch keinen fertigen Bericht.

### Clusteransicht mit gemeinsamem Modell

Ein natives Streudiagramm anlegen:

- X-Achse: `Temperatur_C`.
- Y-Achse: `Vibration_mm_s`.
- Legende: `Cluster` als Kategorie.
- Details / eindeutige Punktkennung: `Messung_ID` (Feldbezeichnung hängt von der Desktop-Version ab).
- Tooltips: Anlage, Zeitstempel, Druck_bar, Ereignisbeschreibung.

Sicherstellen, dass jede Messung als eigener Punkt erscheint. Über **Interaktionen bearbeiten** die gewünschte Filterung zwischen den Diagrammen aktivieren. Der Cluster-Slicer filtert beide Diagramme über dieselbe Tabelle.

### Historisches R-Visual (optional)

Das originale K-Means-Visual kann unabhängig getestet werden: Values = drei Sensorwerte; PointLabels = Anlage oder Messung_ID; ID = Messung_ID. Standardisierung aktivieren. Dieses Visual trainiert sein eigenes Modell. Seine Gruppen werden **nicht** automatisch in die Pulse-Zeitreihe zurückgeschrieben. Deshalb verwendet der integrierte Bericht die vom Python-Ablauf berechnete Cluster-Spalte.

## Historische Quellmodule bauen

`visuals/kmeans` verlangt laut Originalkonfiguration Power BI Visuals Tools **1.10.0**; `visuals/pulsechart` verlangt **2.1.0**. Beide haben eigene `package.json` und `pbiviz.json`. Sie dürfen nicht durch Zusammenkopieren ihrer TypeScript-Dateien in einen Build vermischt werden.

Die Originalskripte `npm install` und `npm run package` sind erhalten. Das ist eine historische Build-Rezeptur, keine Bestätigung, dass sie mit aktuellem Node.js oder Power BI funktioniert. Die Altmodule wurden hier weder kompiliert noch in Power BI Desktop getestet. R ist für die neue Python-Analyse nicht erforderlich; das alte R-Visual benötigt R und dessen im Original dokumentierte Pakete.

## Betrieb

Es gibt keine Live-Verbindung zu PLC, OPC UA oder SCADA. Für neue Daten den Analyseablauf erneut starten und anschließend Power BI aktualisieren. Automatische Aktualisierung und Deployment sind nicht eingerichtet. OEE/MTBF werden nicht berechnet, da dafür zusätzliche fachlich definierte Zustands- und Produktionsdaten nötig sind.
