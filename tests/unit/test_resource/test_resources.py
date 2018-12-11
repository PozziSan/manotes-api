import json
from tests import base
from app import exceptions
from app.resource import resources


class AccountResourceGetTest(base.TestCase):

    # TODO: Implement
    def test_should_return_not_allowed(self):
        # note_resource = resources.NoteResource
        # response = note_resource.get()
        # self.assertEqual()
        self.assertTrue(True)


class NoteResourceGetTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_status_code_401_if_not_auth(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_not_authorized_not_authenticated(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_call_me_to_get_a_note(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertTrue(note_resource.me.get_a_note.called)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_note(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response, {'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_not_mine_if_not_mine_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[0], {'result': 'not-mine', 'error': 'Resource Not Mine', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_status_code_405_if_not_mine_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[1], 405)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_not_found_if_not_found_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('Could not find a note with id 1'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[0], {'result': 'not-found', 'error': 'Resource Not Found', 'id': 1})


    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_status_code_404_if_not_found_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('Could not find a note with id 1'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[1], 404)

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_call_query_if_not_note_id(self, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_resource = resources.NoteResource()
        note_resource.query = self.mock.MagicMock()
        note_resource.query.return_value = [
            {
                'id': 1,
                'name': 'This is a note',
                'content': 'And I need to write a mock content',
                'color': '#FFFFFF'
            },
            {
                'id': 2,
                'name': 'This is another note',
                'content': 'And I need to write another mock content',
                'color': '#FFFFFF'
            },
        ]
        note_resource.get()
        self.assertTrue(note_resource.query.called)


class NoteResourcePostTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_not_authorized_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_status_code_401_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_call_me_to_create_a_note(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.create_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        note_resource.post()
        self.assertTrue(note_resource.me.create_a_note.called)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_created_note(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.create_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.post()
        self.assertEqual(response, payload_mock)


class NoteResourcePutTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_not_authorized_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_status_code_401_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_call_me_to_update_a_note(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock()
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.update_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        note_resource.put(1)
        self.assertTrue(note_resource.me.update_a_note.called)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_updated_note(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock()
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.update_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.put(1)
        self.assertEqual(response, payload_mock)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_not_found_if_not_found_raised(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('foo'))
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.update_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.put(1)
        self.assertEqual(response[0], {'result': 'not-found', 'error': 'Resource Not Found', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_status_code_404_if_not_found_raised(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('foo'))
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = payload_mock
        logged_user_mock.update_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.put(1)
        self.assertEqual(response[1], 404)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_not_mine_if_not_mine_raised(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_resource = resources.NoteResource()
        response = note_resource.put(1)
        self.assertEqual(response[0], {'result': 'not-mine', 'error': 'Resource Not Mine', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.payload')
    def test_should_return_status_code_405_if_not_mine_raised(self, payload_mock, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.update_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        payload_mock = {
            'id': 1,
            'name': 'This is a note',
            'content': 'And I need to write a mock content',
            'color': '#FFFFFF'
        }
        note_resource = resources.NoteResource()
        response = note_resource.put(1)
        self.assertEqual(response[1], 405)


class NoteResourceDeleteTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_status_code_401_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_should_return_not_authorized_if_authentication_fail(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_call_me_to_delete_a_note(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock()
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertTrue(note_resource.me.delete_a_note.called)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_ok(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock()
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertEqual(response, {'result': 'OK'})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_not_found_if_not_found_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertEqual(response[0], {'result': 'not-found', 'error': 'Resource Not Found', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_status_code_404_if_not_found_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock(side_effect=exceptions.NotFound('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertEqual(response[1], 404)

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_not_mine_if_not_mine_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertTrue(note_resource.me.delete_a_note.called)
        self.assertEqual(response[0], {'result': 'not-mine', 'error': 'Resource Not Mine', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_should_return_status_code_405_if_not_mine_raised(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        logged_user_mock.delete_a_note = self.mock.MagicMock(side_effect=exceptions.NotMine('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.delete(1)
        self.assertTrue(note_resource.me.delete_a_note.called)
        self.assertEqual(response[1], 405)
