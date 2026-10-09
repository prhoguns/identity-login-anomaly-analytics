"""Write small synthetic wls_day-01/02 Parquet files to data/raw/ for CI.

Same columns and types as the LANL 2017 Windows logon release, including rows the build must
filter out (non-User accounts, other event IDs). One user has a burst of failures from a single
source that ends in a success, so the anomaly queries have something to rank. It checks that every
query runs; it says nothing about the real data.
"""
import random
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
LOGON = [(3, 'Network', 0.9), (2, 'Interactive', 0.03), (8, 'NetworkClearText', 0.02),
         (7, 'Unlock', 0.02), (9, 'NewCredentials', 0.02), (10, 'RemoteInteractive', 0.01)]
PACKAGES = ['Kerberos'] * 14 + ['NTLM', 'Negotiate']
REASONS = ['Unknown user name or bad password.', 'An Error occured during Logon.',
           'Account locked out.', 'Account currently disabled.']
USERS = [f'User{n:06d}' for n in random.Random(1).sample(range(1, 999_999), 300)]
HOSTS = [f'Comp{n:06d}' for n in random.Random(2).sample(range(1, 999_999), 80)] + ['ActiveDirectory']

random.seed(5)
RAW.mkdir(parents=True, exist_ok=True)
con = duckdb.connect()
for day in (1, 2):
    rows = []
    for _ in range(15_000):
        t = (day - 1) * 86_400 + int(random.triangular(0, 86_399, 50_000))
        ltype, ldesc, _ = random.choices(LOGON, weights=[w for *_, w in LOGON])[0]
        src = random.choice(HOSTS)
        dst = src if random.random() < 0.4 else random.choice(HOSTS)
        fail = random.random() < 0.015
        user = random.choice(USERS) if random.random() < 0.95 else random.choice(['ANONYMOUS LOGON', 'Comp000123$'])
        rows.append((t, 4625 if fail else random.choice([4624] * 9 + [4634]), user, src, dst, dst,
                     ltype, ldesc, random.choice(PACKAGES), None, random.choice(REASONS) if fail else None))
    burst_user, burst_src, burst_dst = USERS[0], HOSTS[0], HOSTS[1]
    start = (day - 1) * 86_400 + 33 * 900  # aligned to a quarter hour
    for i in range(200):  # repeated bad passwords from one source, then a success: a guessed password
        rows.append((start + i * 3, 4625, burst_user, burst_src, burst_dst, burst_dst, 3, 'Network',
                     'NTLM', None, REASONS[0]))
    rows.append((start + 700, 4624, burst_user, burst_src, burst_dst, burst_dst, 3, 'Network', 'NTLM', None, None))
    con.execute('''CREATE OR REPLACE TABLE t (epoch_time BIGINT, event_id BIGINT, user_name VARCHAR, src VARCHAR,
        destination VARCHAR, log_host VARCHAR, logon_type BIGINT, logon_type_description VARCHAR,
        authentication_package VARCHAR, status VARCHAR, failure_reason VARCHAR)''')
    con.executemany('INSERT INTO t VALUES (?,?,?,?,?,?,?,?,?,?,?)', rows)
    out = RAW / f'wls_day-{day:02d}_2v.parquet'
    con.execute(f"COPY t TO '{out}' (FORMAT parquet)")
print(f'fixture: 2 parquet files in {RAW}')
