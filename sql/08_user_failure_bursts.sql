-- Which user-quarter-hour windows have repeated failures?
SELECT dataset_day,quarter_hour,user_name,COUNT(*) failures,COUNT(DISTINCT src) sources,COUNT(DISTINCT destination) destinations FROM auth_enriched WHERE failure GROUP BY 1,2,3 HAVING COUNT(*)>=10 ORDER BY failures DESC LIMIT 30;
