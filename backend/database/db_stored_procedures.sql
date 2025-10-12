
use skyfeedbackdb;


DROP PROCEDURE AddQuestion;
DROP PROCEDURE AddQuestionnaire;
DROP PROCEDURE AddFeedback;
DROP PROCEDURE AddUser;
DROP PROCEDURE UpdateQuestion;
DROP PROCEDURE UpdateQuestionnaire;
DROP PROCEDURE GETQuestionnaire;


-- ADD and UPDATE Questionnaire 
delimiter //
CREATE PROCEDURE AddQuestionnaire(IN title VARCHAR(100))
BEGIN
	INSERT INTO Questionnaire(title) values (title);
END //
     


delimiter //
CREATE PROCEDURE UpdateQuestionnaire(IN ques_id INT, IN ques_title VARCHAR(100))
BEGIN
	UPDATE Questionnaire
    SET title = ques_title
    WHERE id = ques_id;
END //
     


-- ADD and UPDATE Question
delimiter //

CREATE PROCEDURE AddQuestion(IN questionnaire_id INT, IN question VARCHAR(200))
BEGIN
	INSERT INTO Question(questionnaire_id, question) values (questionnaire_id, question);
END //
     


delimiter //
CREATE PROCEDURE UpdateQuestion(IN QuestionnaireID INT, IN QID INT, IN ques_title VARCHAR(100))
BEGIN
	UPDATE Question
    SET question = ques_title, questionnaire_id = QuestionnaireID
    WHERE id = QID;
END //
     


-- ADD Feedback
delimiter //

CREATE PROCEDURE AddFeedback(IN question_id INT, IN user_id INT, IN feedback TEXT)
BEGIN
	INSERT INTO Feedback(question_id, user_id, feedback) values (question_id, user_id, feedback);
END //
     


delimiter //

-- ADD User

CREATE PROCEDURE AddUser(IN username VARCHAR(100), IN name VARCHAR(100))
BEGIN
	INSERT INTO User(username, name) values (username, name);
END //
     



delimiter //

-- 

CREATE PROCEDURE GETQuestionnaire(IN question_id INT)
BEGIN
	SELECT *
	FROM Question q
	INNER JOIN 
	Questionnaire qn
	on q.questionnaire_id = qn.id
	WHERE qn.id = question_id;
END //
     










