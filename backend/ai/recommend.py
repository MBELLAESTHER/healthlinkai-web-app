import json
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class RecommendationEngine:
    """AI-powered recommendation engine for health services and wellness content."""
    
    def __init__(self):
        self.wellness_tips = [
            {
                "category": "nutrition",
                "title": "Stay Hydrated",
                "description": "Drink at least 8 glasses of water daily to maintain optimal health.",
                "priority": "high"
            },
            {
                "category": "exercise",
                "title": "Daily Movement",
                "description": "Aim for at least 30 minutes of physical activity each day.",
                "priority": "high"
            },
            {
                "category": "mental_health",
                "title": "Mindfulness Practice",
                "description": "Take 10 minutes daily for meditation or deep breathing exercises.",
                "priority": "medium"
            },
            {
                "category": "sleep",
                "title": "Sleep Hygiene",
                "description": "Maintain a consistent sleep schedule with 7-9 hours of quality sleep.",
                "priority": "high"
            },
            {
                "category": "nutrition",
                "title": "Balanced Diet",
                "description": "Include fruits, vegetables, whole grains, and lean proteins in your meals.",
                "priority": "medium"
            }
        ]
        
        self.provider_specialties = {
            "anxiety": ["psychiatrist", "psychologist", "therapist"],
            "depression": ["psychiatrist", "psychologist", "therapist"],
            "physical_symptoms": ["general_practitioner", "internist"],
            "chronic_pain": ["pain_specialist", "rheumatologist", "neurologist"],
            "heart_issues": ["cardiologist", "general_practitioner"],
            "mental_health": ["psychiatrist", "psychologist", "therapist"]
        }
    
    def get_personalized_recommendations(self, user_data: Dict = None) -> Dict[str, Any]:
        """Generate personalized health recommendations."""
        
        recommendations = {
            "wellness_tips": self._get_wellness_recommendations(user_data),
            "provider_suggestions": self._get_provider_recommendations(user_data),
            "health_articles": self._get_article_recommendations(user_data),
            "preventive_care": self._get_preventive_care_recommendations(user_data)
        }
        
        return recommendations
    
    def _get_wellness_recommendations(self, user_data: Dict = None) -> List[Dict]:
        """Get personalized wellness tips."""
        # In a real implementation, this would analyze user data
        selected_tips = random.sample(self.wellness_tips, min(3, len(self.wellness_tips)))
        
        for tip in selected_tips:
            tip["personalized"] = True
            tip["recommended_at"] = datetime.utcnow().isoformat()
        
        return selected_tips
    
    def _get_provider_recommendations(self, user_data: Dict = None) -> List[Dict]:
        """Recommend healthcare providers based on user needs."""
        recommendations = []
        
        # Mock provider recommendations
        providers = [
            {
                "name": "Dr. Sarah Johnson",
                "specialty": "General Practitioner",
                "rating": 4.8,
                "distance": "2.3 miles",
                "availability": "Next available: Tomorrow",
                "reason": "Highly rated for preventive care"
            },
            {
                "name": "Dr. Michael Chen",
                "specialty": "Mental Health Counselor",
                "rating": 4.9,
                "distance": "1.8 miles",
                "availability": "Next available: This week",
                "reason": "Specializes in anxiety and stress management"
            }
        ]
        
        return providers
    
    def _get_article_recommendations(self, user_data: Dict = None) -> List[Dict]:
        """Recommend health articles and educational content."""
        articles = [
            {
                "title": "Understanding Stress and Its Impact on Health",
                "category": "mental_health",
                "read_time": "5 min",
                "url": "#",
                "summary": "Learn about stress management techniques and their benefits."
            },
            {
                "title": "The Importance of Regular Health Checkups",
                "category": "preventive_care",
                "read_time": "7 min",
                "url": "#",
                "summary": "Why routine medical examinations are crucial for early detection."
            },
            {
                "title": "Nutrition Basics for Better Health",
                "category": "nutrition",
                "read_time": "6 min",
                "url": "#",
                "summary": "Essential nutrients and how to incorporate them into your diet."
            }
        ]
        
        return articles
    
    def _get_preventive_care_recommendations(self, user_data: Dict = None) -> List[Dict]:
        """Recommend preventive care based on age, gender, and health history."""
        # Mock preventive care recommendations
        recommendations = [
            {
                "type": "Annual Physical Exam",
                "due_date": (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "priority": "high",
                "description": "Comprehensive health assessment and screening"
            },
            {
                "type": "Blood Pressure Check",
                "due_date": (datetime.utcnow() + timedelta(days=90)).strftime("%Y-%m-%d"),
                "priority": "medium",
                "description": "Monitor cardiovascular health"
            },
            {
                "type": "Mental Health Screening",
                "due_date": (datetime.utcnow() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "priority": "medium",
                "description": "Assess mental wellness and stress levels"
            }
        ]
        
        return recommendations
    
    def get_symptom_based_recommendations(self, symptoms: List[str], severity: str = "medium") -> Dict[str, Any]:
        """Generate recommendations based on reported symptoms."""
        
        recommendations = {
            "immediate_actions": [],
            "provider_types": [],
            "self_care": [],
            "when_to_seek_help": []
        }
        
        # Analyze symptoms and provide appropriate recommendations
        if any(symptom in ["chest pain", "difficulty breathing", "severe headache"] for symptom in symptoms):
            recommendations["immediate_actions"].append({
                "action": "Seek immediate medical attention",
                "urgency": "urgent",
                "description": "These symptoms may require emergency care"
            })
            recommendations["provider_types"].extend(["emergency_room", "urgent_care"])
        
        elif any(symptom in ["anxiety", "depression", "stress"] for symptom in symptoms):
            recommendations["provider_types"].extend(["therapist", "psychiatrist", "counselor"])
            recommendations["self_care"].extend([
                "Practice deep breathing exercises",
                "Maintain regular sleep schedule",
                "Consider mindfulness meditation"
            ])
        
        else:
            recommendations["provider_types"].append("general_practitioner")
            recommendations["self_care"].extend([
                "Rest and stay hydrated",
                "Monitor symptoms",
                "Maintain healthy diet"
            ])
        
        recommendations["when_to_seek_help"] = [
            "If symptoms worsen or persist",
            "If you develop new concerning symptoms",
            "If you feel unsure about your condition"
        ]
        
        return recommendations
    
    def get_mental_health_resources(self, mood_data: Dict = None) -> Dict[str, Any]:
        """Provide mental health resources and coping strategies."""
        
        resources = {
            "coping_strategies": [
                {
                    "technique": "4-7-8 Breathing",
                    "description": "Inhale for 4, hold for 7, exhale for 8 seconds",
                    "category": "anxiety"
                },
                {
                    "technique": "Progressive Muscle Relaxation",
                    "description": "Tense and relax muscle groups systematically",
                    "category": "stress"
                },
                {
                    "technique": "Gratitude Journaling",
                    "description": "Write down 3 things you're grateful for daily",
                    "category": "depression"
                }
            ],
            "crisis_resources": [
                {
                    "name": "National Suicide Prevention Lifeline",
                    "phone": "988",
                    "available": "24/7"
                },
                {
                    "name": "Crisis Text Line",
                    "contact": "Text HOME to 741741",
                    "available": "24/7"
                }
            ],
            "self_assessment_tools": [
                {
                    "name": "PHQ-9 Depression Screen",
                    "description": "Quick assessment for depression symptoms"
                },
                {
                    "name": "GAD-7 Anxiety Screen",
                    "description": "Generalized anxiety disorder assessment"
                }
            ]
        }
        
        return resources

    def nearest_providers(self, lat: float, lng: float, provider_type: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find nearest healthcare providers using Haversine distance calculation
        
        Args:
            lat: User's latitude
            lng: User's longitude
            provider_type: Optional filter by provider type/specialty
            limit: Maximum number of providers to return
            
        Returns:
            List of nearest providers with calculated distances
        """
        # Mock provider database - in production this would query actual database
        providers_db = [
            {
                "id": 1,
                "name": "Dr. Sarah Johnson",
                "specialty": "General Practitioner",
                "type": "general_practitioner",
                "phone": "+237-233-44-55-66",
                "email": "dr.johnson@healthcenter.cm",
                "address": "123 Rue de la Paix, Douala",
                "latitude": 4.0511,
                "longitude": 9.7679,
                "rating": 4.8,
                "availability": "Available today",
                "languages": ["French", "English"]
            },
            {
                "id": 2,
                "name": "Dr. Michael Chen",
                "specialty": "Psychiatrist",
                "type": "psychiatrist",
                "phone": "+237-233-44-55-77",
                "email": "dr.chen@mindwellclinic.cm",
                "address": "456 Avenue Kennedy, Yaoundé",
                "latitude": 3.8480,
                "longitude": 11.5021,
                "rating": 4.9,
                "availability": "Next available: Tomorrow",
                "languages": ["French", "English", "Chinese"]
            },
            {
                "id": 3,
                "name": "Dr. Amina Kouassi",
                "specialty": "Cardiologist",
                "type": "cardiologist",
                "phone": "+237-233-44-55-88",
                "email": "dr.kouassi@heartcenter.cm",
                "address": "789 Boulevard de la Liberté, Douala",
                "latitude": 4.0611,
                "longitude": 9.7779,
                "rating": 4.7,
                "availability": "Available this week",
                "languages": ["French", "English", "Arabic"]
            },
            {
                "id": 4,
                "name": "Dr. Jean-Paul Mbarga",
                "specialty": "Psychologist",
                "type": "psychologist",
                "phone": "+237-233-44-55-99",
                "email": "dr.mbarga@therapycenter.cm",
                "address": "321 Rue du Commerce, Yaoundé",
                "latitude": 3.8580,
                "longitude": 11.5121,
                "rating": 4.6,
                "availability": "Available next week",
                "languages": ["French", "English"]
            },
            {
                "id": 5,
                "name": "Dr. Marie Dubois",
                "specialty": "Pediatrician",
                "type": "pediatrician",
                "phone": "+237-233-44-66-00",
                "email": "dr.dubois@childhealth.cm",
                "address": "654 Avenue de l'Indépendance, Douala",
                "latitude": 4.0411,
                "longitude": 9.7579,
                "rating": 4.8,
                "availability": "Available today",
                "languages": ["French", "English"]
            },
            {
                "id": 6,
                "name": "Dr. Ibrahim Hassan",
                "specialty": "Dermatologist",
                "type": "dermatologist",
                "phone": "+237-233-44-66-11",
                "email": "dr.hassan@skinclinic.cm",
                "address": "987 Rue de la République, Yaoundé",
                "latitude": 3.8380,
                "longitude": 11.4921,
                "rating": 4.5,
                "availability": "Available this week",
                "languages": ["French", "English", "Arabic"]
            },
            {
                "id": 7,
                "name": "Dr. Catherine Nkomo",
                "specialty": "Gynecologist",
                "type": "gynecologist",
                "phone": "+237-233-44-66-22",
                "email": "dr.nkomo@womenshealth.cm",
                "address": "147 Boulevard du 20 Mai, Yaoundé",
                "latitude": 3.8680,
                "longitude": 11.5221,
                "rating": 4.9,
                "availability": "Available next week",
                "languages": ["French", "English"]
            },
            {
                "id": 8,
                "name": "Dr. Paul Essomba",
                "specialty": "Orthopedist",
                "type": "orthopedist",
                "phone": "+237-233-44-66-33",
                "email": "dr.essomba@boneclinic.cm",
                "address": "258 Rue Joss, Douala",
                "latitude": 4.0711,
                "longitude": 9.7879,
                "rating": 4.4,
                "availability": "Available tomorrow",
                "languages": ["French", "English"]
            }
        ]
        
        # Filter by provider type if specified
        if provider_type:
            providers_db = [p for p in providers_db if p['type'].lower() == provider_type.lower()]
        
        # Calculate distances using Haversine formula
        providers_with_distance = []
        for provider in providers_db:
            distance = self._calculate_haversine_distance(
                lat, lng, 
                provider['latitude'], provider['longitude']
            )
            
            provider_copy = provider.copy()
            provider_copy['distance_km'] = round(distance, 2)
            provider_copy['distance_display'] = f"{distance:.1f} km"
            providers_with_distance.append(provider_copy)
        
        # Sort by distance and return limited results
        providers_with_distance.sort(key=lambda x: x['distance_km'])
        return providers_with_distance[:limit]
    
    def _calculate_haversine_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth using Haversine formula
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Distance in kilometers
        """
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers
        earth_radius_km = 6371.0
        
        # Calculate the distance
        distance = earth_radius_km * c
        
        return distance


# Convenience function for easy import
def nearest_providers(lat: float, lng: float, provider_type: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Standalone function to find nearest healthcare providers
    
    Args:
        lat: User's latitude
        lng: User's longitude
        provider_type: Optional filter by provider type
        limit: Maximum number of providers to return
        
    Returns:
        List of nearest providers with distances
    """
    engine = RecommendationEngine()
    return engine.nearest_providers(lat, lng, provider_type, limit)
