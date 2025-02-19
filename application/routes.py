from application import app
from flask import render_template, redirect, url_for, flash
from application.models import Item, User
from application.forms import RegisterForm, LoginForm
from application import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user_to_create = User(
                email_address=form.email_address.data,
                blood_group=form.blood_group.data,
                city=form.city.data,
                gender=form.gender.data,
                contact_number=form.contact_number.data,
                dob=form.dob.data
            )
            user_to_create.set_password(form.password1.data)  # Assuming you have this method in your User model
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f"Account created successfully! You are now logged in as {user_to_create.email_address}", category='success')
            return redirect(url_for('home_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while creating your account: {str(e)}', category='danger')
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.email_address}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Email and password do not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



@app.route('/donate')
def donate_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page'))
    else:
        return redirect(url_for('register_page'))

@app.route('/toggle-donor-status')
@login_required
def toggle_donor_status():
    try:
        if current_user.is_active_donor:
            current_user.is_active_donor = False
            current_user.last_donation_date = None
            flash('You are no longer listed as an active donor.', 'info')
        else:
            # Check if it's been 3 months since last donation
            if current_user.last_donation_date:
                months_passed = (datetime.now().date() - current_user.last_donation_date).days / 30
                if months_passed < 3:
                    flash(f'You can donate blood after {90 - int(months_passed*30)} days.', 'danger')
                    return redirect(url_for('profile_page'))
            
            current_user.is_active_donor = True
            current_user.last_donation_date = datetime.now().date()
            flash('You are now listed as an active donor!', 'success')
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('profile_page'))

@app.route('/donors')
def donors_page():
    active_donors = User.query.filter_by(is_active_donor=True).all()
    return render_template('donors.html', donors=active_donors)

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')




