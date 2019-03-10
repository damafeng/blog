from flask import Blueprint, flash, redirect, url_for
from ..utils import require_login, render_template_with_statue, permission_required
from app.forms.register_form import EditProfileAdminForm
from ..models.role import Role, Permission
from ..models.user import User
main = Blueprint('admin', __name__)


@main.route('/edit-profile/<int:u_id>', methods=['GET', 'POST'])
@require_login
@permission_required(Permission.ADMINISTER)
def edit_profile(u_id):
    user = User.find_by(id=u_id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        role = Role.find_by(id=form.role.data)
        update_form = {
            'email': form.email.data,
            'name': form.name.data,
            'about': form.about.data,
            'role_id': role.id,
            'permission': role.permission,
        }
        user.update(update_form)
        flash('资料更新完成')
        return redirect(url_for('main.user_profile', u_id=user.id))
    form.email.data = user.email
    form.name.data = user.name
    form.about.data = user.about
    form.role.data = user.role_id
    return render_template_with_statue('edit_profile.html', form=form)
