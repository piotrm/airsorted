from .models import Contact, ContactSchema, Email
from flask import abort, request, json, jsonify

def show(id):
    schema = ContactSchema()
    contact = Contact.query.get(id)
    if not contact:
        abort(404)

    data, _ = schema.dump(contact)
    return jsonify(data), 200

def index():
    schema = ContactSchema(many=True)
    contacts = Contact.query.all()

    data, _ = schema.dump(contacts)
    return jsonify(data), 200

def create():
    schema = ContactSchema()
    if (not request.get_json() or 'first_name' not in request.get_json() or
        'last_name' not in request.get_json() or 'emails' not in request.get_json()):
        abort(400)

    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    company = request.get_json().get('company')
    emails = request.get_json().get('emails')
    contact = Contact(
        first_name=first_name,
        last_name=last_name,
        company=company
    )

    for e in emails:
        email = Email(address=e)
        contact.emails.append(email)
    contact.save()

    data, _ = schema.dump(contact)
    return jsonify(data), 201

def update(id):
    schema = ContactSchema()

    contact = Contact.query.get(id)
    if not contact:
        abort(400)

    contact.first_name = request.get_json().get('first_name', contact.first_name)
    contact.last_name = request.get_json().get('last_name', contact.last_name)
    contact.company = request.get_json().get('company', contact.company)
    emails = request.get_json().get('emails')

    if emails:
        emails_to_delete = contact.emails.filter(~(Email.address.in_(emails)))
        for email_to_delete in emails_to_delete:
            email_to_delete.delete()

        current_email_addresses = list(map(lambda x: x.address, contact.emails))
        emails_to_add = list(set(emails) - set(current_email_addresses))

        for email in emails_to_add:
            email = Email(address=email)
            contact.emails.append(email)
    contact.save()

    data, _ = schema.dump(contact)
    return jsonify(data), 200

def delete(id):
    contact = Contact.query.get(id)
    if not contact:
        abort(400)

    contact.delete()
    return jsonify( { 'message': 'Successfully deleted Contact #{}'.format(id) } ), 200
