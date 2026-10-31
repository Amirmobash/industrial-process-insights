// Als neue leere Abfrage einfügen und Pfad anpassen. Abfragename: Prozessdaten.
let
    Dateipfad = "C:\Daten\industrial-process-insights\output\prozessdaten_cluster.csv",
    Quelle = Csv.Document(File.Contents(Dateipfad), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Kopf = Table.PromoteHeaders(Quelle, [PromoteAllScalars=true]),
    Typen = Table.TransformColumnTypes(Kopf, {
        {"Zeitstempel", type datetimezone}, {"Anlage", type text},
        {"Temperatur_C", type number}, {"Druck_bar", type number},
        {"Vibration_mm_s", type number}, {"Messung_ID", Int64.Type},
        {"Cluster", Int64.Type}, {"Ereignisgroesse", Int64.Type},
        {"Ereignis", type text}, {"Ereignistitel", type text}, {"Ereignisbeschreibung", type text}
    }, "en-US"),
    ZeitUTC = Table.AddColumn(Typen, "Zeit_UTC", each DateTimeZone.RemoveZone(DateTimeZone.ToUtc([Zeitstempel])), type datetime)
in
    ZeitUTC
