SELECT round(avg(grades), 2) AS Average, g.name AS Name
FROM grades AS a 
    JOIN students AS s ON a.student_id = s.id
    JOIN groups AS g ON s.group_id = g.id
GROUP BY s.group_id
ORDER BY Average DESC;