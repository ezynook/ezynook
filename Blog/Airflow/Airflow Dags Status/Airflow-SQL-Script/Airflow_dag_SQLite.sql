SELECT 
	MAX(a.dag_id) AS dag_id,
	MAX(a.is_paused) AS active,
	MAX(b.start_date) AS start_date,
	MAX(b.state) AS state
FROM
	dag a
LEFT JOIN
	dag_run b ON a.dag_id = b.dag_id
GROUP BY 
	b.dag_id