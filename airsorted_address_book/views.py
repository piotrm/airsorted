from .models import Contact, ContactSchema, Email
from .validators import EmailParamsValidator
from flask import abort, request, json, jsonify
from IPython import embed

def show(id):
    contact = Contact.query.get(id)
    if not contact:
        abort(404)

    data, _ = ContactSchema().dump(contact)
    return jsonify(data), 200

def index():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    if 'email' in request.args:
        contacts = Contact.query.join(Email). \
            filter_by(address=request.args.get('email'))
    else:
        contacts = Contact.query.paginate(page,per_page).items

    data, _ = ContactSchema(many=True).dump(contacts)
    return jsonify(data), 200

def create():
    emails = request.get_json().get('emails')

    if (not request.get_json() or
        (emails and not EmailParamsValidator.check(emails)) or
        ('first_name' not in request.get_json() and
        'last_name' not in request.get_json() and
        'company' not in request.get_json())):
        return abort(400)

    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    company = request.get_json().get('company')
    contact = Contact(
        first_name=first_name,
        last_name=last_name,
        company=company
    )

    for e in emails:
        email = Email(address=e)
        contact.emails.append(email)
    contact.save()

    data, _ = ContactSchema().dump(contact)
    return jsonify(data), 201

def update(id):
    contact = Contact.query.get(id)
    emails = request.get_json().get('emails')

    if (not contact or not request.get_json() or
        (emails and not EmailParamsValidator.check(emails))):
        abort(400)

    contact.first_name = request.get_json().get('first_name', contact.first_name)
    contact.last_name = request.get_json().get('last_name', contact.last_name)
    contact.company = request.get_json().get('company', contact.company)
    emails = request.get_json().get('emails')

    if emails:
        emails_to_delete = contactstact.emails.filter(~(Email.address.in_(emails)))
        for email_to_delete in emails_to_delete:
            email_to_delete.delete()

        current_email_addresses = list(map(lambda x: x.address, contact.emails))
        emails_to_add = list(set(emails) - set(current_email_addresses))

        for email in emails_to_add:
            email = Email(address=email)
            contact.emails.append(email)
    contact.save()

    data, _ = ContactSchema().dump(contact)
    return jsonify(data), 200

def delete(id):
    contact = Contact.query.get(id)
    if not contact:
        abort(400)

    contact.delete()
    return jsonify( { 'message': 'Successfully deleted Contact #{}'.format(id) } ), 200
