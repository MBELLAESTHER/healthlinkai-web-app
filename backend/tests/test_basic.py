import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, SymptomReport, MentalHealthSession, HealthProvider

class HealthLinkAITestCase(unittest.TestCase):
    """Base test case for HealthLinkAI application."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.create_test_data()
    
    def tearDown(self):
        """Clean up after each test method."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_test_data(self):
        """Create test data for testing."""
        # Create test user
        test_user = User(
            email='test@example.com',
            username='testuser',
            password_hash='hashed_password',
            first_name='Test',
            last_name='User',
            gender='other'
        )
        db.session.add(test_user)
        
        # Create test health provider
        test_provider = HealthProvider(
            name='Dr. Test Provider',
            specialty='General Practice',
            description='Test healthcare provider',
            phone='555-0123',
            email='provider@example.com',
            rating=4.5,
            review_count=100,
            accepts_insurance=True,
            telehealth_available=True
        )
        db.session.add(test_provider)
        
        db.session.commit()

class TestRoutes(HealthLinkAITestCase):
    """Test case for application routes."""
    
    def test_index_page(self):
        """Test the index page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HealthLinkAI', response.data)
    
    def test_symptom_checker_page(self):
        """Test the symptom checker page loads correctly."""
        response = self.client.get('/symptom-checker')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Symptom Checker', response.data)
    
    def test_mindwell_page(self):
        """Test the MindWell page loads correctly."""
        response = self.client.get('/mindwell')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MindWell', response.data)
    
    def test_providers_page(self):
        """Test the providers page loads correctly."""
        response = self.client.get('/providers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Healthcare Providers', response.data)
    
    def test_dashboard_page(self):
        """Test the dashboard page loads correctly."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health Dashboard', response.data)

class TestAPI(HealthLinkAITestCase):
    """Test case for API endpoints."""
    
    def test_symptom_checker_api(self):
        """Test the symptom checker API endpoint."""
        test_data = {
            'symptoms': ['headache', 'fever', 'sore throat'],
            'age': 30,
            'gender': 'female'
        }
        
        response = self.client.post('/api/check-symptoms',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('risk_level', data)
        self.assertIn('possible_conditions', data)
        self.assertIn('recommendations', data)
    
    def test_symptom_checker_api_missing_data(self):
        """Test symptom checker API with missing data."""
        test_data = {
            'symptoms': []  # Empty symptoms
        }
        
        response = self.client.post('/api/check-symptoms',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 400])
    
    def test_mindwell_chat_api(self):
        """Test the MindWell chat API endpoint."""
        test_data = {
            'message': 'I am feeling anxious',
            'session_id': 'test_session_123'
        }
        
        response = self.client.post('/api/mindwell-chat',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
    
    def test_recommendations_api(self):
        """Test the recommendations API endpoint."""
        response = self.client.get('/api/recommendations')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('wellness_tips', data)
        self.assertIn('provider_suggestions', data)

class TestModels(HealthLinkAITestCase):
    """Test case for database models."""
    
    def test_user_model(self):
        """Test User model creation and attributes."""
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.first_name, 'Test')
            self.assertEqual(user.last_name, 'User')
    
    def test_symptom_report_creation(self):
        """Test SymptomReport model creation."""
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            
            report = SymptomReport(
                user_id=user.id,
                session_id='test_session',
                symptoms=['headache', 'fever'],
                risk_level='medium',
                recommendations=['rest', 'hydrate']
            )
            db.session.add(report)
            db.session.commit()
            
            saved_report = SymptomReport.query.filter_by(session_id='test_session').first()
            self.assertIsNotNone(saved_report)
            self.assertEqual(saved_report.risk_level, 'medium')
            self.assertEqual(len(saved_report.symptoms), 2)
    
    def test_mental_health_session_creation(self):
        """Test MentalHealthSession model creation."""
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            
            session = MentalHealthSession(
                user_id=user.id,
                session_id='mindwell_test_session',
                conversation_history=[
                    {'role': 'user', 'message': 'I feel anxious'},
                    {'role': 'assistant', 'message': 'I understand you are feeling anxious...'}
                ],
                session_type='anxiety'
            )
            db.session.add(session)
            db.session.commit()
            
            saved_session = MentalHealthSession.query.filter_by(session_id='mindwell_test_session').first()
            self.assertIsNotNone(saved_session)
            self.assertEqual(saved_session.session_type, 'anxiety')
            self.assertEqual(len(saved_session.conversation_history), 2)
    
    def test_health_provider_model(self):
        """Test HealthProvider model creation and attributes."""
        with self.app.app_context():
            provider = HealthProvider.query.filter_by(name='Dr. Test Provider').first()
            self.assertIsNotNone(provider)
            self.assertEqual(provider.specialty, 'General Practice')
            self.assertEqual(provider.rating, 4.5)
            self.assertTrue(provider.accepts_insurance)
            self.assertTrue(provider.telehealth_available)

