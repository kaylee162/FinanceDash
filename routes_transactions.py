from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Transaction
from forms import TransactionForm
from datetime import datetime

# Create the blueprint
txn_bp = Blueprint("transactions", __name__)

# -------------------------
# List all transactions
# -------------------------
@txn_bp.route("/transactions")
@login_required
def list_transactions():
    txns = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .order_by(Transaction.date.desc())
        .all()
    )
    return render_template("transactions.html", txns=txns)

# -------------------------
# Add a new transaction
# -------------------------
@txn_bp.route("/transactions/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_txn = Transaction(
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            date=form.date.data or datetime.utcnow(),
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_txn)
        db.session.commit()
        return redirect(url_for("transactions.list_transactions"))

    return render_template("add_transaction.html", form=form)

# -------------------------
# Delete a transaction
# -------------------------
@txn_bp.route("/transactions/<int:txn_id>/delete", methods=["POST"])
@login_required
def delete_transaction(txn_id):
    txn = Transaction.query.get_or_404(txn_id)
    if txn.user_id != current_user.id:
        return "Not allowed", 403
    db.session.delete(txn)
    db.session.commit()
    return redirect(url_for("transactions.list_transactions"))

@txn_bp.route("/transactions/<int:txn_id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(txn_id):
    txn = Transaction.query.filter_by(id=txn_id, user_id=current_user.id).first_or_404()
    form = TransactionForm(obj=txn)  # pre-fill with current values

    if form.validate_on_submit():
        txn.type = form.type.data
        txn.category = form.category.data
        txn.amount = form.amount.data
        txn.date = form.date.data
        txn.description = form.description.data

        db.session.commit()
        flash("Transaction updated successfully!", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("edit_transaction.html", form=form, txn=txn)
