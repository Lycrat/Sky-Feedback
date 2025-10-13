
use skyfeedbackdb;


-- DROP PROCEDURE AddQuestion;
-- DROP PROCEDURE AddQuestionnaire;
-- DROP PROCEDURE AddFeedback;
-- DROP PROCEDURE AddUser;
-- DROP PROCEDURE UpdateQuestion;
-- DROP PROCEDURE UpdateQuestionnaire;
-- DROP PROCEDURE GETQuestionnaire;


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

delimiter //

CREATE PROCEDURE AddQuestion(IN questionnaire_id INT, IN question VARCHAR(200), IN q_type VARCHAR(50))
BEGIN
	INSERT INTO Question(questionnaire_id, question, type) values (questionnaire_id, question, q_type);
END //

delimiter //
CREATE PROCEDURE UpdateQuestion(IN QuestionnaireID INT, IN QID INT, IN ques_title VARCHAR(200), IN q_type VARCHAR(50))
BEGIN
	UPDATE Question
	SET question = ques_title, questionnaire_id = QuestionnaireID, type = q_type
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
	INSERT INTO Users(username, name) values (username, name);
END //

delimiter //

-- Question options helpers
delimiter //
CREATE PROCEDURE AddOption(IN qid INT, IN opt_text VARCHAR(200))
BEGIN
    INSERT INTO Options(question_id, option_text) VALUES (qid, opt_text);
END //

delimiter //
CREATE PROCEDURE DeleteOptionsForQuestion(IN qid INT)
BEGIN
    DELETE FROM Options WHERE question_id = qid;
END //

delimiter //
-- Get questionnaire with questions and types; join options if any
CREATE PROCEDURE GETQuestionnaire(IN question_id INT)
BEGIN
	SELECT qn.id as questionnaire_id,
           qn.title,
           qn.created_at,
           q.id as question_id,
           q.question,
           q.type,
           o.id as option_id,
           o.option_text
	FROM Questionnaire qn
	LEFT JOIN Question q ON q.questionnaire_id = qn.id
	LEFT JOIN Options o ON o.question_id = q.id
	WHERE qn.id = question_id
	ORDER BY q.id, o.id;
END //