class TestAIComponents(HealthLinkAITestCase):
    """Test case for AI components."""
    
    def test_symptom_checker_import(self):
        """Test that SymptomChecker can be imported and initialized."""
        try:
            from ai.symptom_checker import SymptomChecker
            checker = SymptomChecker()
            self.assertIsNotNone(checker)
        except ImportError:
            self.fail("SymptomChecker could not be imported")
    
    def test_mindwell_bot_import(self):
        """Test that MindWellBot can be imported and initialized."""
        try:
            from ai.mindwell_bot import MindWellBot
            bot = MindWellBot()
            self.assertIsNotNone(bot)
        except ImportError:
            self.fail("MindWellBot could not be imported")
    
    def test_recommendation_engine_import(self):
        """Test that RecommendationEngine can be imported and initialized."""
        try:
            from ai.recommend import RecommendationEngine
            engine = RecommendationEngine()
            self.assertIsNotNone(engine)
        except ImportError:
            self.fail("RecommendationEngine could not be imported")

class TestSecurity(HealthLinkAITestCase):
    """Test case for security features."""
    
    def test_sql_injection_protection(self):
        """Test protection against SQL injection attacks."""
        malicious_input = "'; DROP TABLE users; --"
        
        test_data = {
            'symptoms': [malicious_input],
            'age': 30,
            'gender': 'male'
        }
        
        response = self.client.post('/api/check-symptoms',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # Should not cause server error
        self.assertNotEqual(response.status_code, 500)
        
        # Database should still be intact
        with self.app.app_context():
            users = User.query.all()
            self.assertGreater(len(users), 0)
    
    def test_xss_protection(self):
        """Test protection against XSS attacks."""
        malicious_script = "<script>alert('XSS')</script>"
        
        test_data = {
            'message': malicious_script,
            'session_id': 'test_xss_session'
        }
        
        response = self.client.post('/api/mindwell-chat',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 400])

class TestPerformance(HealthLinkAITestCase):
    """Test case for performance considerations."""
    
    def test_large_symptom_list(self):
        """Test handling of large symptom lists."""
        large_symptom_list = ['symptom_' + str(i) for i in range(100)]
        
        test_data = {
            'symptoms': large_symptom_list,
            'age': 25,
            'gender': 'other'
        }
        
        response = self.client.post('/api/check-symptoms',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # Should handle large inputs gracefully
        self.assertIn(response.status_code, [200, 400, 413])
    
    def test_concurrent_requests(self):
        """Test handling of multiple concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            test_data = {
                'symptoms': ['headache'],
                'age': 30,
                'gender': 'female'
            }
            response = self.client.post('/api/check-symptoms',
                                      data=json.dumps(test_data),
                                      content_type='application/json')
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        for status_code in results:
            self.assertEqual(status_code, 200)

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestRoutes))
    test_suite.addTest(unittest.makeSuite(TestAPI))
    test_suite.addTest(unittest.makeSuite(TestModels))
    test_suite.addTest(unittest.makeSuite(TestAIComponents))
    test_suite.addTest(unittest.makeSuite(TestSecurity))
    test_suite.addTest(unittest.makeSuite(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
