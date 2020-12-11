from app import db


class User(db.Model):
    """User Model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    score = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Score %r>' % self.score
