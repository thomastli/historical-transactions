SELECT request_id, customer_id , request_datetime , request_amount,
CASE
	WHEN customer_request_count > 1 THEN 1
	ELSE 0
END AS first_request_flag
FROM requests
LEFT JOIN (SELECT request_id as id, COUNT(customer_id) OVER (PARTITION BY customer_id ORDER BY request_id) AS customer_request_count FROM requests ORDER BY id)
ON request_id = id
