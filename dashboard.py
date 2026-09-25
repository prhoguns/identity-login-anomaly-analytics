from pathlib import Path
import duckdb
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='Identity and login anomaly analytics',layout='wide')
st.title('Identity and login anomaly analytics')
st.caption('LANL Unified Host and Network Dataset · anonymized User-prefixed account logon events · first two days')
db=ROOT/'data/analytics.duckdb'
if not db.exists():
    st.error('Run scripts/download.py and scripts/build_db.py first.');st.stop()
con=duckdb.connect(str(db),read_only=True)
days=st.sidebar.multiselect('Dataset days',[1,2],default=[1,2])
if not days:
    st.warning('Select at least one dataset day.');st.stop()
where='dataset_day IN ('+','.join(str(int(d)) for d in days)+')'
count,fail,users=con.execute(f'''SELECT COUNT(*),SUM(failure::INT),COUNT(DISTINCT user_name)
 FROM auth_enriched WHERE {where}''').fetchone()
a,b,c=st.columns(3)
a.metric('Logon events',f'{count:,}');b.metric('Failures',f'{fail:,}')
c.metric('Anonymized users',f'{users:,}')
hourly=con.execute(f'''SELECT dataset_day,hour_of_day,COUNT(*) logons,
 SUM(failure::INT) failures FROM auth_enriched WHERE {where}
 GROUP BY 1,2 ORDER BY 1,2''').df()
hourly['day']=hourly['dataset_day'].map(lambda d:f'Day {d}')
left,right=st.columns(2)
left.plotly_chart(px.line(hourly,x='hour_of_day',y='failures',color='day',markers=True,
 title='Failed logons by hour'),use_container_width=True)
right.plotly_chart(px.bar(hourly,x='hour_of_day',y='logons',color='day',barmode='group',
 title='Logon volume by hour'),use_container_width=True)
types=con.execute(f'''SELECT logon_type_description,COUNT(*) logons,
 100.0*AVG(failure::INT) failure_pct FROM auth_enriched WHERE {where}
 GROUP BY 1 ORDER BY logons DESC LIMIT 8''').df()
st.plotly_chart(px.bar(types,x='logon_type_description',y='failure_pct',hover_data=['logons'],
 title='Failure rate by logon type'),use_container_width=True)
st.subheader('Investigation queues')
tab1,tab2=st.tabs(['Failure bursts','New day-2 user–host pairs'])
with tab1:
    st.dataframe(con.execute((ROOT/'sql/08_user_failure_bursts.sql').read_text()).df(),
     use_container_width=True,hide_index=True)
with tab2:
    st.dataframe(con.execute((ROOT/'sql/10_new_user_host_pairs.sql').read_text()).df(),
     use_container_width=True,hide_index=True)
st.caption('Times are relative seconds and day indices, not calendar dates. New means unseen in day 1 only. The mirror fills missing source/destination fields with LogHost; rankings are investigation leads, not confirmed attacks.')
con.close()
