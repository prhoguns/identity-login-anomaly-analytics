-- Which high-volume accounts have elevated failure rates?
SELECT user_name,COUNT(*) logons,SUM(failure::INT) failures,ROUND(100.0*AVG(failure::INT),2) failure_pct FROM auth_enriched GROUP BY 1 HAVING COUNT(*)>=100 AND SUM(failure::INT)>=10 ORDER BY failure_pct DESC,failures DESC LIMIT 30;
