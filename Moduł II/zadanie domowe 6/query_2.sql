SELECT round(avg(grades),2) AS Average, s.name AS Name
FROM grades AS a 
    JOIN students AS s on a.student_id = s.id
WHERE a.subject_id = 1
GROUP BY a.student_id
ORDER BY Average DESC
LIMIT 1;