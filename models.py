from datetime import datetime
from app import db
import bcrypt

# Association table for friends (many-to-many)
friends = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(500), default='https://api.dicebear.com/7.x/avataaars/svg?seed=default')
    status = db.Column(db.String(20), default='offline')  # online, offline, away, busy
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    friends = db.relationship(
        'User', 
        secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        backref=db.backref('friend_of', lazy='dynamic'),
        lazy='dynamic'
    )
    
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    
    sent_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.sender_id', backref='sender', lazy='dynamic')
    received_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.receiver_id', backref='receiver', lazy='dynamic')
    
    def set_password(self, password):
        # Use 12 rounds for strong security (2^12 = 4096 iterations)
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.to_dict(),
            'receiver': self.receiver.to_dict(),
            'created_at': self.created_at.isoformat()
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=True)
    is_direct_message = db.Column(db.Boolean, default=False)
    edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'sender': self.sender.to_dict(),
            'recipient': self.recipient.to_dict() if self.recipient else None,
            'channel_id': self.channel_id,
            'is_direct_message': self.is_direct_message,
            'edited': self.edited,
            'edited_at': self.edited_at.isoformat() if self.edited_at else None,
            'created_at': self.created_at.isoformat()
        }

# Association table for channel members
channel_members = db.Table('channel_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'), primary_key=True)
)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    channel_type = db.Column(db.String(20), default='text')  # text, voice
    is_public = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_channels')
    members = db.relationship('User', secondary=channel_members, backref=db.backref('channels', lazy='dynamic'))
    messages = db.relationship('Message', backref='channel', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'channel_type': self.channel_type,
            'is_public': self.is_public,
            'creator': self.creator.to_dict(),
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat()
        }
