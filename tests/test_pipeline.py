import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pipeline import cluster, analyse, load_csv, run, FEATURES
ROOT=Path(__file__).resolve().parents[1]

class PipelineTests(unittest.TestCase):
    def test_scale_invariance_and_repeatability(self):
        points=[[i*.01,i*.02,i*.03] for i in range(8)]+[[10+i*.01,20+i*.02,30+i*.03] for i in range(8)]
        labels,_=cluster(points,2)
        changed,_=cluster([[p[0]*1000,p[1],p[2]] for p in points],2)
        self.assertEqual(labels,changed)
        self.assertEqual(labels,cluster(points,2)[0])
        self.assertEqual(len(set(labels[:8])),1)
        self.assertNotEqual(labels[0],labels[-1])

    def test_no_cross_asset_transition(self):
        rows=[]
        for a,v in [('A',0),('B',10),('A',0),('B',10)]:
            rows.append(dict(Anlage=a,Ereignis='Prüfung' if not rows else '',**dict(zip(FEATURES,[v]*3))))
        result,_=analyse(rows,2)
        self.assertFalse(any('Clusterwechsel' in r['Ereignistitel'] for r in result))
        self.assertEqual(result[0]['Ereignistitel'],'Prüfung')
        rows[-1].update(dict(zip(FEATURES,[0]*3)))
        self.assertIn('Clusterwechsel',analyse(rows,2)[0][-1]['Ereignistitel'])

    def test_invalid_and_constant(self):
        with self.assertRaises(ValueError):cluster([[1,1]]*5,2)
        self.assertEqual(len(cluster([[1,0],[1,1],[1,10],[1,11]],2)[0]),4)
        for bad in ['nan','inf','abc']:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'bad.csv'
                p.write_text('Zeitstempel,Anlage,Temperatur_C,Druck_bar,Vibration_mm_s,Ereignis\n2026-01-01T00:00:00+00:00,A,'+bad+',1,2,\n')
                with self.assertRaises(ValueError):load_csv(p)

    def test_full_export_and_embedded_data(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(ROOT/'data/sensordaten_demo.csv',d)
            self.assertEqual(len(result),360)
            with (Path(d)/'prozessdaten_cluster.csv').open(encoding='utf-8-sig') as f:
                exported=list(csv.DictReader(f))
            self.assertEqual(len(exported),360)
            self.assertEqual(len({r['Messung_ID'] for r in exported}),360)
            html=(Path(d)/'dashboard.html').read_text()
            payload=html.split('<script id="daten" type="application/json">')[1].split('</script>')[0]
            self.assertEqual(json.loads(payload)['rows'],result)
            self.assertNotIn('__DATEN_JSON__',html)
            self.assertEqual(set(r['Cluster'] for r in result),{1,2,3})

if __name__=='__main__':unittest.main()
