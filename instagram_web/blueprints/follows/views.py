from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models.follower_following import FollowerFollowing
from flask_login import login_user, login_required, current_user
from models.user import User

follows_blueprint = Blueprint('follows',
                              __name__,
                              template_folder='templates')

#  --------- CREATE NEW INSTANCE OF A FOLLOWER-FOLLOWING RELATIONSHIP -----------

# ---- CALL BOTH OF THESE METHODS ON USER PROFILE(a.k.a) users/show.html


@follows_blueprint.route('/<idol_id>', methods=['POST'])
def create(idol_id):

    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash(f'No user found with this id', 'error')
        return redirect(url_for('users.index'))

    new_follow = FollowerFollowing(fan_id=current_user.id, idol_id=idol.id)

    if not new_follow.save():
        flash(f"Unable to save this follow", "error")
        return redirect(url_for('users.show', usefdrname=idol.name))

    flash('Follow request sent, please wait for approval')
    return redirect(url_for('users.show', username=idol.name))


@follows_blueprint.route('/<idol_id>', methods=['POST'])
def delete(idol_id):

    follow = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == idol_id) and (
        FollowerFollowing.fan_id == current_user.id))

    flash(f"You have unfollowed {follow.idol.name}")
    return redirect(url_for('users_show', username=follow.idol.name))

# http://127.0.0.1:5000/follows/34/review
@follows_blueprint.route('/<user_id>/review')
def review(user_id):
    user = User.get_or_none(User.id == user_id)

# PEEWEEE AND SQL HAVE DIFFERNT COMMNDS. & and and, lookup later

    requests = FollowerFollowing.select().where(
        FollowerFollowing.idol_id == current_user.id)

    # requests = FollowerFollowing.select().where(
    #     (FollowerFollowing.idol_id == current_user.id) & (FollowerFollowing.approved == False))

    if current_user.id == user.id:
        return render_template("follows/requestreview.html", user=user, requests=requests)
    else:
        return abort(401)


@follows_blueprint.route('<fan_id>/review/approve', methods=["POST"])
def approve(fan_id):

    # ------GET THE INSTANCE AND SET APPROVED TO TRUE ---------------
    approved_follow = FollowerFollowing.get_or_none(
        (FollowerFollowing.idol_id == current_user.id) & (FollowerFollowing.fan_id == fan_id))

    if not approved_follow:
        flash(f"No relationship found", "error")
        return redirect(url_for('follows.review', user_id=current_user.id))

    if approved_follow.approved == False:
        approved_follow.approved = True
    else:
        approved_follow.approved = False

    if not approved_follow.save():
        flash(f"Could not approve follower", "error")
        return redirect(url_for('follows.review', user_id=current_user.id))

    else:
        flash(f"Sucessfully approved follower", "sucess")
        return redirect(url_for('follows.review', user_id=current_user.id))

# -------------- ISSUES TO KEEP IN MIND ----------
# 1) previous code on users/views.py may have been set to deny a user to see another users profile, as in give a error page. change it to where can see profile, but have to follow to see images

# 2)while logged in as JonBonPony, typing in users/DogBerg will go to Dogbergs page that shows A) his images and B) his upload user images form.
# A) keep user images, but make it so that they are hidden until followed
# B) the upload user images wont work when not logged in as DogBerg, any uploaded pic will go to JonBonPony's page instead. move the upload to edit details instead?
# the users page is users/show.html

# 3) HOW TO DEAL WITH APPROVING FOLLOW REQUESTS?
