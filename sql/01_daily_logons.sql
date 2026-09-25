-- How do logon volume and failure rate change from day 1 to day 2?
SELECT dataset_day,COUNT(*) logons,SUM(failure::INT) failures,ROUND(100.0*AVG(failure::INT),3) failure_pct FROM auth_enriched GROUP BY 1 ORDER BY 1;
