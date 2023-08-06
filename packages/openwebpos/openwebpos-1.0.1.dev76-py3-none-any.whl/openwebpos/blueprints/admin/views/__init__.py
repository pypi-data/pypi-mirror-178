from os import getenv, environ, path

import dotenv
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from openwebpos.blueprints.billing.models import PaymentMethod
from openwebpos.blueprints.pos.models import (Order)
from openwebpos.blueprints.user.decorators import role_require, \
    permission_require
from openwebpos.blueprints.user.forms import UserProfileForm, AddUserForm
from openwebpos.blueprints.user.models import User, UserProfile, UserActivity
from .menu_views import bp as menu_bp
from .order_views import bp as order_bp
from .printer_views import bp as printer_bp
from ..forms import CompanyForm, CompanyBranchForm, TwilioForm
from ..models import Company, Branch

admin = Blueprint('admin', __name__, template_folder='../templates',
                  url_prefix='/admin')

admin.register_blueprint(printer_bp)
admin.register_blueprint(menu_bp)
admin.register_blueprint(order_bp)


@admin.before_request
@login_required
@role_require('Administrator')
@permission_require('view_admin')
def before_request():
    """
    Protects all the admin endpoints.
    """
    pass


@admin.route('/')
def index():
    """
    Admin dashboard.
    """
    _company = Company.query.first()
    return render_template('admin/index.html', title='Admin', company=_company)


@admin.route('/users', methods=['GET', 'POST'])
def users():
    """
    Displays all the users.
    """
    _users = User.query.all()
    form = AddUserForm()
    form.set_choices()
    if form.validate_on_submit():
        _user = User(username=form.username.data,
                     email=form.email.data,
                     role_id=form.role.data)
        _user.set_password(form.password.data)
        _user.save()
        flash('User added successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/users.html', title='Users', users=_users,
                           form=form)


@admin.get('/user/delete/<int:user_id>')
def delete_user(user_id):
    """
    Deletes the user.
    """
    # Check if more users exist
    if User.query.count() >= 1:
        user = User.query.get_or_404(user_id)
        # Check if the user is not the current user
        if user.id != current_user.id:
            # check if user has any orders
            if Order.query.filter_by(user_id=user.id).count() != 0:
                # Make the user inactive if the user has orders
                flash('User has orders. Cannot delete user.', 'danger')
                flash('Making user inactive instead.', 'info')
                user.make_inactive()
            else:
                # Delete user if not the last admin or staff.
                if not user.is_last_admin() or not user.is_last_staff():
                    user.delete()
                    flash('User deleted.', 'success')
                else:
                    flash('Cannot delete last admin or staff.', 'danger')
    return redirect(url_for('admin.users'))


@admin.get('/users/toggle/<int:user_id>/<string:field>')
def toggle_user(user_id, field):
    """
    Toggles the user's active status.
    """
    user = User.query.get_or_404(user_id)
    if field == 'active':
        if not user.query.count() == 1:
            user.toggle_active()
            flash('User active status toggled.', 'success')
    elif field == 'staff':
        if not user.is_last_staff():
            user.set_as_staff()
    return redirect(url_for('admin.users'))


