"""Sensoranalyse: standardisierte K-Means-Cluster und gemeinsame Ereigniszeitreihe."""
from __future__ import annotations
import argparse
import csv
import json
import math
import random
from datetime import datetime
from pathlib import Path

FEATURES = ('Temperatur_C', 'Druck_bar', 'Vibration_mm_s')
REQUIRED = ('Zeitstempel', 'Anlage', *FEATURES, 'Ereignis')


def load_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not set(REQUIRED).issubset(reader.fieldnames or []):
            raise ValueError('Fehlende Spalten: ' + ', '.join(sorted(set(REQUIRED) - set(reader.fieldnames or []))))
        rows, seen = [], set()
        for line, row in enumerate(reader, 2):
            try:
                stamp = datetime.fromisoformat(row['Zeitstempel'])
                if stamp.tzinfo is None:
                    raise ValueError('Zeitstempel benötigt Zeitzone')
                if not row['Anlage'].strip():
                    raise ValueError('Anlage ist leer')
                key = (stamp, row['Anlage'])
                if key in seen:
                    raise ValueError('Doppelter Zeitstempel je Anlage')
                seen.add(key)
                for field in FEATURES:
                    row[field] = float(row[field])
                    if not math.isfinite(row[field]):
                        raise ValueError('Nicht endlicher Messwert')
                row['Ereignis'] = row['Ereignis'] or ''
                rows.append(row)
            except (ValueError, TypeError) as exc:
                raise ValueError(f'Zeile {line}: {exc}') from exc
    if not rows:
        raise ValueError('Keine Messdaten vorhanden')
    return sorted(rows, key=lambda r: (datetime.fromisoformat(r['Zeitstempel']), r['Anlage']))


def distance(a, b):
    return sum((x-y)**2 for x, y in zip(a, b))


def cluster(points, k=3, seed=42, max_iter=200):
    if k < 2 or k > len(points) or k > len(set(map(tuple, points))):
        raise ValueError('k muss zwischen 2 und der Anzahl unterschiedlicher Messpunkte liegen')
    means = [sum(col)/len(points) for col in zip(*points)]
    scales = [math.sqrt(sum((v-m)**2 for v in col)/len(points)) or 1.0 for col, m in zip(zip(*points), means)]
    scaled = [[(v-m)/s for v,m,s in zip(p, means, scales)] for p in points]
    # Mehrfachinitialisierung; Distanzberechnung erfolgt in standardisierten Einheiten.
    best = None
    for attempt in range(10):
        rng = random.Random(seed + attempt)
        centers = [scaled[rng.randrange(len(scaled))][:]]
        while len(centers) < k:
            weights = [min(distance(p,c) for c in centers) for p in scaled]
            centers.append(scaled[rng.choices(range(len(scaled)), weights=weights)[0]][:])
        previous = None
        for iteration in range(max_iter):
            labels = [min(range(k), key=lambda j: distance(p, centers[j])) for p in scaled]
            if labels == previous:
                break
            previous = labels[:]
            for j in range(k):
                members = [p for p,label in zip(scaled,labels) if label == j]
                if members:
                    centers[j] = [sum(col)/len(members) for col in zip(*members)]
                else:
                    centers[j] = max(scaled, key=lambda p: min(distance(p,c) for c in centers))[:]
        labels = [min(range(k), key=lambda j: distance(p, centers[j])) for p in scaled]
        score = sum(distance(p,centers[label]) for p,label in zip(scaled,labels))
        if best is None or score < best[0]:
            best = score, labels, centers, iteration + 1
    score, labels, centers, iterations = best
    # Stabile Nummerierung nach Temperatur; keine automatische Fehlerdiagnose.
    order = sorted(range(k), key=lambda j: tuple(centers[j]))
    mapping = {old:new+1 for new,old in enumerate(order)}
    physical = [[round(v*s+m,6) for v,s,m in zip(centers[j],scales,means)] for j in order]
    return [mapping[label] for label in labels], {'merkmale':list(FEATURES), 'mittelwerte':means, 'standardabweichungen':scales, 'zentren':physical, 'traegheit':score, 'iterationen':iterations, 'seed':seed, 'k':k}


def analyse(rows, k=3):
    labels, model = cluster([[r[f] for f in FEATURES] for r in rows], k)
    last, result = {}, []
    for index, (row,label) in enumerate(zip(rows, labels), 1):
        row = dict(row)
        old = last.get(row['Anlage'])
        title = row['Ereignis']
        change = old is not None and old != label
        if change:
            title = ' · '.join(filter(None, [title, 'Clusterwechsel']))
        row.update(Messung_ID=index, Cluster=label, Ereignistitel=title,
                   Ereignisbeschreibung=(f'Cluster {old} → {label}. ' if change else '') + row['Ereignis'],
                   Ereignisgroesse=1 if title else 0)
        last[row['Anlage']] = label
        result.append(row)
    return result, model


def run(input_path, output, k=3):
    rows, model = analyse(load_csv(input_path), k)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with (output/'prozessdaten_cluster.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output/'modell.json').write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding='utf-8')
    template = (Path(__file__).parent/'dashboard.html').read_text(encoding='utf-8')
    payload = json.dumps({'rows': rows, 'model': model}, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    (output/'dashboard.html').write_text(template.replace('__DATEN_JSON__', payload), encoding='utf-8')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/sensordaten_demo.csv', help='CSV mit Sensorwerten')
    parser.add_argument('--output', default='output', help='Ausgabeordner')
    parser.add_argument('--clusters', type=int, default=3, help='Anzahl der Cluster')
    args = parser.parse_args()
    try:
        rows = run(args.input,args.output,args.clusters)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Fehler: {exc}\n')
    print(f'{len(rows)} Messungen verarbeitet. Dashboard: {args.output}/dashboard.html')

if __name__ == '__main__':
    main()
