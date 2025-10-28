from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Transaction
from models_budget import Budget
from forms import BudgetForm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -------------------------------
# Blueprint setup
# -------------------------------
dash_bp = Blueprint("dashboard", __name__)

# Category icons
CATEGORY_ICONS = {
    "income": "💰",
    "food": "☕",
    "rent": "🏠",
    "entertainment": "🎉",
    "transport": "🚗",
    "shopping": "🛍️",
    "utilities": "💡",
    "other": "💵",
}


# -------------------------------
# MAIN DASHBOARD (with pagination)
# -------------------------------
@dash_bp.route("/")
@login_required
def dashboard():
    """Main dashboard route showing summaries, charts, budgets, and paginated recent transactions."""
    # ---- Pagination setup ----
    page = request.args.get("page", 1, type=int)
    per_page = 5  # show 5 recent transactions per page

    txns_query = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc())
    pagination = txns_query.paginate(page=page, per_page=per_page, error_out=False)
    txns = txns_query.all()
    recent_txns = pagination.items

    # ---- If no transactions yet ----
    if not txns:
        return render_template(
            "dashboard.html",
            total_income=0,
            total_spent=0,
            balance=0,
            pie_chart=None,
            line_chart=None,
            recent_txns=[],
            pagination=None,
            category_icons=CATEGORY_ICONS,
            budgets=[],
        )

    # ---- Convert transactions to DataFrame ----
    df = pd.DataFrame(
        [
            {
                "type": t.type,
                "category": t.category or "Other",
                "amount": t.amount,
                "date": t.date,
            }
            for t in txns
        ]
    )

    # Sort by date
    df = df.sort_values("date")

    # ---- Summary stats ----
    total_income = df[df["type"] == "income"]["amount"].sum()
    total_spent = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_spent

    # ------------------------------
    # Pie chart: Spending by category
    # ------------------------------
    expense_df = df[df["type"] == "expense"]
    if not expense_df.empty:
        cat_totals = expense_df.groupby("category")["amount"].sum().reset_index()
        cat_totals["hover_label"] = cat_totals.apply(
            lambda x: f"{x['category']} – ${x['amount']:.2f}", axis=1
        )

        pie_fig = px.pie(
            cat_totals,
            names="category",
            values="amount",
            title="Spending by Category",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        pie_fig.update_traces(
            textinfo="percent",
            hovertemplate="%{customdata}<extra></extra>",
            customdata=cat_totals["hover_label"],
        )
        pie_chart = pie_fig.to_html(full_html=False)
    else:
        pie_chart = None

    # ------------------------------
    # Line chart: Balance over time
    # ------------------------------
    df["signed_amount"] = df.apply(
        lambda row: row["amount"] if row["type"] == "income" else -row["amount"],
        axis=1,
    )

    daily_df = (
        df.groupby("date", as_index=False)["signed_amount"]
        .sum()
        .sort_values("date")
    )
    daily_df["balance"] = daily_df["signed_amount"].cumsum()

    line_fig = go.Figure()
    line_fig.add_trace(
        go.Scatter(
            x=daily_df["date"],
            y=daily_df["balance"],
            mode="lines+markers",
            name="Balance",
            line=dict(color="#007bff"),
            marker=dict(size=6),
        )
    )
    line_fig.update_layout(
        title="Balance Over Time",
        xaxis_title="Date",
        yaxis_title="Balance ($)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    line_chart = line_fig.to_html(full_html=False)

    # ------------------------------
    # Monthly budgets
    # ------------------------------
    budgets = []
    monthly_spent = expense_df.groupby("category")["amount"].sum().to_dict()

    user_budgets = {
        b.category.lower(): b.limit for b in Budget.query.filter_by(user_id=current_user.id).all()
    }

    default_limits = {
        "food": 300,
        "rent": 1000,
        "entertainment": 200,
        "transport": 150,
        "shopping": 250,
        "utilities": 100,
        "other": 200,
    }

    combined_limits = default_limits.copy()
    combined_limits.update(user_budgets)

    for category, spent in monthly_spent.items():
        limit = combined_limits.get(category.lower(), 200)
        percent = round((spent / limit) * 100, 1) if limit > 0 else 0
        percent = min(100, percent)

        budgets.append(
            {
                "category": category,
                "icon": CATEGORY_ICONS.get(category.lower(), "💵"),
                "spent": spent,
                "limit": limit,
                "percent": percent,
                "color": (
                    "bg-success"
                    if percent < 70
                    else "bg-warning"
                    if percent < 90
                    else "bg-danger"
                ),
            }
        )

    # ------------------------------
    # Render dashboard
    # ------------------------------
    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_spent=total_spent,
        balance=balance,
        pie_chart=pie_chart,
        line_chart=line_chart,
        recent_txns=recent_txns,
        pagination=pagination,
        category_icons=CATEGORY_ICONS,
        budgets=budgets,
    )


# -------------------------------
# EDIT BUDGET PAGE
# -------------------------------
@dash_bp.route("/budget/edit", methods=["GET", "POST"])
@login_required
def edit_budget():
    """Allows the user to create or update their monthly budget limits."""
    form = BudgetForm()

    if form.validate_on_submit():
        category = form.category.data.lower()
        limit = form.limit.data

        budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()
        if budget:
            budget.limit = limit
        else:
            budget = Budget(user_id=current_user.id, category=category, limit=limit)
            db.session.add(budget)
        db.session.commit()

        flash(f"Budget for {category.title()} set to ${limit:.2f}.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("edit_budget.html", form=form)
