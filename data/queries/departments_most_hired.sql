SELECT 
    d.department_id, 
    d.department,
    count(e.employee_id) as hired
FROM employee e
JOIN department d ON e.department_id = d.department_id
WHERE EXTRACT(YEAR FROM e.datetime) = 2021
GROUP BY d.department_id, d.department
HAVING count(e.employee_id) > (
    SELECT count(e.employee_id) / count(distinct d.department_id) 
    FROM employee e
    JOIN department d ON e.department_id = d.department_id
    WHERE EXTRACT(YEAR FROM e.datetime) = 2021
)
ORDER BY hired DESC;