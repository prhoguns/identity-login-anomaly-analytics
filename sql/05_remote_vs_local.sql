-- What share of logons is remote in the mirrored fields?
SELECT remote_logon,COUNT(*) logons,SUM(failure::INT) failures,ROUND(100.0*AVG(failure::INT),3) failure_pct FROM auth_enriched GROUP BY 1 ORDER BY 1;
