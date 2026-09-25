-- How does logon-type mix change between the two days?
SELECT dataset_day,logon_type_description,COUNT(*) logons,ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY dataset_day),2) share_pct FROM auth_enriched GROUP BY 1,2 ORDER BY 1,logons DESC;
