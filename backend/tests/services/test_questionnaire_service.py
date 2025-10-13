import unittest
from unittest.mock import patch
from backend.services.questionnaire_service import (
    get_questionnaires,
    get_questionnaire,
    create_questionnaire,
    delete_questionnaire,
    update_questionnaire
)

class TestQuestionnaireService(unittest.TestCase):

    @patch('backend.services.questionnaire_service.DataAccess')
    def test_get_questionnaires(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = [
            {'id': 1, 'title': 'Survey A', 'created_at': '2025-10-01'}
        ]

        result = get_questionnaires()
        mock_instance.query.assert_called_once_with(
            "SELECT id, title, created_at FROM Questionnaire ORDER BY created_at DESC;"
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Survey A')



    @patch('backend.services.questionnaire_service.DataAccess')
    def test_get_questionnaire(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.query.return_value = [
            {'id': 1, 'title': 'Survey A', 'created_at': '2025-10-01'}
        ]

        mock_instance.callproc.return_value = [{"created_at": '2025-10-01',
                "id": 1,
                "qn.id": 1,
                "question": "How are you?",
                "questionnaire_id": 1,
                "title": "Survey A"}]


        result = get_questionnaire(1)

        mock_instance.callproc.assert_called_once_with("GETQuestionnaire", (1,))
        self.assertEqual(result['questionnaire'][0]['title'], 'Survey A')
        self.assertEqual(result['questions'][0]['question'], 'How are you?')

    @patch('backend.services.questionnaire_service.add_question')
    @patch('backend.services.questionnaire_service.get_questionnaire')
    @patch('backend.services.questionnaire_service.DataAccess')
    def test_create_questionnaire(self, mock_data_access, mock_get_questionnaire, mock_add_question):
        mock_instance = mock_data_access.return_value
        mock_instance.getlastrowis_for_callproc.return_value = 1
        mock_get_questionnaire.return_value = {'id': 1, 'title': 'Survey A', 'questions': []}
        mock_add_question.return_value = [{'id': 1, 'question': 'Q1','questionnaire_id': 1},
                                          {'id': 2, 'question': 'Q2', 'questionnaire_id': 1}]

        data = {
            'title': 'Survey A',
            'questions_list': ["Q1", "Q2"]
        }

        result = create_questionnaire(data)

        mock_instance.callproc.assert_called_once_with("AddQuestionnaire", ('Survey A',))
        self.assertEqual(result['title'], 'Survey A')
        self.assertEqual(mock_add_question.call_count, 2)

    @patch('backend.services.questionnaire_service.DataAccess')
    def test_delete_questionnaire(self, mock_data_access):
        mock_instance = mock_data_access.return_value
        mock_instance.execute.return_value = True

        result = delete_questionnaire(1)
        mock_instance.execute.assert_called_once_with("DELETE FROM Questionnaire WHERE id = %s;", 1)
        self.assertTrue(result)

    @patch('backend.services.questionnaire_service.update_question')
    @patch('backend.services.questionnaire_service.get_questionnaire')
    @patch('backend.services.questionnaire_service.DataAccess')
    def test_update_questionnaire(self, mock_data_access, mock_get_questionnaire, mock_update_question):
        mock_instance = mock_data_access.return_value
        mock_instance.execute.return_value = 1
        mock_get_questionnaire.return_value = {'questionnaire': [{'id': 1, 'title': 'Updated Survey', "created_at": '2025-10-01'}],
                                               'questions': [{"created_at": '2025-10-01',
                                                              "id": 2,
                                                              "qn.id": 1,
                                                              "question": "Updated Q1",
                                                              "questionnaire_id": 1,
                                                              "title": "Updated Survey"}]}

        mock_update_question.return_value = {'id': 2, "questionnaire_id": 1, 'question': 'Updated Q1'}

        data = {
            'title': 'Updated Survey',
            'to_update_questions': [{'id': 2, 'question': 'Updated Q1', "questionnaire_id": 1}]
        }

        result = update_questionnaire(1,data)
        mock_instance.callproc.assert_called_once_with("UpdateQuestionnaire", (1, 'Updated Survey'))
        mock_update_question.assert_called_once_with(2, {'id': 2, 'question': 'Updated Q1', "questionnaire_id": 1})
        self.assertEqual(result['questionnaire'][0]['title'], 'Updated Survey')
