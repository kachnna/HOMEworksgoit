SELECT round(avg(grades),2) AS Average, s.name AS Subject 
FROM grades AS a
    JOIN subjects AS s ON a.subject_id = s.id
WHERE subject_id IN
(SELECT id FROM subjects WHERE lecturer_id = 1)
GROUP BY subject_id
ORDER BY Average DESC;