from pathlib import Path
import duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / 'data/analytics.duckdb'), read_only=True)
out = ROOT / 'results'
charts = ROOT / 'charts'
out.mkdir(exist_ok=True)
charts.mkdir(exist_ok=True)

def markdown(df):
    cols = [str(c) for c in df.columns]
    rows = [['' if v is None else str(round(v, 4) if isinstance(v, float) else v) for v in row]
            for row in df.itertuples(index=False, name=None)]
    return '| ' + ' | '.join(cols) + ' |\n| ' + ' | '.join(['---']*len(cols)) + ' |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)

for file in sorted((ROOT / 'sql').glob('*.sql')):
    sql = file.read_text()
    title = sql.splitlines()[0].removeprefix('-- ').strip()
    df = con.execute(sql).df()
    df.to_csv(out / f'{file.stem}.csv', index=False)
    (out / f'{file.stem}.md').write_text(f'# {title}\n\n{markdown(df.head(30))}')
    print(file.name, len(df), 'rows')

daily=con.execute((ROOT/'sql/01_daily_logons.sql').read_text()).df()
fig,ax=plt.subplots(figsize=(8,4.5))
ax.bar(daily['dataset_day'].astype(str),daily['failures'],color='#b45309')
ax.set(title='Failed human-account logons by dataset day',xlabel='Dataset day',ylabel='Failures')
fig.tight_layout();fig.savefig(charts/'daily_failures.png',dpi=160);plt.close(fig)

hourly=con.execute((ROOT/'sql/02_hourly_failures.sql').read_text()).df()
fig,ax=plt.subplots(figsize=(9,4.5))
for day,group in hourly.groupby('dataset_day'):
 ax.plot(group['hour_of_day'],group['failures'],marker='o',label=f'Day {day}')
ax.set(title='Failed logons by hour',xlabel='Dataset hour',ylabel='Failures')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(charts/'hourly_failures.png',dpi=160);plt.close(fig)
