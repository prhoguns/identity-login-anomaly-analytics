-- Which logon types account for human-account activity?
SELECT logon_type_description,COUNT(*) logons,SUM(failure::INT) failures,ROUND(100.0*AVG(failure::INT),3) failure_pct FROM auth_enriched GROUP BY 1 ORDER BY logons DESC;
