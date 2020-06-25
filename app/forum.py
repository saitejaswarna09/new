from flask import redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models import Group, Post, Thread, User, Quiz
from app.profile import set_class_code
from app.group import validate_group_link, add_user
from datetime import datetime



def validate_post_link(groupID, threadID, postID):
    # Check validity of link access first
    group = validate_group_link(groupID)
    if group is None:
        return 
    thread = Thread.query.filter_by(id=threadID,groupID=groupID).first_or_404()
    post = Post.query.filter_by(id=postID,threadID=threadID).first_or_404()
    if current_user.id != post.userID and current_user.urole != 'educator':
        return 
    return post

def save_post(content, threadID):
    post = Post(user=current_user, threadID=threadID, 
                timestamp=datetime.now(), content=content)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')

def remove_post(post):
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')

def add_thread(user, group, title, content):
    thread = Thread(group=group,timestamp=datetime.now(), title=title)
    db.session.add(thread)
    db.session.flush()

    save_post(content, thread.id)
    
    db.session.add(post)
    db.session.commit()

def remove_thread(thread):
    for p in Post.query.filter_by(threadID=thread.id).all():
        db.session.delete(p)
    db.session.delete(thread)
    db.session.commit()

def get_post_users(posts):
    '''Return user names as userID, name pairs in a dictionary'''
    users = {}
    for post in posts:
        if post.userID in users: continue
        user = User.query.filter_by(id=post.userID).first()
        users[post.userID] = ' '.join((user.firstName,user.lastName))
    return users

###########################
# To move to Unit Testing #
def add_test_forum():
    clear_test_forum()
    user = User.query.first()
    if user is None: return
    group = create_group(user, "first")
    add_user(group, user)
    create_thread(user, group, "first thread", "first post")

def clear_test_forum():
    g = Group.query.all()
    t = Thread.query.all()
    p = Post.query.all()
    q = Quiz.query.all()
    g.extend(t)
    g.extend(p)
    g.extend(q)
    for i in g:
        db.session.delete(i)
    db.session.commit()

add_test_forum()

