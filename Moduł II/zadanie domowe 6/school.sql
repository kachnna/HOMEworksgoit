-- Students tabel
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id integer  PRIMARY KEY AUTOINCREMENT,
    name text,
    group_id integer,
    FOREIGN KEY (group_id) REFERENCES groups (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
-- Groups tabel
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text
);

-- Lecturers tabel
DROP TABLE IF EXISTS lecturers;
CREATE TABLE lecturers (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text
);

-- Subjects tabel
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id integer PRIMARY KEY,
    name text,
    lecturer_id integer,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Grades tabel
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
    id integer PRIMARY KEY,
    grades integer,
    student_id integer,
    subject_id integer,
    created_at DATE,
    FOREIGN KEY (student_id) REFERENCES students (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);