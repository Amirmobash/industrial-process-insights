# In dein GitHub-Repository hochladen

Ziel: https://github.com/Amirmobash/industrial-process-insights

## Über die Weboberfläche

1. ZIP vollständig entpacken.
2. Repository öffnen und **Add file → Upload files** wählen (bei einem leeren Repository gegebenenfalls **uploading an existing file**).
3. Den **Inhalt** des Ordners `industrial-process-insights` hochladen, nicht nur die ZIP-Datei und nicht den äußeren Ordner. `README.md`, `src`, `visuals`, `data`, `output`, `docs` und `powerbi` gehören auf die oberste Ebene.
4. Commit-Nachricht: `Deutsche Prozessanalyse mit Clustering und Ereigniszeitreihe hinzufügen`.

Die Weboberfläche hat Upload-Grenzen. Falls zu viele Dateien vorliegen oder versteckte Dateien wie `.github` nicht mitkommen, GitHub Desktop oder Git verwenden.

## Mit Git

In einem neuen Arbeitsordner:

```sh
git clone https://github.com/Amirmobash/industrial-process-insights.git
cd industrial-process-insights
```

Dann den gesamten Inhalt des entpackten Projektordners **einschließlich versteckter Dateien** in den geklonten Ordner kopieren, ohne dessen `.git`-Ordner zu verändern.

```sh
git add .
git commit -m "Deutsche Prozessanalyse mit Clustering und Ereigniszeitreihe hinzufügen"
git push origin main
```

Beschreibungsvorschlag für das Repository:

> Industrielle Prozessanalyse mit K-Means-Clustering, ereignisbasierter Zeitreihe und Power-BI-Integration.

Mögliche Topics: `powerbi`, `industrial-automation`, `kmeans`, `sensor-data`, `process-monitoring`, `python`.
