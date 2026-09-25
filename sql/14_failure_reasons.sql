-- Which reported reasons accompany failed logons?
SELECT COALESCE(NULLIF(failure_reason,''),'not supplied') failure_reason,COUNT(*) failures FROM auth_enriched WHERE failure GROUP BY 1 ORDER BY failures DESC LIMIT 20;
