-- Which day-2 accounts reach the most distinct destination devices?
SELECT user_name,COUNT(DISTINCT destination) destinations,COUNT(DISTINCT src) sources,COUNT(*) logons FROM auth_enriched WHERE dataset_day=2 AND success AND remote_logon GROUP BY 1 HAVING destinations>=10 ORDER BY destinations DESC,logons DESC LIMIT 30;
