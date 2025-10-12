import unittest
from unittest.mock import patch

from backend.services.question_service import (get_questions,
                                               get_question,
                                               add_question,
                                               delete_question,
                                               update_question)


class TestQuestionService(unittest.TestCase):
    # Mock DataAccess path
    DATA_ACCESS_PATH = 'backend.services.question_service.DataAccess'

    # Test get_questions
    @patch(DATA_ACCESS_PATH)
    def test_get_questions_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = [{'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?'},
                                             {'id': 2, 'questionnaire_id': 101, 'question': 'How old are you?'}]

        result = get_questions(101)
        assert result == [{'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?'}
                          , {'id': 2, 'questionnaire_id': 101, 'question': 'How old are you?'}]
        mock_instance.query.assert_called_once_with(
            "SELECT id, questionnaire_id, question FROM Question WHERE questionnaire_id = %s", 101
        )

    # Test get_question
    @patch(DATA_ACCESS_PATH)
    def test_get_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = {'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?'}

        result = get_question(1)
        assert result == {'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?'}

    # Test add_question
    @patch(DATA_ACCESS_PATH)
    def test_add_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = {'id': 4, 'questionnaire_id': 101, 'question': "What is your favorite color?"}

        result = add_question(101, "What is your favorite color?")

        mock_instance.callproc.assert_called_once_with("AddQuestion", (101, "What is your favorite color?"))
        assert result == {'id': 4, 'questionnaire_id': 101, 'question': "What is your favorite color?"}

    # Test delete_question
    @patch(DATA_ACCESS_PATH)
    def test_delete_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value

        result = delete_question(1)
        assert result is True
        mock_instance.execute.assert_called_once_with("DELETE FROM Question WHERE id = (%s);", 1)

    # Test update_question
    @patch('backend.services.question_service.get_question')
    @patch(DATA_ACCESS_PATH)
    def test_update_question_success(self, mock_data_access, mock_get_question):

        mock_instance = mock_data_access.return_value
        mock_get_question.return_value = {'id': 1, 'questionnaire_id': 101, 'question': 'Updated question'}

        result = update_question(101, 1, {'question': 'Updated question'})


        mock_instance.callproc.assert_called_once_with("UpdateQuestion", (101, 1, "Updated question"))
        assert result == {'id': 1, 'questionnaire_id': 101, 'question': 'Updated question'}
