import os
from pathlib import Path
import duckdb

ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/'data/raw'
files=[raw/f'wls_day-{day}_2v.parquet' for day in ('01','02')]
if not all(f.exists() for f in files):
    raise SystemExit('Run python scripts/download.py first.')
db=ROOT/'data/analytics.duckdb'
con=duckdb.connect(str(db))
con.execute('SET threads=4')
con.execute('''CREATE OR REPLACE TABLE auth_events AS
 SELECT epoch_time,CAST(FLOOR(epoch_time/86400)+1 AS INTEGER) dataset_day,
 CAST(FLOOR((epoch_time%86400)/3600) AS INTEGER) hour_of_day,
 CAST(FLOOR(epoch_time/900) AS BIGINT) quarter_hour,
 event_id,user_name,src,destination,log_host,logon_type,
 logon_type_description,authentication_package,status,failure_reason
 FROM read_parquet(?)
 WHERE event_id IN (4624,4625) AND user_name LIKE 'User%' ''',
 [[str(f) for f in files]])
con.execute('''CREATE OR REPLACE VIEW auth_enriched AS SELECT *,
 event_id=4624 success, event_id=4625 failure,
 src<>destination remote_logon
 FROM auth_events''')
count,fail=con.execute('SELECT COUNT(*),SUM(failure::INT) FROM auth_enriched').fetchone()
min_rows=int(os.getenv('MIN_ROWS','1000000'))  # CI lowers this for the synthetic fixture
assert count>min_rows and 0<fail<count,(count,fail)
print(f'{count:,} User-prefixed account logon events; {fail:,} failed; database: {db}')
con.close()
