from pathlib import Path
from urllib.request import urlretrieve

ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/'data/raw'
raw.mkdir(parents=True,exist_ok=True)
for day in ('01','02'):
    name=f'wls_day-{day}_2v.parquet'
    target=raw/name
    if not target.exists():
        urlretrieve(f'https://datasets.rocketgraph.com/LANL/xgt/{name}',target)
    print(f'{name}: {target.stat().st_size:,} bytes')
