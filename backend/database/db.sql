CREATE database skyfeedbackdb;

use skyfeedbackdb;

DROP TABLE Feedback;
DROP TABLE User;
DROP TABLE Question;
DROP TABLE Questionnaire;

CREATE TABLE Questionnaire (
  id INT AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE Question (
  id INT AUTO_INCREMENT,
  questionnaire_id INT NOT NULL,
  question VARCHAR(200) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (questionnaire_id) REFERENCES Questionnaire (id) ON DELETE CASCADE
);

CREATE TABLE User (
  id INT AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Feedback (
  id INT AUTO_INCREMENT,
  question_id INT NOT NULL,
  user_id INT NOT NULL,
  feedback TEXT NOT NULL, 
  PRIMARY KEY (id),
  FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);


