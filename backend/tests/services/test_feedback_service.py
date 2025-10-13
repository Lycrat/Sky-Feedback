import unittest
from unittest.mock import patch

from backend.services.feedback_service import (get_feedbacks, get_feedbacks_by_user_id, add_feedback)


class TestFeedbackService(unittest.TestCase):

    DATA_ACCESS_PATH = "backend.services.feedback_service.DataAccess"

    # Test get_feedbacks
    @patch(DATA_ACCESS_PATH)
    def test_get_feedbacks(self, data_access_mock):

        mock_instance = data_access_mock.return_value
        mock_instance.query.return_value = [
            {'id':1, 'question_id':1, 'user_id':1, 'feedback':"The app looks good"},
            {'id':2, 'question_id':2, 'user_id':1, 'feedback':"The button is not accessible"},
            {'id':3, 'question_id':1, 'user_id':2, 'feedback':"The app's look can be improved"},
            {'id':4, 'question_id':2, 'user_id':2, 'feedback':"The button is not accessible on small screens"},
        ]

        get_feedbacks()
        mock_instance.query.assert_called_with("SELECT id, question_id, user_id, feedback FROM Feedback")

    # Test get_feedbacks_by_user_id
    @patch(DATA_ACCESS_PATH)
    def test_get_feedbacks_by_user_id(self, data_access_mock):

        mock_instance = data_access_mock.return_value
        mock_instance.query.return_value = [
            {'id':1, 'question_id':1, 'user_id':1, 'feedback':"The app looks good"},
            {'id':2, 'question_id':2, 'user_id':1, 'feedback':"The button is not accessible"},
        ]

        get_feedbacks_by_user_id(1)
        mock_instance.query.assert_called_with("SELECT id, question_id, feedback FROM Feedback WHERE user_id=%s", 1)

    # Test get_add_feedback
    @patch('backend.services.feedback_service.get_feedback')
    @patch(DATA_ACCESS_PATH)
    def test_add_feedback(self, data_access_mock, mock_get_feedback):
        mock_instance = data_access_mock.return_value
        mock_get_feedback.return_value = {
            'id':3, 'question_id':1, 'user_id':3, 'feedback':"The app looks great"
        }

        result = add_feedback(1,3,"The app looks great")
        assert result == {
            'id':3, 'question_id':1, 'user_id':3, 'feedback':"The app looks great"
        }
        mock_instance.callproc.assert_called_once_with("AddFeedback",(3,1,"The app looks great"))
