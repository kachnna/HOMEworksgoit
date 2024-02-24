SELECT s.name AS Subject
FROM grades AS a
    JOIN subjects AS s ON a.subject_id = s.id
WHERE student_id = 1
GROUP BY Subject
ORDER BY Subject ASC;