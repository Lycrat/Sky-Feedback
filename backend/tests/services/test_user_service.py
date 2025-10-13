import unittest
from unittest.mock import patch
from services.user_service import (get_users, get_user, add_user)

class TestUserService(unittest.TestCase):

    DATA_ACCESS_PATH = 'services.user_service.DataAccess'

    @patch(DATA_ACCESS_PATH)
    def test_get_users(self, data_access_mock):
        mock_data_access_instance = data_access_mock.return_value
        mock_data_access_instance.query.return_value = [
            {'id': 1, 'username': 'user1', 'name': 'User One'},
            {'id': 2, 'username': 'user2', 'name': 'User Two'}
            ]

        users = get_users()
        mock_data_access_instance.query.assert_called_once()
        assert users == [{'id': 1, 'username': 'user1', 'name': 'User One'},
                         {'id': 2, 'username': 'user2', 'name': 'User Two'}]

    @patch(DATA_ACCESS_PATH)
    def test_get_user(self, data_access_mock):
        mock_data_access_instance = data_access_mock.return_value
        mock_data_access_instance.query.return_value = {'id': 1, 'username': 'user1', 'name': 'User One'}

        users = get_user(1)
        mock_data_access_instance.query.assert_called_once()
        assert users == {'id': 1, 'username': 'user1', 'name': 'User One'}

    @patch("services.user_service.get_user")
    @patch(DATA_ACCESS_PATH)
    def test_get_users_success(self, mock_data_access, mock_get_user):
        mock_data_access_instance = mock_data_access.return_value
        mock_get_user.return_value = {'id': 1, 'username': 'user1', 'name': 'User One'}

        user = add_user('user1', 'User One')
        mock_data_access_instance.callproc.assert_called_once_with("AddUser", ('user1', 'User One',))
        assert user == {'id': 1, 'username': 'user1', 'name': 'User One'}