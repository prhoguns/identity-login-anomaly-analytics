-- Which day-2 accounts log in from the most distinct source devices?
SELECT user_name,COUNT(DISTINCT src) source_devices,COUNT(DISTINCT destination) destination_devices,COUNT(*) logons FROM auth_enriched WHERE dataset_day=2 AND success AND remote_logon GROUP BY 1 HAVING source_devices>=10 ORDER BY source_devices DESC,logons DESC LIMIT 30;
