-- employee_by_quarter.sql

SELECT 
    d.department,
    j.job,
    COUNT(e.employee_id) FILTER (WHERE EXTRACT(MONTH FROM e.datetime) < 3) AS Q1,
    COUNT(e.employee_id) FILTER (WHERE EXTRACT(MONTH FROM e.datetime) BETWEEN 3 AND 6) AS Q2,
    COUNT(e.employee_id) FILTER (WHERE EXTRACT(MONTH FROM e.datetime) BETWEEN 6 AND 9) AS Q3,
    COUNT(e.employee_id) FILTER (WHERE EXTRACT(MONTH FROM e.datetime) > 9) AS Q4
FROM employee e
JOIN department d ON e.department_id = d.department_id
JOIN job j ON e.job_id = j.job_id 
WHERE EXTRACT(YEAR FROM e.datetime) = 2021
GROUP BY d.department, j.job
ORDER BY d.department, j.job;