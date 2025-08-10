import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class SymptomAnalyzer:
    def __init__(self):
        # Enhanced symptom database with Arabic translations
        self.symptom_database = {
            # Neurological symptoms
            'headache': {
                'en': 'headache',
                'ar': 'صداع',
                'severity': 'moderate',
                'category': 'neurological',
                'keywords': ['head', 'pain', 'ache', 'migraine', 'صداع', 'رأس', 'ألم']
            },
            'dizziness': {
                'en': 'dizziness',
                'ar': 'دوخة',
                'severity': 'mild',
                'category': 'neurological',
                'keywords': ['dizzy', 'vertigo', 'spinning', 'دوخة', 'دوار', 'عدم توازن']
            },
            'nausea': {
                'en': 'nausea',
                'ar': 'غثيان',
                'severity': 'mild',
                'category': 'gastrointestinal',
                'keywords': ['nausea', 'sick', 'vomit', 'غثيان', 'قيء', 'استفراغ']
            },
            # Respiratory symptoms
            'cough': {
                'en': 'cough',
                'ar': 'سعال',
                'severity': 'mild',
                'category': 'respiratory',
                'keywords': ['cough', 'coughing', 'سعال', 'كحة', 'سعلة']
            },
            'shortness_of_breath': {
                'en': 'shortness of breath',
                'ar': 'ضيق في التنفس',
                'severity': 'moderate',
                'category': 'respiratory',
                'keywords': ['breath', 'breathing', 'shortness', 'dyspnea', 'تنفس', 'ضيق', 'نهجة']
            },
            # General symptoms
            'fever': {
                'en': 'fever',
                'ar': 'حمى',
                'severity': 'moderate',
                'category': 'general',
                'keywords': ['fever', 'temperature', 'hot', 'حمى', 'سخونة', 'حرارة']
            },
            'fatigue': {
                'en': 'fatigue',
                'ar': 'إرهاق',
                'severity': 'mild',
                'category': 'general',
                'keywords': ['tired', 'fatigue', 'exhausted', 'إرهاق', 'تعب', 'إجهاد']
            },
            'chills': {
                'en': 'chills',
                'ar': 'قشعريرة',
                'severity': 'mild',
                'category': 'general',
                'keywords': ['chills', 'shivering', 'cold', 'قشعريرة', 'رعشة', 'برد']
            },
            # Pain symptoms
            'chest_pain': {
                'en': 'chest pain',
                'ar': 'ألم في الصدر',
                'severity': 'severe',
                'category': 'cardiovascular',
                'keywords': ['chest', 'pain', 'heart', 'صدر', 'ألم', 'قلب']
            },
            'abdominal_pain': {
                'en': 'abdominal pain',
                'ar': 'ألم في البطن',
                'severity': 'moderate',
                'category': 'gastrointestinal',
                'keywords': ['stomach', 'belly', 'abdomen', 'pain', 'بطن', 'معدة', 'ألم']
            },
            'back_pain': {
                'en': 'back pain',
                'ar': 'ألم في الظهر',
                'severity': 'moderate',
                'category': 'musculoskeletal',
                'keywords': ['back', 'spine', 'pain', 'ظهر', 'عمود فقري', 'ألم']
            }
        }
        
        # Enhanced disease database with Arabic translations
        self.disease_database = {
            'common_cold': {
                'en': 'Common Cold',
                'ar': 'نزلة برد عادية',
                'symptoms': ['cough', 'fever', 'fatigue', 'headache'],
                'description': {
                    'en': 'A viral infection of the upper respiratory tract',
                    'ar': 'عدوى فيروسية في الجهاز التنفسي العلوي'
                },
                'icd10': 'J00',
                'severity': 'mild'
            },
            'influenza': {
                'en': 'Influenza (Flu)',
                'ar': 'الأنفلونزا',
                'symptoms': ['fever', 'cough', 'fatigue', 'headache', 'chills'],
                'description': {
                    'en': 'A viral infection that attacks the respiratory system',
                    'ar': 'عدوى فيروسية تهاجم الجهاز التنفسي'
                },
                'icd10': 'J11',
                'severity': 'moderate'
            },
            'migraine': {
                'en': 'Migraine',
                'ar': 'الشقيقة',
                'symptoms': ['headache', 'nausea', 'dizziness'],
                'description': {
                    'en': 'A neurological condition characterized by severe headaches',
                    'ar': 'حالة عصبية تتميز بصداع شديد'
                },
                'icd10': 'G43',
                'severity': 'moderate'
            },
            'gastroenteritis': {
                'en': 'Gastroenteritis',
                'ar': 'التهاب المعدة والأمعاء',
                'symptoms': ['nausea', 'abdominal_pain', 'fever', 'fatigue'],
                'description': {
                    'en': 'Inflammation of the stomach and intestines',
                    'ar': 'التهاب في المعدة والأمعاء'
                },
                'icd10': 'K59.1',
                'severity': 'moderate'
            },
            'pneumonia': {
                'en': 'Pneumonia',
                'ar': 'الالتهاب الرئوي',
                'symptoms': ['cough', 'fever', 'shortness_of_breath', 'chest_pain', 'fatigue'],
                'description': {
                    'en': 'Infection that inflames air sacs in one or both lungs',
                    'ar': 'عدوى تسبب التهاب الحويصلات الهوائية في الرئتين'
                },
                'icd10': 'J18',
                'severity': 'severe'
            }
        }
        
        # Red flag symptoms that require immediate medical attention
        self.red_flags = {
            'chest_pain': {
                'en': 'Chest pain can indicate serious heart conditions. Seek immediate medical attention.',
                'ar': 'ألم الصدر قد يشير إلى حالات قلبية خطيرة. اطلب العناية الطبية الفورية.'
            },
            'shortness_of_breath': {
                'en': 'Severe breathing difficulties require immediate medical evaluation.',
                'ar': 'صعوبات التنفس الشديدة تتطلب تقييماً طبياً فورياً.'
            },
            'severe_headache': {
                'en': 'Sudden severe headache may indicate serious neurological conditions.',
                'ar': 'الصداع الشديد المفاجئ قد يشير إلى حالات عصبية خطيرة.'
            }
        }

    def extract_symptoms(self, text: str, language: str = 'en') -> List[Dict[str, Any]]:
        """Extract symptoms from user input text"""
        text_lower = text.lower()
        extracted_symptoms = []
        
        for symptom_key, symptom_data in self.symptom_database.items():
            for keyword in symptom_data['keywords']:
                if keyword.lower() in text_lower:
                    extracted_symptoms.append({
                        'symptom': symptom_data[language],
                        'key': symptom_key,
                        'severity': symptom_data['severity'],
                        'category': symptom_data['category']
                    })
                    break
        
        # Remove duplicates
        seen = set()
        unique_symptoms = []
        for symptom in extracted_symptoms:
            if symptom['key'] not in seen:
                seen.add(symptom['key'])
                unique_symptoms.append(symptom)
        
        return unique_symptoms

    def analyze_potential_conditions(self, symptoms: List[str], language: str = 'en') -> List[Dict[str, Any]]:
        """Analyze potential medical conditions based on symptoms"""
        potential_conditions = []
        
        for condition_key, condition_data in self.disease_database.items():
            matching_symptoms = set(symptoms) & set(condition_data['symptoms'])
            if matching_symptoms:
                probability = len(matching_symptoms) / len(condition_data['symptoms'])
                
                potential_conditions.append({
                    'condition': condition_data[language],
                    'key': condition_key,
                    'probability': probability,
                    'description': condition_data['description'][language],
                    'icd10Code': condition_data['icd10'],
                    'severity': condition_data['severity'],
                    'matching_symptoms': len(matching_symptoms),
                    'total_symptoms': len(condition_data['symptoms'])
                })
        
        # Sort by probability (highest first)
        potential_conditions.sort(key=lambda x: x['probability'], reverse=True)
        
        return potential_conditions[:5]  # Return top 5 matches

    def generate_recommendations(self, symptoms: List[str], conditions: List[Dict], language: str = 'en') -> List[Dict[str, Any]]:
        """Generate medical recommendations based on analysis"""
        recommendations = []
        
        # General recommendations based on language
        general_recs = {
            'en': [
                {
                    'action': 'Monitor your symptoms and track any changes',
                    'type': 'monitoring',
                    'priority': 'medium',
                    'precautions': [
                        'Keep a symptom diary',
                        'Note the time and severity of symptoms',
                        'Record any triggers or patterns'
                    ]
                },
                {
                    'action': 'Stay hydrated and get adequate rest',
                    'type': 'lifestyle',
                    'priority': 'high',
                    'precautions': [
                        'Drink plenty of fluids',
                        'Get 7-8 hours of sleep',
                        'Avoid strenuous activities'
                    ]
                },
                {
                    'action': 'Consult with a healthcare professional for proper diagnosis',
                    'type': 'medical',
                    'priority': 'high',
                    'precautions': [
                        'Schedule an appointment with your doctor',
                        'Bring your symptom diary',
                        'List all medications you are taking'
                    ]
                }
            ],
            'ar': [
                {
                    'action': 'راقب أعراضك وتتبع أي تغييرات',
                    'type': 'monitoring',
                    'priority': 'medium',
                    'precautions': [
                        'احتفظ بمذكرة للأعراض',
                        'سجل وقت وشدة الأعراض',
                        'سجل أي محفزات أو أنماط'
                    ]
                },
                {
                    'action': 'حافظ على الترطيب واحصل على راحة كافية',
                    'type': 'lifestyle',
                    'priority': 'high',
                    'precautions': [
                        'اشرب الكثير من السوائل',
                        'احصل على 7-8 ساعات من النوم',
                        'تجنب الأنشطة الشاقة'
                    ]
                },
                {
                    'action': 'استشر أخصائي رعاية صحية للحصول على تشخيص صحيح',
                    'type': 'medical',
                    'priority': 'high',
                    'precautions': [
                        'حدد موعداً مع طبيبك',
                        'أحضر مذكرة الأعراض',
                        'اذكر جميع الأدوية التي تتناولها'
                    ]
                }
            ]
        }
        
        recommendations.extend(general_recs[language])
        
        # Add specific recommendations based on conditions
        if conditions:
            highest_prob_condition = conditions[0]
            if highest_prob_condition['severity'] == 'severe':
                urgent_rec = {
                    'en': {
                        'action': 'Seek immediate medical attention due to potentially serious condition',
                        'type': 'urgent',
                        'priority': 'critical',
                        'precautions': [
                            'Go to emergency room if symptoms worsen',
                            'Call emergency services if experiencing severe symptoms',
                            'Do not delay medical care'
                        ]
                    },
                    'ar': {
                        'action': 'اطلب العناية الطبية الفورية بسبب حالة محتملة خطيرة',
                        'type': 'urgent',
                        'priority': 'critical',
                        'precautions': [
                            'اذهب إلى غرفة الطوارئ إذا ساءت الأعراض',
                            'اتصل بخدمات الطوارئ إذا كنت تعاني من أعراض شديدة',
                            'لا تؤخر الرعاية الطبية'
                        ]
                    }
                }
                recommendations.insert(0, urgent_rec[language])
        
        return recommendations

    def check_red_flags(self, symptoms: List[str], language: str = 'en') -> List[Dict[str, Any]]:
        """Check for red flag symptoms that require immediate attention"""
        red_flags_found = []
        
        for symptom in symptoms:
            if symptom in self.red_flags:
                red_flags_found.append({
                    'condition': symptom,
                    'action': self.red_flags[symptom][language]
                })
            elif 'chest_pain' in symptom or 'severe' in symptom.lower():
                red_flags_found.append({
                    'condition': symptom,
                    'action': self.red_flags.get('chest_pain', {}).get(language, 
                        'Seek immediate medical attention.' if language == 'en' else 'اطلب العناية الطبية الفورية.')
                })
        
        return red_flags_found

    def analyze_symptoms(self, symptoms_text: str, language: str = 'en', additional_info: Dict = None) -> Dict[str, Any]:
        """Main method to analyze symptoms and return comprehensive results"""
        try:
            # Extract symptoms from text
            extracted_symptoms = self.extract_symptoms(symptoms_text, language)
            
            if not extracted_symptoms:
                # If no symptoms found, provide helpful response instead of error
                fallback_response = {
                    'en': {
                        'message': 'I could not identify specific symptoms from your description. Please try describing your symptoms more specifically, such as "I have a headache and fever" or "I feel nauseous and tired".',
                        'suggestions': [
                            'Use specific symptom names (headache, fever, cough, etc.)',
                            'Describe the location of pain or discomfort',
                            'Mention how long you have been experiencing symptoms',
                            'Include severity (mild, moderate, severe)'
                        ]
                    },
                    'ar': {
                        'message': 'لم أتمكن من تحديد أعراض محددة من وصفك. يرجى محاولة وصف أعراضك بشكل أكثر تحديداً، مثل "أعاني من صداع وحمى" أو "أشعر بالغثيان والتعب".',
                        'suggestions': [
                            'استخدم أسماء أعراض محددة (صداع، حمى، سعال، إلخ)',
                            'اوصف موقع الألم أو عدم الراحة',
                            'اذكر منذ متى تعاني من الأعراض',
                            'اذكر الشدة (خفيف، متوسط، شديد)'
                        ]
                    }
                }
                
                return {
                    'success': True,
                    'extractedSymptoms': [],
                    'potentialDiagnoses': [],
                    'recommendations': [],
                    'redFlags': [],
                    'confidenceScore': 0.0,
                    'helpfulMessage': fallback_response[language]['message'],
                    'suggestions': fallback_response[language]['suggestions'],
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get symptom keys for analysis
            symptom_keys = [s['key'] for s in extracted_symptoms]
            
            # Analyze potential conditions
            potential_conditions = self.analyze_potential_conditions(symptom_keys, language)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(symptom_keys, potential_conditions, language)
            
            # Check for red flags
            red_flags = self.check_red_flags(symptom_keys, language)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(extracted_symptoms, potential_conditions)
            
            return {
                'success': True,
                'extractedSymptoms': extracted_symptoms,
                'potentialDiagnoses': potential_conditions,
                'recommendations': recommendations,
                'redFlags': red_flags,
                'confidenceScore': confidence_score,
                'timestamp': datetime.now().isoformat(),
                'language': language
            }
            
        except Exception as e:
            # Log error but don't expose it to user
            error_message = {
                'en': 'I apologize, but I encountered an issue while analyzing your symptoms. Please try rephrasing your symptoms or contact support if the problem persists.',
                'ar': 'أعتذر، لكنني واجهت مشكلة أثناء تحليل أعراضك. يرجى إعادة صياغة أعراضك أو الاتصال بالدعم إذا استمرت المشكلة.'
            }
            
            return {
                'success': False,
                'error': {
                    'message': error_message[language],
                    'code': 'ANALYSIS_ERROR'
                },
                'timestamp': datetime.now().isoformat()
            }

    def _calculate_confidence(self, symptoms: List[Dict], conditions: List[Dict]) -> float:
        """Calculate confidence score for the analysis"""
        if not symptoms or not conditions:
            return 0.0
        
        # Base confidence on number of symptoms and best match probability
        symptom_factor = min(len(symptoms) / 3, 1.0)  # Normalize to max 3 symptoms
        condition_factor = conditions[0]['probability'] if conditions else 0.0
        
        # Combine factors
        confidence = (symptom_factor * 0.4 + condition_factor * 0.6)
        
        return round(confidence, 2)

    # Legacy method for backward compatibility
    def analyze(self, symptoms_text: str, language: str = 'en', 
                additional_info: Optional[Dict] = None, 
                follow_up_answers: Optional[List] = None) -> Dict[str, Any]:
        """Legacy analyze method for backward compatibility"""
        result = self.analyze_symptoms(symptoms_text, language, additional_info)
        
        # Convert to legacy format
        if result['success']:
            return {
                'extracted_symptoms': result['extractedSymptoms'],
                'potential_diagnoses': result['potentialDiagnoses'],
                'recommendations': result['recommendations'],
                'red_flags': result['redFlags'],
                'confidence_score': result['confidenceScore']
            }
        else:
            raise Exception(result['error']['message'])

