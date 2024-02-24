SELECT a.grades AS grades, s.name AS Name
FROM grades AS a
    JOIN students AS s ON a.student_id = s.id
WHERE subject_id = 1 AND s.group_id = 1;