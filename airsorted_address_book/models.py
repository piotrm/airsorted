from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields

db = SQLAlchemy()
ma = Marshmallow()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), nullable = False)
    last_name = db.Column(db.String(80), nullable = False)
    company = db.Column(db.String(140))
    emails = db.relationship('Email',
        backref='contact', lazy='dynamic', cascade='save-update,delete')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Email(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(80), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)

class EmailSchema(ma.ModelSchema):
    class Meta:
        model = Email

class ContactSchema(ma.ModelSchema):
    class Meta:
        model = Contact
    emails = ma.Nested(EmailSchema, many=True)
