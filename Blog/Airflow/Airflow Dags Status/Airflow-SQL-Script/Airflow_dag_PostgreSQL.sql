SELECT DISTINCT ON (a.dag_id)
        a.dag_id as dag_id, 
        a.start_date as start_date, 
        a.state as state
    FROM 
        dag_run a
    LEFT JOIN
        dag b ON a.dag_id = b.dag_id
    WHERE
        dag.is_paused = False
    ORDER BY 
        a.dag_id, a.start_date DESC