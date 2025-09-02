#!/usr/bin/env python3
"""
HealthLinkAI Setup and Run Script
This script initializes the database and starts the Flask application.
"""

import os
import sys
from app import app
from models import init_database

def setup_database():
    """Initialize the database with tables and seed data"""
    print("🔧 Setting up database...")
    try:
        with app.app_context():
            init_database()
        print("✅ Database setup complete!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("💡 Make sure MySQL is running and credentials in .env are correct")
        return False

def run_application():
    """Start the Flask application"""
    print("🚀 Starting HealthLinkAI application...")
    print("📱 Access the app at: http://localhost:5000")
    print("🔐 Admin panel: http://localhost:5000/admin (admin/healthlink2024)")
    print("💰 Subscription page: http://localhost:5000/subscribe")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )

if __name__ == '__main__':
    print("🏥 HealthLinkAI - Freemium Health Platform")
    print("=" * 50)
    
    # Setup database
    if setup_database():
        # Run the application
        try:
            run_application()
        except KeyboardInterrupt:
            print("\n👋 HealthLinkAI stopped. Goodbye!")
            sys.exit(0)
    else:
        print("❌ Cannot start application due to database setup failure")
        sys.exit(1)
