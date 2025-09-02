from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps
from werkzeug.security import check_password_hash
import base64

# Import AI modules
from ai.symptom_checker import SymptomChecker
from ai.mindwell_bot import mindwell_reply
from ai.recommend import nearest_providers

# Import models
from models import db, User, SymptomLog, Assessment, Provider, Message, Subscription, UsageLog, DoctorCallback, init_db

# Import usage tracking
from utils.usage_tracker import require_usage_limit, get_usage_summary, check_usage_limit, get_user_subscription

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def config_db():
    """Configure database from DATABASE_URL environment variable"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Default to local MySQL for development
        database_url = 'mysql+pymysql://root:password@localhost/healthlinkai'
    
    return database_url

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = config_db()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Enable CORS
CORS(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if request.method == 'POST':
        # Check usage limits for free users
        user_id = 1  # Mock user ID for now
        usage_check = require_usage_limit(user_id, 'symptom_check')
        
        if 'error' in usage_check:
            return render_template('symptom_checker.html', 
                                 usage_error=usage_check, 
                                 show_upgrade_modal=True)
        
        # Get form data
        symptom_text = request.form.get('symptom_text', '')
        selected_symptoms = request.form.getlist('selected_symptoms')
        
        # Analyze symptoms using AI
        checker = SymptomChecker()
        analysis = checker.analyze_symptoms(symptom_text, selected_symptoms)
        
        # Save to database (mock user for now)
        symptom_report = SymptomReport(
            user_id=1,  # Mock user ID
            symptoms_text=symptom_text,
            selected_symptoms=','.join(selected_symptoms),
            risk_level=analysis['risk_band'],
            conditions=','.join([c['name'] for c in analysis['conditions']]),
            advice=analysis['advice'],
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(symptom_report)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving symptom report: {e}")
        
        return render_template('symptom_checker.html', analysis=analysis, show_results=True)
    
    return render_template('symptom_checker.html')

@app.route('/mindwell')
def mindwell():
    return render_template('mindwell.html')

@app.route('/api/mindwell', methods=['POST'])
def api_mindwell():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Check usage limits for free users
    user_id = 1  # Mock user ID for now
    usage_check = require_usage_limit(user_id, 'mindwell_chat')
    
    if 'error' in usage_check:
        return jsonify({
            'error': 'Usage limit exceeded',
            'message': usage_check['message'],
            'upgrade_required': True,
            'current_plan': usage_check['current_plan']
        }), 429
    
    # Get AI response
    response = mindwell_reply(user_message)
    
    # Save session to database (mock user for now)
    session_record = MentalHealthSession(
        user_id=1,  # Mock user ID
        user_message=user_message,
        bot_response=response['response'],
        sentiment_score=response.get('sentiment_score', 0),
        detected_intent=response.get('intent', 'general'),
        alert_flag=response.get('alert_flag', False),
        created_at=datetime.utcnow()
    )
    
    try:
        db.session.add(session_record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving mental health session: {e}")
    
    return jsonify(response)

@app.route('/providers')
def providers():
    # Get query parameters
    provider_type = request.args.get('type')
    city = request.args.get('city')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    limit = request.args.get('limit', 10, type=int)
    
    providers_data = []
    
    # If coordinates provided, get nearest providers
    if lat and lng:
        # Check usage limits for provider lookups
        user_id = 1  # Mock user ID for now
        usage_check = require_usage_limit(user_id, 'provider_lookup')
        
        if 'error' in usage_check:
            if request.headers.get('Content-Type') == 'application/json' or request.args.get('format') == 'json':
                return jsonify({
                    'error': 'Usage limit exceeded',
                    'message': usage_check['message'],
                    'upgrade_required': True,
                    'current_plan': usage_check['current_plan']
                }), 429
            else:
                return render_template('providers.html', 
                                     usage_error=usage_check, 
                                     show_upgrade_modal=True)
        
        try:
            providers_data = nearest_providers(lat, lng, provider_type, limit)
        except Exception as e:
            print(f"Error getting nearest providers: {e}")
            providers_data = []
    
    # Return JSON for API calls, HTML for browser requests
    if request.headers.get('Content-Type') == 'application/json' or request.args.get('format') == 'json':
        return jsonify({
            'providers': providers_data,
            'count': len(providers_data),
            'filters': {
                'type': provider_type,
                'city': city,
                'lat': lat,
                'lng': lng,
                'limit': limit
            }
        })
    
    return render_template('providers.html', providers=providers_data)

@app.route('/dashboard')
def dashboard():
    # Mock user ID for now
    user_id = 1
    
    # Get recent symptom reports
    recent_symptoms = SymptomReport.query.filter_by(user_id=user_id)\
        .order_by(SymptomReport.created_at.desc()).limit(5).all()
    
    # Get recent mental health sessions with alerts
    recent_sessions = MentalHealthSession.query.filter_by(user_id=user_id)\
        .order_by(MentalHealthSession.created_at.desc()).limit(5).all()
    
    # Count alerts
    alert_count = MentalHealthSession.query.filter_by(user_id=user_id, alert_flag=True).count()
    
    # Mock subscription status
    subscription = {
        'plan': 'free',
        'expires_at': None,
        'features': ['Basic symptom checker', 'MindWell chat', 'Provider search']
    }
    
    return render_template('dashboard.html', 
                         recent_symptoms=recent_symptoms,
                         recent_sessions=recent_sessions,
                         alert_count=alert_count,
                         subscription=subscription)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        plan = request.form.get('plan', 'premium')
        user_id = 1  # Mock user ID
        
        # Update user subscription
        subscription = get_user_subscription(user_id)
        subscription.plan = plan
        db.session.commit()
        
        flash(f'Successfully upgraded to {plan.title()} plan!', 'success')
        return redirect(url_for('dashboard'))
    
    # GET request - show subscription options
    user_id = 1  # Mock user ID
    current_subscription = get_user_subscription(user_id)
    usage_summary = get_usage_summary(user_id)
    
    return render_template('subscribe.html', 
                         current_plan=current_subscription.plan,
                         usage_summary=usage_summary)

@app.route('/request-callback', methods=['POST'])
def request_callback():
    user_id = 1  # Mock user ID
    subscription = get_user_subscription(user_id)
    
    # Only premium users can request callbacks
    if subscription.plan != 'premium':
        return jsonify({
            'error': 'Premium subscription required',
            'message': 'Doctor callbacks are only available for Premium subscribers. Upgrade now!'
        }), 403
    
    data = request.get_json() if request.is_json else request.form
    phone = data.get('phone')
    preferred_time = data.get('preferred_time')
    reason = data.get('reason', '')
    
    if not phone:
        return jsonify({'error': 'Phone number is required'}), 400
    
    # Create callback request
    callback = DoctorCallback(
        user_id=user_id,
        phone=phone,
        preferred_time=preferred_time,
        reason=reason
    )
    
    try:
        db.session.add(callback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Doctor callback requested successfully! We will contact you within 24 hours.',
            'callback_id': callback.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to request callback'}), 500

# Basic auth decorator for admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != 'healthlink2024':
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Admin Area"'
            })
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin():
    # Get all alerts and sessions for admin review
    alerts = MentalHealthSession.query.filter_by(alert_flag=True)\
        .order_by(MentalHealthSession.created_at.desc()).all()
    
    # Get high-risk symptom reports
    high_risk_symptoms = SymptomReport.query.filter(
        SymptomReport.risk_level.in_(['high', 'critical'])
    ).order_by(SymptomReport.created_at.desc()).all()
    
    # Get recent appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(20).all()
    
    return render_template('admin.html',
                         alerts=alerts,
                         high_risk_symptoms=high_risk_symptoms,
                         recent_appointments=recent_appointments)

@app.route('/admin/mark_handled/<int:session_id>', methods=['POST'])
@admin_required
def mark_handled(session_id):
    session_record = MentalHealthSession.query.get_or_404(session_id)
    session_record.alert_flag = False
    
    try:
        db.session.commit()
        flash('Alert marked as handled', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating alert', 'error')
    
    return redirect(url_for('admin'))

def run_seed_sql():
    """Execute the seed SQL script"""
    import subprocess
    import pymysql
    from urllib.parse import urlparse
    
    database_url = config_db()
    parsed = urlparse(database_url)
    
    # Extract connection details
    host = parsed.hostname
    port = parsed.port or 3306
    user = parsed.username
    password = parsed.password
    database = parsed.path.lstrip('/')
    
    try:
        # Read and execute SQL file
        with open('scripts/seed_providers.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Connect and execute
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Split and execute SQL statements
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            for statement in statements:
                if statement and not statement.startswith('--'):
                    cursor.execute(statement)
        
        connection.commit()
        connection.close()
        print("✅ Seed data inserted successfully!")
        
    except Exception as e:
        print(f"❌ Error running seed script: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # CLI argument parsing
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--init-db':
            print("🔄 Initializing database...")
            with app.app_context():
                init_database()
            print("✅ Database initialized successfully!")
            
        elif command == '--seed':
            print("🔄 Seeding database with provider data...")
            run_seed_sql()
            
        else:
            print("❌ Unknown command. Available commands:")
            print("  python app.py --init-db  → Create tables and admin user")
            print("  python app.py --seed     → Run seed SQL script")
            sys.exit(1)
    else:
        # Run Flask development server
        app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
