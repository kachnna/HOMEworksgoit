SELECT round(avg(grades),2) AS Average, s.name AS Name
FROM grades AS a 
JOIN students AS s ON a.student_id = s.id
GROUP BY a.student_id
ORDER BY Average DESC
LIMIT 5;