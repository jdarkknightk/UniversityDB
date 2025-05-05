USE university_db;
CREATE TABLE Administrator (
    AdminID INT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(50) NOT NULL
);

CREATE TABLE Student (
    StudID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    CGPA DECIMAL(3,2) CHECK (CGPA >= 0 AND CGPA <= 10)
);


CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Credits INT CHECK (Credits > 0)
);


CREATE TABLE Enrollment (
    EnrollID INT PRIMARY KEY,
    StudID INT,
    CourseID INT,
    FOREIGN KEY (StudID) REFERENCES Student(StudID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);


CREATE TABLE Attendance (
    AttndID INT PRIMARY KEY,
    StudID INT,
    CourseID INT,
    FOREIGN KEY (StudID) REFERENCES Student(StudID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);


CREATE TABLE Exam (
    ExamID INT PRIMARY KEY,
    CourseID INT,
    ExamDate DATE,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);


CREATE TABLE Faculty (
    FacultyID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Salary DECIMAL(10,2) CHECK (Salary > 0)
);


CREATE TABLE Department (
    DeptID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Contact VARCHAR(15),
    HOD VARCHAR(100)
);
INSERT INTO Administrator (AdminID, Username, Password) VALUES
(1, 'admin1', 'pass123'),
(2, 'admin2', 'securePass'),
(3, 'admin3', 'admin321'),
(4, 'admin4', 'rootPass'),
(5, 'admin5', 'myAdminPass');

INSERT INTO Student (StudID, Name, CGPA) VALUES
(101, 'Alice Johnson', 8.5),
(102, 'Bob Smith', 7.2),
(103, 'Charlie Brown', 9.1),
(104, 'David Wilson', 6.8),
(105, 'Emily Davis', 7.9);

INSERT INTO Course (CourseID, Name, Credits) VALUES
(201, 'Data Structures', 4),
(202, 'Database Management', 3),
(203, 'Machine Learning', 4),
(204, 'Operating Systems', 3),
(205, 'Web Development', 2);

INSERT INTO Enrollment (EnrollID, StudID, CourseID) VALUES
(301, 101, 201),
(302, 102, 202),
(303, 103, 203),
(304, 104, 204),
(305, 105, 205);

INSERT INTO Attendance (AttndID, StudID, CourseID) VALUES
(401, 101, 201),
(402, 102, 202),
(403, 103, 203),
(404, 104, 204),
(405, 105, 205);

INSERT INTO Exam (ExamID, CourseID, ExamDate) VALUES
(501, 201, '2025-05-10'),
(502, 202, '2025-05-12'),
(503, 203, '2025-05-15'),
(504, 204, '2025-05-18'),
(505, 205, '2025-05-20');

INSERT INTO Faculty (FacultyID, Name, Salary) VALUES
(601, 'Dr. Sharma', 90000.00),
(602, 'Dr. Gupta', 85000.00),
(603, 'Dr. Verma', 87000.00),
(604, 'Dr. Iyer', 88000.00),
(605, 'Dr. Mishra', 89000.00);

INSERT INTO Department (DeptID, Name, Contact, HOD) VALUES
(706, 'Computer Science', '1234567890', 'Dr. Sharma'),
(707, 'Mechanical Engineering', '9876543210', 'Dr. Singh'),
(708, 'Electrical Engineering', '5678901234', 'Dr. Patel'),
(709, 'Civil Engineering', '3456789012', 'Dr. Kumar'),
(710, 'Biotechnology', '6789012345', 'Dr. Reddy');

DELIMITER //

CREATE PROCEDURE ShowAllTables()
BEGIN
    SELECT * FROM Administrator;
    SELECT * FROM Student;
    SELECT * FROM Course;
    SELECT * FROM Department;
    SELECT * FROM Enrollment;
    SELECT * FROM Attendance;
END //

DELIMITER ;

CALL ShowAllTables();


