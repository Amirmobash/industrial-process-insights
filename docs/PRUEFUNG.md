# Prüfprotokoll

Folgende Prüfungen wurden für den neuen Integrationsablauf erfolgreich ausgeführt:

- Vier Python-Tests: reproduzierbare Gruppen, Skalierungsinvarianz, konstante Merkmale, unzulässige Messwerte, Ereigniswechsel je Anlage und vollständiger CSV-/HTML-Export.
- Demoanalyse mit 360 Messungen: CSV, Modellmetadaten und eingebettete HTML-Daten erzeugt.
- JavaScript-DOM-Funktionstest mit Node.js: initialer Aufbau beider Diagramme, Anlagenfilter, Clustermarkierung, Punktdetails und Messgrößenwechsel. Der Test nutzt ein minimales DOM-Modell; er ersetzt keine Browserprüfung.

Nicht durchgeführt: visuelle Browserprüfung (kein Browser-Binary im Ausführungsumfeld), Build der historischen `.pbiviz`-Module, Ausführung des alten R-Codes und Import in Power BI Desktop. Ein produktiver Anlagenbetrieb wurde nicht geprüft.

Erneut ausführen, im Hauptordner:

```sh
python -m unittest discover -s tests -v
python src/pipeline.py
node tests/test_dashboard.cjs
```

Die GitHub-Actions-Datei führt diese Prüfungen nach dem Upload aus. Sie benötigt die Freigabe von Actions im Repository und wurde noch nicht auf GitHub ausgeführt.
