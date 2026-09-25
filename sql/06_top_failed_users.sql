-- Which anonymized users have the most failures?
SELECT user_name,COUNT(*) logons,SUM(failure::INT) failures,COUNT(DISTINCT src) sources,COUNT(DISTINCT destination) destinations FROM auth_enriched GROUP BY 1 HAVING failures>=20 ORDER BY failures DESC LIMIT 30;
