import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any

class SymptomChecker:
    def __init__(self):
        self.rules_path = os.path.join(os.path.dirname(__file__), 'symptom_rules.json')
        self.load_rules()
    
    def load_rules(self):
        """Load symptom analysis rules from JSON file"""
        try:
            with open(self.rules_path, 'r') as f:
                self.rules = json.load(f)
        except FileNotFoundError:
            self.rules = self._get_default_rules()
    
    def _get_default_rules(self):
        """Fallback rules if JSON file not found"""
        return {
            "symptom_rules": [],
            "red_flag_terms": [],
            "keyword_mappings": {},
            "risk_bands": {
                "low": {"range": [0, 30], "message": "Low risk", "actions": []},
                "medium": {"range": [31, 60], "message": "Medium risk", "actions": []},
                "high": {"range": [61, 89], "message": "High risk", "actions": []},
                "emergency": {"range": [90, 100], "message": "Emergency", "actions": []}
            },
            "disclaimers": []
        }
    
    def analyze_symptoms(self, text: str, selected: List[str]) -> Dict[str, Any]:
        """
        Analyze provided symptoms and return assessment
        
        Args:
            text: Free-text description of symptoms
            selected: List of selected symptom chips
            
        Returns:
            Dictionary containing analysis results with conditions, advice, and risk level
        """
        if not text and not selected:
            return {"error": "No symptoms provided"}
        
        # Normalize and combine all symptom inputs
        all_symptoms = self._normalize_symptoms(text, selected)
        
        # Check for red flag terms first (emergency conditions)
        red_flag_result = self._check_red_flags(text, selected)
        if red_flag_result:
            return red_flag_result
        
        # Match symptoms to conditions using rules
        matched_conditions = self._match_symptom_rules(all_symptoms)
        
        # Calculate overall risk score
        risk_score = self._calculate_risk_score(matched_conditions, all_symptoms)
        
        # Determine risk band
        risk_band = self._get_risk_band(risk_score)
        
        # Generate advice based on conditions and risk
        advice = self._generate_advice(matched_conditions, risk_band, all_symptoms)
        
        # Create final assessment
        assessment = {
            "conditions": [
                {
                    "name": condition["name"],
                    "probability": f"{int(condition['probability'] * 100)}%",
                    "description": f"Based on symptom pattern analysis"
                }
                for condition in matched_conditions[:3]  # Top 3 conditions
            ],
            "advice": advice,
            "risk": risk_band,
            "risk_score": risk_score,
            "symptoms_analyzed": all_symptoms,
            "timestamp": datetime.utcnow().isoformat(),
            "disclaimers": self.rules.get("disclaimers", [])
        }
        
        return assessment
    
    def _normalize_symptoms(self, text: str, selected: List[str]) -> List[str]:
        """Normalize and combine text and selected symptoms"""
        all_symptoms = []
        
        # Add selected symptoms
        if selected:
            all_symptoms.extend([s.lower().strip() for s in selected])
        
        # Process free text
        if text:
            # Clean and normalize text
            normalized_text = re.sub(r'[^\w\s]', ' ', text.lower())
            words = normalized_text.split()
            
            # Map keywords to standard symptom terms
            keyword_mappings = self.rules.get("keyword_mappings", {})
            for standard_term, keywords in keyword_mappings.items():
                for keyword in keywords:
                    if keyword in normalized_text:
                        if standard_term not in all_symptoms:
                            all_symptoms.append(standard_term)
        
        return list(set(all_symptoms))  # Remove duplicates
    
    def _check_red_flags(self, text: str, selected: List[str]) -> Dict[str, Any]:
        """Check for emergency red flag terms"""
        combined_text = f"{text} {' '.join(selected or [])}".lower()
        
        red_flag_terms = self.rules.get("red_flag_terms", [])
        
        for red_flag in red_flag_terms:
            terms = red_flag.get("terms", [])
            for term in terms:
                if term.lower() in combined_text:
                    return {
                        "conditions": [{
                            "name": red_flag["condition"],
                            "probability": "High concern",
                            "description": "Emergency symptoms detected"
                        }],
                        "advice": [
                            "🚨 EMERGENCY: Seek immediate medical attention",
                            "Call emergency services (911) immediately",
                            "Do not drive yourself to the hospital",
                            "Stay calm and follow emergency dispatcher instructions"
                        ],
                        "risk": "emergency",
                        "risk_score": red_flag["risk_score"],
                        "emergency": True,
                        "symptoms_analyzed": [term],
                        "timestamp": datetime.utcnow().isoformat(),
                        "disclaimers": self.rules.get("disclaimers", [])
                    }
        
        return None
    
    def _match_symptom_rules(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """Match symptoms against predefined rules"""
        matched_conditions = []
        symptom_rules = self.rules.get("symptom_rules", [])
        
        for rule in symptom_rules:
            rule_symptoms = rule.get("symptoms", [])
            match_count = 0
            
            # Count how many rule symptoms match user symptoms
            for rule_symptom in rule_symptoms:
                if any(rule_symptom in user_symptom for user_symptom in symptoms):
                    match_count += 1
            
            # If we have a partial or full match
            if match_count > 0:
                match_ratio = match_count / len(rule_symptoms)
                
                # Add conditions from this rule
                for condition in rule.get("conditions", []):
                    condition_copy = condition.copy()
                    # Adjust probability based on match ratio
                    condition_copy["probability"] = condition["probability"] * match_ratio
                    condition_copy["match_ratio"] = match_ratio
                    condition_copy["rule_symptoms"] = rule_symptoms
                    matched_conditions.append(condition_copy)
        
        # Sort by probability
        matched_conditions.sort(key=lambda x: x["probability"], reverse=True)
        return matched_conditions
    
    def _calculate_risk_score(self, conditions: List[Dict[str, Any]], symptoms: List[str]) -> int:
        """Calculate overall risk score (0-100)"""
        if not conditions:
            # Base risk on number of symptoms if no conditions matched
            return min(len(symptoms) * 10, 50)
        
        # Get highest risk score from matched conditions
        max_risk = max(condition.get("risk_score", 30) for condition in conditions)
        
        # Adjust based on number of symptoms
        symptom_multiplier = 1 + (len(symptoms) - 1) * 0.1
        
        # Conservative approach - round up
        final_score = min(int(max_risk * symptom_multiplier), 100)
        
        return final_score
    
    def _get_risk_band(self, risk_score: int) -> str:
        """Determine risk band from score"""
        risk_bands = self.rules.get("risk_bands", {})
        
        for band, data in risk_bands.items():
            risk_range = data.get("range", [0, 100])
            if risk_range[0] <= risk_score <= risk_range[1]:
                return band
        
        # Default fallback
        if risk_score >= 90:
            return "emergency"
        elif risk_score >= 61:
            return "high"
        elif risk_score >= 31:
            return "medium"
        else:
            return "low"
    
    def _generate_advice(self, conditions: List[Dict[str, Any]], risk_band: str, symptoms: List[str]) -> List[str]:
        """Generate specific advice based on conditions and risk"""
        advice = []
        
        # Get risk band specific advice
        risk_bands = self.rules.get("risk_bands", {})
        if risk_band in risk_bands:
            band_data = risk_bands[risk_band]
            advice.append(band_data.get("message", ""))
            advice.extend(band_data.get("actions", []))
        
        # Add condition-specific advice
        if conditions:
            top_condition = conditions[0]
            condition_name = top_condition.get("name", "").lower()
            
            if "infection" in condition_name or "malaria" in condition_name:
                advice.append("Monitor temperature and stay well hydrated")
                advice.append("Avoid contact with others to prevent spread")
            
            if "migraine" in condition_name or "headache" in condition_name:
                advice.append("Rest in a dark, quiet room")
                advice.append("Apply cold or warm compress to head/neck")
            
            if "pneumonia" in condition_name or "respiratory" in condition_name:
                advice.append("Get plenty of rest and avoid strenuous activity")
                advice.append("Use a humidifier or breathe steam from hot shower")
            
            if "gastroenteritis" in condition_name:
                advice.append("Follow BRAT diet (bananas, rice, applesauce, toast)")
                advice.append("Replace lost fluids with oral rehydration solutions")
        
        # Add symptom-specific advice
        if any("fever" in s for s in symptoms):
            advice.append("Monitor temperature regularly")
        
        if any("pain" in s for s in symptoms):
            advice.append("Consider appropriate pain relief medication")
        
        # Always include safety reminder
        advice.append("⚠️ Seek immediate care if symptoms worsen or new concerning symptoms develop")
        
        return list(set(advice))  # Remove duplicates


# Convenience function for easy import
def analyze_symptoms(text: str, selected: List[str]) -> Dict[str, Any]:
    """
    Standalone function to analyze symptoms
    
    Args:
        text: Free-text description of symptoms
        selected: List of selected symptom chips
        
    Returns:
        Dictionary with conditions, advice, and risk assessment
    """
    checker = SymptomChecker()
    return checker.analyze_symptoms(text, selected)
