import unittest
from unittest.mock import patch

from backend.services.question_service import (get_questions,
                                               get_question,
                                               add_question,
                                               delete_question,
                                               update_question,
                                               add_option,
                                               get_options_by_question_id, replace_options)


class TestQuestionService(unittest.TestCase):
    # Mock DataAccess path
    DATA_ACCESS_PATH = 'backend.services.question_service.DataAccess'

    # Test get_questions
    @patch(DATA_ACCESS_PATH)
    def test_get_questions_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = [{'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?', 'type': 'text'},
                         {'id': 2, 'questionnaire_id': 101, 'question': 'How old are you?', 'type': 'text'}]

        result = get_questions(101)
        assert result == [{'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?', 'type': 'text'}
                          , {'id': 2, 'questionnaire_id': 101, 'question': 'How old are you?', 'type': 'text'}]
        mock_instance.query.assert_called_once_with(
            "SELECT id, questionnaire_id, question, type FROM Question WHERE questionnaire_id = %s", 101
        )

    # Test get_question
    @patch(DATA_ACCESS_PATH)
    def test_get_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = {'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?', 'type': 'text'}

        result = get_question(1)
        assert result == {'id': 1, 'questionnaire_id': 101, 'question': 'What is your name?', 'type': 'text', 'options': []}

    # Test add_question
    @patch(DATA_ACCESS_PATH)
    def test_add_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = {'id': 4, 'questionnaire_id': 101, 'question': "What is your favorite color?", 'type': 'text'}

        result = add_question(101, "What is your favorite color?")

        mock_instance.callproc.assert_called_once_with("AddQuestion", (101, "What is your favorite color?", 'text'))
        assert result == {'id': 4, 'questionnaire_id': 101, 'question': "What is your favorite color?", 'type': 'text', 'options': []}

    # Test delete_question
    @patch(DATA_ACCESS_PATH)
    def test_delete_question_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value

        result = delete_question(1)
        assert result is True
        mock_instance.execute.assert_called_once_with("DELETE FROM Question WHERE id = (%s);", 1)

    # Test update_question
    @patch("backend.services.question_service.replace_options")
    @patch('backend.services.question_service.get_question')
    @patch(DATA_ACCESS_PATH)
    def test_update_question_success(self, mock_data_access, mock_get_question, mock_replace_options):

        mock_instance = mock_data_access.return_value
        mock_get_question.return_value = {'id': 1, 'questionnaire_id': 101, 'question': 'Updated question', 'type': 'text', 'options': []}

        result = update_question(101, 1, {'question': 'Updated question'})

        mock_replace_options.return_value = None

        mock_instance.callproc.assert_called_once_with("UpdateQuestion", (101, 1, "Updated question", 'text'))
        assert result == {'id': 1, 'questionnaire_id': 101, 'question': 'Updated question', 'type': 'text', 'options': []}


    @patch(DATA_ACCESS_PATH)
    def test_add_option_success(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = None

        add_option(1, "Option1")
        mock_instance.callproc.assert_called_once_with("AddOption", (1, "Option1"))


    @patch(DATA_ACCESS_PATH)
    def test_get_options_by_id(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = [{"id":1, "question_id":1, "option_text":"Option 1"},
                                            {"id":2, "question_id":1, "option_text":"Option 2"}]

        get_options_by_question_id(1)
        mock_instance.query.assert_called_once_with("SELECT id, option_text FROM Options WHERE question_id = %s ORDER BY id ASC", 1)

    @patch('backend.services.question_service.add_option')
    @patch(DATA_ACCESS_PATH)
    def test_replace_options_success(self, mock_data_access, mock_add_option):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = None

        replace_options(1, ["Option1", "Option2"])

        mock_instance.callproc.assert_called_once_with("DeleteOptionsForQuestion", (1,))
        # Check if the mock_add_option is called 2 times
        # assert mock_add_option.query.call_count == 2