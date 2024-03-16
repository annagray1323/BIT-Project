from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session 
from flask_login import login_required, current_user
from .models import Note, User 
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def map():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("map.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/info')
@login_required
def info():
    return render_template('info.html', user=current_user)

@views.route('/barcode.html')
def barcode():
    return render_template('barcode.html', user=current_user)

@views.route('/journey.html')
def journey():
    return render_template('journey.html', user=current_user)

@views.route('/begin_journey.html')
def begin_journey():
    return render_template('begin_journey.html', user=current_user)

@views.route('/resume_journey.html')
def resume_journey():
    return render_template('resume_journey.html', user=current_user)

@views.route('/end_journey')
def end_journey():
    return render_template('end_journey.html', user=current_user)

@views.route('/wallet', methods=['GET', 'POST']) 
@login_required 
def wallet():
    selected_amount = None  
    if request.method == 'POST':
        selected_amount = float(request.form.get('amount')) 
# Update wallet balance for the current user 
        current_user.wallet_balance += selected_amount 
        # Add transaction to the WalletTransaction model 
       # transaction = WalletTransaction(user_id=current_user.id, amount=selected_amount) 
       #db.session.add(transaction) 
    # db.session.commit() 
        flash('Your wallet has been updated!', category='success') 
        return redirect(url_for('views.wallet'))  
    return render_template('wallet.html', user=current_user, selected_amount=selected_amount)

    return render_template('wallet.html', user=current_user)

@views.route('/history.html')
def history():
    return render_template('history.html', user=current_user)

@views.route('/pricing.html')
def pricing():
    return render_template('pricing.html', user=current_user)

@views.route('/day_pass.html', methods=['GET', 'POST'])
def day_pass():
    if request.method == 'POST':
        flash("Your day pass is now active, let's get moving!", category='success')
        return redirect(url_for('views.day_pass'))
    return render_template('day_pass.html', user=current_user)

@views.route('/three_day_pass.html', methods=['GET', 'POST'])
def three_day_pass():
    if request.method == 'POST':
        flash("Your three day pass is now active, let's get moving!", category='success')
        return redirect(url_for('views.three_day_pass'))
    return render_template('three_day_pass.html', user=current_user)

@views.route('/monthly_pass.html', methods=['GET', 'POST'])
def monthly_pass():
    if request.method == 'POST':
        flash("Your monthly day pass is now active, let's get moving!", category='success')
        return redirect(url_for('views.monthly_pass'))
    return render_template('monthly_pass.html', user=current_user)

@views.route('/co2.html')
def co2():
    return render_template('co2.html', user=current_user)






