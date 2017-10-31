import json
from flask_script import Manager
from airsorted_address_book import create_app
from airsorted_address_book.models import Contact, Email

app = create_app()
manager = Manager(app)

@manager.command
def seed():
    with open('seeds.json') as data_file:    
        data = json.load(data_file)
        data_file.close()

    for contact_data in data:
        emails_data = contact_data.pop('emails')
        contact = Contact(**contact_data)
        if emails_data:
            for email_data in emails_data:
                email = Email(**email_data)
                contact.emails.append(email)
        contact.save()


if __name__ == "__main__":
    manager.run()