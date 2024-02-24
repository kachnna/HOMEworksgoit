SELECT s.name AS Subject
FROM grades AS a
    JOIN subjects AS s ON a.subject_id = s.id
    JOIN students AS st ON a.student_id = st.id
WHERE  subject_id IN 
(SELECT id FROM subjects WHERE lecturer_id = 1)
AND student_id = 1
GROUP BY Subject
ORDER BY Subject ASC;