from airsorted_address_book import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), nullable = False)
    last_name = db.Column(db.String(80), nullable = False)
    company = db.Column(db.String(140))
    emails = db.relationship('Email',
        backref=db.backref('contact', lazy='joined'))

class Email(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(80), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationshiop('Contact',
        backref=db.backref('emails', lazy='joined')) 
