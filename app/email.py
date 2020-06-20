from flask import render_template, url_for, redirect, flash
from flask_mail import Message
from flask_login import login_user
from app import app, db, mail
from app.models import User
from app.token import generate_confirmation_token


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_conf_email(user, confirm_url):
    send_email('[Knewbie] Confirmation',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/activate.txt',
                                         name=user.firstName, confirm_url=confirm_url),
               html_body=render_template('email/activate.html',
                                         name=user.firstName, confirm_url=confirm_url))

def send_contact_email(form):
    send_email('[Knewbie] Contact',
               sender=app.config['ADMINS'][0],
               recipients=app.config['ADMINS'],
               text_body=render_template('email/contactmsg.txt', form=form),
               html_body=render_template('email/contactmsg.html', form=form)
    )

def send_reset_email(user):
    token = user.reset_token()
    #message = Message('[Knewbie] Password Reset Request', sender='resetpassword@knewbie.com', recipients=[user.email])
    send_email('Password Reset Request', 
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset.txt', name=user.firstName, token=token),
               html_body=render_template('email/reset.html', name=user.firstName, token=token)
    )

def send_deactivate_email(user):
    token = user.reset_token()
    #message = Message('[Knewbie] Deactivate Account Request', sender='deactivate@knewbie.com', recipients=[user.email])
    send_email('[Knewbie] Deactivate Account Request', 
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/deactivate.txt', name=user.firstName, token=token),
               html_body=render_template('email/deactivate.html', name=user.firstName, token=token)
    )

def get_confirm_url(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    return confirm_url

def register(form, role):
    user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, urole=role, confirmed=False)
    user.set_password(form.password.data)
    if role == 'student':
        user.set_knewbie_id()
    db.session.add(user)
    db.session.commit()
    confirm_url = get_confirm_url(user)
    send_conf_email(user, confirm_url)
        
    #login_user(user)

    flash('A confirmation email has been sent via email.', 'success')
    #flash('Congratulations, you are now a registered user!')
    return redirect(url_for('unconfirmed'))

def resend_conf(user):
    confirm_url = get_confirm_url(user)
    send_conf_email(user, confirm_url)
    flash('A new confirmation email has been sent.', 'success')


def add_user():
    if User.query.all(): return
    user = User(firstName='test',lastName='test',email='testflask202005@gmail.com', urole='student',confirmed=True)
    user.set_password('test')
    user.set_knewbie_id()
    db.session.add(user)
    db.session.commit()

add_user()