-- When are failed logons concentrated by dataset hour?
SELECT dataset_day,hour_of_day,COUNT(*) logons,SUM(failure::INT) failures,ROUND(100.0*AVG(failure::INT),3) failure_pct FROM auth_enriched GROUP BY 1,2 ORDER BY 1,2;