@admin.route('/user/profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    """
    Displays the user's profile.
    """
    user = User.query.get(user_id)
    _user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    form = UserProfileForm(obj=_user_profile)
    if form.validate_on_submit():
        update_profile = UserProfile(user_id=user_id)
        form.populate_obj(update_profile)
        if _user_profile:
            update_profile.update()
        update_profile.save()
        return redirect(url_for('admin.users'))
    return render_template('admin/user_profile.html', title='User Profile',
                           user=user, form=form)


@admin.route('/user/activity/<int:user_id>')
def user_activity(user_id):
    """
    Displays the user's activity.
    """
    user = User.query.get(user_id)
    user_activities = UserActivity.query.filter_by(user_id=user_id).all()
    return render_template('admin/user_activity.html', title='User Activity',
                           user=user, user_activities=user_activities)


@admin.route('/menus')
def menus():
    """
    Displays the menu types, categories and items.
    """
    return render_template('admin/menus.html', title='Menus')


@admin.route('/orders')
def orders():
    """
    Displays all the orders.
    """
    _orders = Order.query.all()
    return render_template('admin/orders.html', title='Orders', orders=_orders)


@admin.route('/billing')
def billing():
    """
    Displays the billing page.
    """
    return render_template('admin/billing.html', title='Billing')


@admin.route('/billing/payment_methods')
def payment_methods():
    """
    Displays all the payment methods.
    """
    _payment_methods = PaymentMethod.query.all()
    return render_template('admin/payment_methods.html',
                           title='Payment Methods',
                           payment_methods=_payment_methods)


@admin.get('/billing/payment_method/toggle/<int:payment_method_id>')
def toggle_payment_method(payment_method_id):
    """
    Toggles the payment method. (Enables/Disables)

    Args:
        payment_method_id: The payment method id.

    Returns:
        The payment methods page.
    """
    _payment_method = PaymentMethod.query.get(payment_method_id)
    _payment_method.toggle()
    return redirect(url_for('admin.payment_methods'))


@admin.route('/company', methods=['GET', 'POST'])
def company():
    """
    Displays the company page.
    """
    company_form = CompanyForm(obj=Company.query.first())
    _company = Company.query.first()
    branches = Branch.query.all()
    if company_form.validate_on_submit():
        _company = Company.query.first()
        if not _company:
            _company = Company()
        company_form.populate_obj(_company)
        _company.name = company_form.name.data.title()
        _company.update()
        return redirect(url_for('admin.company'))
    return render_template('admin/company.html', title='Company',
                           company_form=company_form,
                           branches=branches, company=_company)


@admin.route('/company/toggle/twilio')
def toggle_twilio():
    """
    Toggles the twilio. (Enables/Disables)

    Returns:
        The company page.
    """
    _company = Company.query.first()
    _company.toggle_twilio()
    return redirect(url_for('admin.company'))


@admin.get('/company/branch/toggle/<int:branch_id>')
def toggle_branch(branch_id):
    """
    Toggles the branch. (Enables/Disables)

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    _branches = Branch.query.all()
    _branch = Branch.query.get(branch_id)
    if len(_branches) > 1:
        _branch.toggle()
        flash('Branch toggled successfully.', 'green')
    else:
        flash('You must have at least one active branch.', 'red')
    return redirect(url_for('admin.company'))


@admin.route('/company/branch/delete/<int:branch_id>')
def delete_branch(branch_id):
    """
    Deletes the branch.

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    _branch = Branch.query.get(branch_id)
    _company_branches = Company.query.filter_by(id=_branch.company_id).all()
    # Check if the branch is the only branch. if so, don't delete it.
    if len(_company_branches) > 1:
        # Delete the branch.
        flash('Branch deleted successfully.', 'green')
        _branch.delete()
    else:
        flash('You cannot delete the only branch.', 'red')
        # TODO: Add a message to the user that the branch was deleted.
    # If the branch is the only branch, don't delete it.
    # TODO: Add a message to the user that the branch can't be deleted.
    return redirect(url_for('admin.company'))


@admin.route('/company/branch/edit/<int:branch_id>', methods=['GET', 'POST'])
def edit_branch(branch_id):
    """
    Edits the branch.

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    _branch = Branch.query.get(branch_id)
    branch_form = CompanyBranchForm(obj=_branch)
    if branch_form.validate_on_submit():
        branch_form.populate_obj(_branch)
        _branch.update()
        return redirect(url_for('admin.company'))
    return render_template('admin/branch.html', title='Edit Branch',
                           branch_form=branch_form, branch=_branch)


@admin.get('/printers')
def printers():
    """
    Display the printers page.
    """
    return render_template('admin/printers.html', title='Printers')


@admin.route('/twilio', methods=['GET', 'POST'])
def twilio():
    """
    Displays the twilio page and handles the form.
    form is used to update the twilio credentials saved in the .env file.

    Returns:
        The twilio config page.(admin.twilio)
    """
    # Check if the .env file exists.
    if not path.exists('.env'):
        # If it doesn't exist, create it.
        with open('.env', 'w') as f:
            f.write('')
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    form = TwilioForm()
    form.account_sid.data = getenv('TWILIO_ACCOUNT_SID')
    form.auth_token.data = getenv('TWILIO_AUTH_TOKEN')
    form.phone_number.data = getenv('TWILIO_PHONE_NUMBER')
    if form.validate_on_submit():
        environ['TWILIO_ACCOUNT_SID'] = form.account_sid.data
        environ['TWILIO_AUTH_TOKEN'] = form.auth_token.data
        environ['TWILIO_PHONE_NUMBER'] = form.phone_number.data
        dotenv.set_key(dotenv_file, 'TWILIO_ACCOUNT_SID',
                       form.account_sid.data)
        dotenv.set_key(dotenv_file, 'TWILIO_AUTH_TOKEN',
                       form.auth_token.data)
        dotenv.set_key(dotenv_file, 'TWILIO_PHONE_NUMBER',
                       form.phone_number.data)
        return redirect(url_for('admin.twilio'))
    return render_template('admin/twilio.html', title='Twilio', form=form)
