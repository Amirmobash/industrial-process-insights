# Herkunft, Änderungen und Lizenzhinweise

## Mitgelieferte Quellen

- `visuals/pulsechart`: Nutzer-Upload `powerbi-visuals-pulsechart-master(1).zip`; Repository https://github.com/PowerBi-Projects/powerbi-visuals-pulsechart ; ursprüngliches Microsoft-Projekt https://github.com/microsoft/powerbi-visuals-pulsechart . Version laut package.json: 2.5.0.
- `visuals/kmeans`: Nutzer-Upload `PowerBI-visuals-clustering-kmeans-master(1).zip`; Repository https://github.com/PowerBi-Projects/PowerBI-visuals-clustering-kmeans ; ursprüngliches Microsoft-Projekt https://github.com/microsoft/PowerBI-visuals-clustering-kmeans . Version laut package.json: 1.0.6.

Die ZIPs enthalten keine verlässliche Commit-ID. SHA-256-Prüfsummen der hochgeladenen Archive stehen in `QUELLEN_SHA256.txt`.

## Änderungen

Neue Integration: Python-Analyse, standardisiertes Clustering, Ereigniserkennung je Anlage, gemeinsame CSV, deutsches Offline-Dashboard, synthetische Beispieldaten, Power-Query-Vorlage, DAX-Beispiele und Tests. Der neue Ablauf verwendet den Quellcode der historischen Visuals nicht zur Laufzeit; die Visuals werden als eigenständige Power-BI-Module mitgeliefert.

In beiden Visual-Modulen wurde die ursprüngliche README als `README.upstream.md` bewahrt und eine deutsche README ergänzt. Anzeigenamen und Beschreibungen in `pbiviz.json` und `capabilities.json` wurden lokalisiert. Interne Datenrollen, technische Namen, GUIDs und Algorithmen bleiben unverändert. Pulse Chart behält seine vollständigen Sprachressourcen. Bestehende englische Codekommentare, R-Laufzeitmeldungen und upstream Dokumente wurden nicht vollständig übersetzt.

## Lizenzen

Die TypeScript-Dateien beider Originalmodule enthalten Microsoft-Copyright- und MIT-Lizenztexte. Pulse Chart nennt außerdem MIT in package.json. Diese Hinweise bleiben vollständig erhalten. Der R-Code enthält eigene Microsoft- und Drittanbieterhinweise, die ebenfalls erhalten bleiben. Drittanbieterabhängigkeiten behalten ihre eigenen Lizenzbedingungen.

`LICENSE` gilt für neu hinzugefügte Integrationsdateien. Daraus entsteht keine Änderung der Lizenz oder Urheberschaft der enthaltenen Originaldateien. Dies ist ein unabhängiges Portfolio-/Demonstrationsprojekt und kein offizielles Microsoft-Produkt.
