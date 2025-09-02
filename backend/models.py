from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_role'), default='user', nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    symptom_logs = db.relationship('SymptomLog', backref='user', lazy=True)
    assessments = db.relationship('Assessment', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class SymptomLog(db.Model):
    __tablename__ = 'symptom_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms_text = db.Column(db.Text, nullable=False)
    conditions_json = db.Column(db.JSON)
    risk_level = db.Column(db.Enum('low', 'medium', 'high', name='risk_level'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SymptomLog {self.id}>'

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    recommended_action = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Assessment {self.id}>'

class Provider(db.Model):
    __tablename__ = 'providers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum('clinic', 'hospital', 'pharmacy', 'counseling', name='provider_type'), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Provider {self.name}>'

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel = db.Column(db.Enum('mindwell', 'support', name='message_channel'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20))
    alert_flag = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}>'

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan = db.Column(db.Enum('free', 'premium', name='subscription_plan'), default='free', nullable=False)
    status = db.Column(db.Enum('active', 'inactive', name='subscription_status'), default='active', nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Subscription {self.id}>'

class UsageLog(db.Model):
    __tablename__ = 'usage_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feature = db.Column(db.Enum('symptom_check', 'mindwell_chat', 'provider_lookup', name='feature_type'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='usage_logs')
    
    def __repr__(self):
        return f'<UsageLog {self.user_id}-{self.feature}-{self.date}>'

class DoctorCallback(db.Model):
    __tablename__ = 'doctor_callbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    preferred_time = db.Column(db.String(50))
    reason = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'scheduled', 'completed', 'cancelled', name='callback_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='callback_requests')
    
    def __repr__(self):
        return f'<DoctorCallback {self.id}>'

# Database initialization and helpers
def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
def create_tables():
    """Create all database tables"""
    db.create_all()

def seed_admin_user():
    """Create hardcoded admin user for MVP"""
    from werkzeug.security import generate_password_hash
    
    admin_user = User.query.filter_by(email='admin@healthlinkai.com').first()
    if not admin_user:
        admin_user = User(
            name='Admin User',
            email='admin@healthlinkai.com',
            role='admin',
            password_hash=generate_password_hash('admin123')  # Change in production
        )
        db.session.add(admin_user)
        
        # Create default subscription for admin
        admin_subscription = Subscription(
            user_id=admin_user.id,
            plan='premium',
            status='active'
        )
        db.session.add(admin_subscription)
        
        db.session.commit()
        print("Admin user created: admin@healthlinkai.com / admin123")

def init_database():
    """Complete database initialization"""
    create_tables()
    seed_admin_user()
    print("Database initialized successfully")
