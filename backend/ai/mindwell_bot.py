import json
import uuid
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# NLTK imports with automatic download
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    print("NLTK not installed. Please install with: pip install nltk")
    raise

# Download VADER lexicon if not present
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon', quiet=True)

class MindWellBot:
    def __init__(self):
        self.conversation_sessions = {}
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.intent_keywords = self._load_intent_keywords()
        self.guided_exercises = self._load_guided_exercises()
        self.crisis_terms = self._load_crisis_terms()
        self.empathetic_responses = self._load_empathetic_responses()
    
    def _load_intent_keywords(self) -> Dict[str, List[str]]:
        """Load intent detection keywords"""
        return {
            "stress": ["stressed", "pressure", "overwhelmed", "burden", "too much", "can't handle", "breaking point"],
            "anxiety": ["anxious", "worried", "nervous", "panic", "fear", "scared", "terrified", "dread"],
            "sleep": ["can't sleep", "insomnia", "tired", "exhausted", "sleepless", "restless", "nightmares"],
            "exam_pressure": ["exam", "test", "studying", "grades", "academic", "school stress", "performance"],
            "bullying": ["bullied", "picked on", "harassment", "mean", "excluded", "teased", "targeted"],
            "loneliness": ["lonely", "alone", "isolated", "no friends", "nobody", "disconnected", "empty"]
        }
    
    def _load_guided_exercises(self) -> Dict[str, Dict[str, Any]]:
        """Load guided mental health exercises"""
        return {
            "box_breathing": {
                "name": "Box Breathing",
                "description": "A calming breathing technique to reduce anxiety and stress",
                "steps": [
                    "Find a comfortable position and close your eyes",
                    "Breathe in slowly through your nose for 4 counts",
                    "Hold your breath for 4 counts",
                    "Exhale slowly through your mouth for 4 counts",
                    "Hold empty for 4 counts",
                    "Repeat this cycle 4-6 times"
                ],
                "duration": "2-3 minutes"
            },
            "grounding_5432": {
                "name": "5-4-3-2-1 Grounding",
                "description": "A sensory grounding technique to manage anxiety and panic",
                "steps": [
                    "Look around and name 5 things you can see",
                    "Notice 4 things you can touch or feel",
                    "Listen for 3 things you can hear",
                    "Identify 2 things you can smell",
                    "Think of 1 thing you can taste",
                    "Take a deep breath and notice how you feel now"
                ],
                "duration": "3-5 minutes"
            },
            "journaling_prompt": {
                "name": "Mindful Journaling",
                "description": "Writing exercise to process emotions and thoughts",
                "steps": [
                    "Find a quiet space with paper or your phone",
                    "Write about how you're feeling right now",
                    "Describe what triggered these feelings",
                    "Write down 3 things you're grateful for today",
                    "Note one small positive action you can take",
                    "End with a kind message to yourself"
                ],
                "duration": "5-10 minutes"
            },
            "progressive_relaxation": {
                "name": "Progressive Muscle Relaxation",
                "description": "Tension release technique for stress and anxiety",
                "steps": [
                    "Lie down or sit comfortably",
                    "Tense your toes for 5 seconds, then relax",
                    "Move up to your calves, tense and relax",
                    "Continue with thighs, abdomen, hands, arms",
                    "Tense your shoulders, then your face",
                    "Finally, tense your whole body, then completely relax"
                ],
                "duration": "10-15 minutes"
            },
            "mindful_walking": {
                "name": "Mindful Walking",
                "description": "Moving meditation to clear your mind and reduce stress",
                "steps": [
                    "Find a quiet path or space to walk slowly",
                    "Focus on the sensation of your feet touching the ground",
                    "Notice your breathing as you walk",
                    "Observe your surroundings without judgment",
                    "If your mind wanders, gently return focus to walking",
                    "Walk for as long as feels comfortable"
                ],
                "duration": "5-20 minutes"
            },
            "positive_affirmations": {
                "name": "Positive Affirmations",
                "description": "Self-compassion practice to build confidence and self-worth",
                "steps": [
                    "Find a quiet moment and take three deep breaths",
                    "Say aloud: 'I am worthy of love and respect'",
                    "Continue: 'I am doing my best with what I have'",
                    "Add: 'My feelings are valid and temporary'",
                    "Finish: 'I have the strength to get through this'",
                    "Repeat any that resonate with you"
                ],
                "duration": "2-5 minutes"
            },
            "worry_time": {
                "name": "Scheduled Worry Time",
                "description": "Technique to contain anxious thoughts to a specific time",
                "steps": [
                    "Set aside 15 minutes as your 'worry time'",
                    "Write down all your worries during this time",
                    "For each worry, ask: 'Can I do something about this?'",
                    "If yes, write one small action step",
                    "If no, practice letting it go for now",
                    "Outside worry time, remind yourself to wait until tomorrow"
                ],
                "duration": "15 minutes daily"
            },
            "gratitude_practice": {
                "name": "Gratitude Practice",
                "description": "Daily practice to shift focus toward positive aspects of life",
                "steps": [
                    "Think of three things that went well today",
                    "They can be small (good coffee) or big (friend's support)",
                    "For each, reflect on why it was meaningful",
                    "Notice how focusing on good things makes you feel",
                    "Consider sharing your gratitude with someone",
                    "Make this a daily habit before bed"
                ],
                "duration": "3-5 minutes"
            }
        }
    
    def _load_crisis_terms(self) -> List[str]:
        """Load crisis/self-harm indicators"""
        return [
            "want to end it", "end it all", "kill myself", "suicide", "want to die",
            "better off dead", "not worth living", "hurt myself", "self harm",
            "cutting", "overdose", "can't go on", "give up completely",
            "no point in living", "everyone would be better", "permanent solution"
        ]
    
    def _load_empathetic_responses(self) -> Dict[str, List[str]]:
        """Load empathetic, non-clinical responses for different intents"""
        return {
            "stress": [
                "It sounds like you're carrying a lot right now. That feeling of being overwhelmed is really tough.",
                "Stress can feel so heavy sometimes. You're not alone in feeling this way.",
                "I hear that you're under a lot of pressure. It makes sense that you'd feel stressed."
            ],
            "anxiety": [
                "Anxiety can feel so overwhelming and scary. Thank you for sharing this with me.",
                "Those anxious feelings are really difficult to deal with. You're being so brave by reaching out.",
                "I can sense how worried you're feeling. Anxiety can make everything feel so much bigger."
            ],
            "sleep": [
                "Sleep troubles can make everything feel so much harder. I'm sorry you're going through this.",
                "Not being able to sleep is exhausting in so many ways. Your tiredness is completely understandable.",
                "Sleep issues can really affect how we feel during the day. You're not alone in struggling with this."
            ],
            "exam_pressure": [
                "Academic pressure can feel intense and overwhelming. It's completely normal to feel stressed about this.",
                "School stress is so real and valid. You're dealing with a lot of expectations right now.",
                "Exam anxiety affects so many people. You're not alone in feeling this pressure."
            ],
            "bullying": [
                "I'm really sorry you're experiencing this. Being treated badly by others is never okay.",
                "What you're going through sounds really difficult and hurtful. You don't deserve to be treated this way.",
                "Bullying can be so isolating and painful. Thank you for trusting me with this."
            ],
            "loneliness": [
                "Feeling lonely can be one of the most painful experiences. I'm glad you reached out.",
                "Loneliness can feel so heavy and overwhelming. You're taking a brave step by connecting here.",
                "Feeling disconnected from others is really hard. You matter, and your feelings are valid."
            ],
            "general": [
                "Thank you for sharing what's on your mind. I'm here to listen and support you.",
                "It takes courage to reach out when you're struggling. I'm glad you're here.",
                "Whatever you're going through, you don't have to face it alone. I'm here with you."
            ]
        }
    
    def mindwell_reply(self, user_text: str) -> Dict[str, Any]:
        """
        Main function to analyze user text and generate empathetic response
        
        Args:
            user_text: User's message text
            
        Returns:
            Dictionary with response, sentiment, intents, exercises, and resources
        """
        # Analyze sentiment using NLTK VADER
        sentiment_scores = self.sentiment_analyzer.polarity_scores(user_text)
        
        # Detect crisis indicators first
        crisis_detected = self._detect_crisis(user_text)
        if crisis_detected:
            return self._generate_crisis_response(user_text, sentiment_scores)
        
        # Detect intents from keywords
        detected_intents = self._detect_intents(user_text)
        
        # Generate empathetic response
        response = self._generate_empathetic_response(user_text, sentiment_scores, detected_intents)
        
        # Add guided exercises based on intents
        exercises = self._suggest_exercises(detected_intents, sentiment_scores)
        
        # Add resource suggestions
        resources = self._suggest_resources(detected_intents)
        
        # Log message (would integrate with Message model)
        alert_flag = self._should_flag_message(user_text, sentiment_scores, detected_intents)
        self._log_message(user_text, response, alert_flag)
        
        return {
            "response": response,
            "sentiment": {
                "compound": sentiment_scores['compound'],
                "positive": sentiment_scores['pos'],
                "neutral": sentiment_scores['neu'],
                "negative": sentiment_scores['neg']
            },
            "intents_detected": detected_intents,
            "guided_exercises": exercises,
            "resources": resources,
            "alert_flag": alert_flag,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _detect_crisis(self, text: str) -> bool:
        """Detect self-harm indicators in user text"""
        text_lower = text.lower()
        
        for crisis_term in self.crisis_terms:
            if crisis_term in text_lower:
                return True
        
        return False
    
    def _generate_crisis_response(self, text: str, sentiment: Dict) -> Dict[str, Any]:
        """Generate crisis response for self-harm indicators"""
        crisis_message = (
            "I'm really concerned about what you're sharing with me. Your safety and wellbeing are the most important things right now.\n\n"
            "Please reach out to someone who can help immediately:\n\n"
            "🆘 **Crisis Helplines:**\n"
            "• National Suicide Prevention Lifeline: **988**\n"
            "• Crisis Text Line: Text **HOME** to **741741**\n"
            "• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/\n\n"
            "🤝 **Trusted Adults:**\n"
            "• A parent, guardian, or family member\n"
            "• School counselor or teacher\n"
            "• Healthcare provider\n"
            "• Religious or community leader\n\n"
            "You don't have to go through this alone. There are people who care about you and want to help. "
            "These feelings can change, and support is available."
        )
        
        return {
            "response": crisis_message,
            "sentiment": sentiment,
            "intents_detected": ["crisis"],
            "guided_exercises": [],
            "resources": ["crisis_helplines"],
            "alert_flag": True,
            "crisis_detected": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _detect_intents(self, text: str) -> List[str]:
        """Detect user intents from keyword matching"""
        text_lower = text.lower()
        detected_intents = []
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if intent not in detected_intents:
                        detected_intents.append(intent)
                    break
        
        return detected_intents if detected_intents else ["general"]
    
    def _generate_empathetic_response(self, text: str, sentiment: Dict, intents: List[str]) -> str:
        """Generate empathetic, non-clinical response"""
        # Determine primary intent
        primary_intent = intents[0] if intents else "general"
        
        # Get empathetic response based on intent
        responses = self.empathetic_responses.get(primary_intent, self.empathetic_responses["general"])
        base_response = responses[0]  # Use first response for consistency
        
        # Add sentiment-aware follow-up
        if sentiment['compound'] <= -0.5:  # Very negative sentiment
            base_response += " I can hear how much pain you're in right now."
        elif sentiment['compound'] <= -0.1:  # Somewhat negative
            base_response += " These feelings are completely valid."
        elif sentiment['compound'] >= 0.1:  # Positive sentiment
            base_response += " I'm glad you felt comfortable sharing this with me."
        
        return base_response
    
    def _suggest_exercises(self, intents: List[str], sentiment: Dict) -> List[Dict[str, Any]]:
        """Suggest appropriate guided exercises based on intents and sentiment"""
        suggested = []
        
        # Map intents to exercises
        exercise_mapping = {
            "stress": ["box_breathing", "progressive_relaxation"],
            "anxiety": ["grounding_5432", "box_breathing"],
            "sleep": ["progressive_relaxation", "mindful_walking"],
            "exam_pressure": ["worry_time", "box_breathing"],
            "bullying": ["positive_affirmations", "journaling_prompt"],
            "loneliness": ["gratitude_practice", "journaling_prompt"]
        }
        
        # Add exercises based on detected intents
        for intent in intents:
            if intent in exercise_mapping:
                for exercise_key in exercise_mapping[intent][:2]:  # Max 2 per intent
                    if exercise_key in self.guided_exercises:
                        exercise = self.guided_exercises[exercise_key].copy()
                        exercise["key"] = exercise_key
                        if exercise not in suggested:
                            suggested.append(exercise)
        
        # If no specific exercises, suggest based on sentiment
        if not suggested:
            if sentiment['compound'] <= -0.3:
                suggested.append({**self.guided_exercises["box_breathing"], "key": "box_breathing"})
            else:
                suggested.append({**self.guided_exercises["gratitude_practice"], "key": "gratitude_practice"})
        
        return suggested[:3]  # Limit to 3 exercises
    
    def _suggest_resources(self, intents: List[str]) -> List[str]:
        """Suggest resources based on detected intents"""
        resources = []
        
        resource_mapping = {
            "stress": ["stress_management_tips", "time_management_resources"],
            "anxiety": ["anxiety_coping_strategies", "relaxation_techniques"],
            "sleep": ["sleep_hygiene_guide", "bedtime_routine_tips"],
            "exam_pressure": ["study_techniques", "test_anxiety_help"],
            "bullying": ["bullying_support_resources", "building_confidence_tips"],
            "loneliness": ["social_connection_ideas", "community_resources"]
        }
        
        for intent in intents:
            if intent in resource_mapping:
                resources.extend(resource_mapping[intent])
        
        # Always include general mental health resources
        resources.append("mental_health_basics")
        
        return list(set(resources))[:4]  # Remove duplicates, limit to 4
    
    def _should_flag_message(self, text: str, sentiment: Dict, intents: List[str]) -> bool:
        """Determine if message should be flagged for review"""
        # Flag if very negative sentiment
        if sentiment['compound'] <= -0.7:
            return True
        
        # Flag if contains concerning intents
        concerning_intents = ["bullying", "loneliness"]
        if any(intent in concerning_intents for intent in intents):
            return True
        
        # Flag if contains concerning keywords (but not crisis level)
        concerning_keywords = ["hopeless", "worthless", "can't cope", "giving up"]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in concerning_keywords):
            return True
        
        return False
    
    def _log_message(self, user_text: str, response: str, alert_flag: bool) -> None:
        """Log message interaction (placeholder for Message model integration)"""
        # This would integrate with the Message model from models.py
        # For now, just print for debugging
        log_entry = {
            "user_message": user_text,
            "bot_response": response,
            "alert_flag": alert_flag,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # In production, this would save to database:
        # message = Message(
        #     content=user_text,
        #     response=response,
        #     alert_flag=alert_flag,
        #     timestamp=datetime.utcnow()
        # )
        # db.session.add(message)
        # db.session.commit()
        
        print(f"[MindWell Log] Alert: {alert_flag}, Time: {log_entry['timestamp']}")
    
# Convenience function for easy import
def mindwell_reply(user_text: str) -> Dict[str, Any]:
    """
    Standalone function to generate MindWell bot response
    
    Args:
        user_text: User's message text
        
    Returns:
        Dictionary with empathetic response, sentiment analysis, and resources
    """
    bot = MindWellBot()
    return bot.mindwell_reply(user_text)
