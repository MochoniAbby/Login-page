DROP TABLE IF EXISTS student_new;

/*CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    pass_word TEXT NOT NULL
);*/

CREATE TABLE student_new (
    username TEXT PRIMARY KEY, 
    pass_word VARCHAR(255),
    email TEXT NOT NULL, 
    otp_code TEXT
);

ALTER TABLE student_new RENAME TO student;