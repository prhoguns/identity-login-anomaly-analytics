-- Which source devices have the most failed logons?
SELECT src,COUNT(*) logons,SUM(failure::INT) failures,COUNT(DISTINCT user_name) users FROM auth_enriched GROUP BY 1 HAVING failures>=20 ORDER BY failures DESC LIMIT 30;
