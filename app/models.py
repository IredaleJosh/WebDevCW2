from app import db

# M:M Relationship - Users and Groups

user_group = db.Table(
    "user_group",
    db.Column("user_id", db.Integer, db.ForeignKey('UserInfo.id'), primary_key=True), 
    db.Column("group_id", db.Integer, db.ForeignKey('Groups.id'), primary_key=True),
)

# M:M - Users and Games

user_games = db.Table(
    "user_games",
    db.Column("user_id", db.Integer, db.ForeignKey('UserInfo.id'), primary_key=True), 
    db.Column("game_id", db.Integer, db.ForeignKey('Games.id'), primary_key=True),
)

# M:M - User and Messages - Check for User liking/disliking message

user_msg = db.Table(
    "user_msg",
    db.Column("user_id", db.Integer, db.ForeignKey('UserInfo.id'), primary_key=True), 
    db.Column("message_id", db.Integer, db.ForeignKey('Messages.id'), primary_key=True),
)

class UserInfo(db.Model):
    __tablename__ = "UserInfo"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25)) # May change via more testing
    username = db.Column(db.String(15))
    password = db.Column(db.String(15)) # Min length 12, Max length 16
    # Store list of groups linked to specific user
    group = db.relationship(
        "Groups", secondary=user_group, back_populates="users"
    )
    # Store list of games user has reviewed
    games = db.relationship(
        "Games", secondary=user_games, back_populates="users"
    )
    # Store messages user has interacted with
    action = db.relationship(
        "Messages", secondary=user_msg, back_populates="users"
    )

# M:M - Users and Games

class Games(db.Model):
    __tablename__ = "Games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # Store Users Who "WishList" the Game
    users = db.relationship(
        "UserInfo", secondary=user_games, back_populates="games"
    )
    # Store Reviews linked to specific game
    review = db.relationship('Review', backref='games', lazy='dynamic')


class Groups(db.Model):
    __tablename__ = "Groups"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20))
    desc = db.Column(db.String(50))
    # Store users linked to specific group
    users = db.relationship(
        "UserInfo", secondary=user_group, back_populates="group"
    )
    # Store Messages linked to a specific group
    messages = db.relationship('Messages', backref='groups', lazy='dynamic')

# 1:M Relationship - Groups and Messages

class Messages(db.Model):
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    # Each User does either once
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('Groups.id'))
    # Store UserId when they like a message
    users = db.relationship(
        "UserInfo", secondary=user_msg, back_populates="action"
    )

class Review(db.Model):
    __tablename__ = "Review"
    id = db.Column(db.Integer, primary_key=True)
    # Store User when typing review
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(15))
    name = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    text = db.Column(db.String(100))
    game_id = db.Column(db.Integer, db.ForeignKey('Games.id'))

    def __repr__(self):
        return f"<Review(user_id={self.user_id}, name={self.name}, rating={self.rating}, text={self.text}, game_id={self.game_id})>"