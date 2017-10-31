import unittest
import os
import json
from airsorted_address_book import create_app, db
from airsorted_address_book.models import Contact, Email

class ContactsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='test')
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

    ''' Helper method '''
    def create_test_contact(self, first_name, last_name):
        contact = Contact(
            first_name=first_name,
            last_name=last_name
        )
        contact.emails = [
            Email(address=('{}@{}.pl').format(first_name, last_name))
        ]
        contact.save()
        return contact

    def test_show(self):
        contact = self.create_test_contact('Aaa', 'Bbb')
        response = self.client().get(
            '/api/v1/contacts/{}'.format(contact.id))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['first_name'], 'Aaa')
        self.assertEqual(response_data['last_name'], 'Bbb')

    def test_index(self):
        contact1 = self.create_test_contact('Issaac', 'Newton')
        contact2 = self.create_test_contact('Albert', 'Einstein')
        response = self.client().get('/api/v1/contacts')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        response_first_names = list(map(lambda x: x['first_name'], response_data))
        self.assertIn('Albert', response_first_names)
        self.assertIn('Issaac', response_first_names)

    def test_index_with_parameter(self):
        contact1 = self.create_test_contact('Issaac', 'Newton')
        contact2 = self.create_test_contact('Albert', 'Einstein')
        response = self.client().get('/api/v1/contacts?email=Albert@Einstein.pl')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        response_first_names = list(map(lambda x: x['first_name'], response_data))
        self.assertIn('Albert', response_first_names)
        self.assertNotIn('Issaac', response_first_names)

    def test_create(self):
        contact_params = {
            'first_name': 'Olaf',
            'last_name': 'Snowman',
            'emails': [
                'olaf@abcde.com',
                'osnowman@abcde.com'
            ]
        }
        response = self.client().post(
            '/api/v1/contacts',
            data=json.dumps(contact_params),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['first_name'], 'Olaf')
        self.assertEqual(response_data['last_name'], 'Snowman')
        email_addresses = list(map(lambda x: x['address'], response_data['emails']))
        self.assertIn('olaf@abcde.com', email_addresses)

    def test_update(self):
        contact = self.create_test_contact('Alfred', 'Nobel')
        response = self.client().put(
            '/api/v1/contacts/{}'.format(contact.id),
            data=json.dumps({'first_name': 'Sheldon'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['first_name'], 'Sheldon')
        self.assertEqual(response_data['last_name'], 'Nobel')

    def test_delete(self):
        contact = self.create_test_contact('Nikola', 'Tesla')
        response = self.client().delete(
            '/api/v1/contacts/{}'.format(contact.id))
        self.assertEqual(response.status_code, 200)
        response_empty = self.client().get(
            '/api/v1/contacts/{}'.format(contact.id))
        self.assertEqual(response_empty.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()