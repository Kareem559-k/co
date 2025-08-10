from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.medical_user import MedicalUser, SymptomAnalysis, db
from src.services.symptom_analyzer import SymptomAnalyzer
import uuid

symptoms_bp = Blueprint('symptoms', __name__)

@symptoms_bp.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """Public endpoint for symptom analysis"""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({
                'success': False,
                'error': {
                    'message': 'Symptoms text is required',
                    'code': 'VALIDATION_ERROR'
                }
            }), 400
        
        symptoms_text = data['symptoms']
        language = data.get('language', 'en')
        additional_info = data.get('additional_info', {})
        
        # Initialize the symptom analyzer
        analyzer = SymptomAnalyzer()
        
        # Analyze symptoms using the new method
        result = analyzer.analyze_symptoms(
            symptoms_text=symptoms_text,
            language=language,
            additional_info=additional_info
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'message': 'An error occurred while analyzing symptoms. Please try again.',
                'code': 'ANALYSIS_ERROR'
            }
        }), 500

@symptoms_bp.route('/symptoms', methods=['POST'])
@jwt_required()
def analyze_symptoms_authenticated():
    """Analyze user-provided symptoms (authenticated endpoint)"""
    try:
        current_user_id = get_jwt_identity()
        user = MedicalUser.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': 'User not found',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 404
        
        # Check user consent
        if not user.consent_to_medical_analysis:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'CONSENT_REQUIRED',
                    'message': 'Medical analysis consent is required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 403
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('symptoms'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Symptoms text is required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Validate language
        language = data.get('language', 'en')
        if language not in ['en', 'ar']:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Language must be "en" or "ar"',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Create analysis record
        analysis = SymptomAnalysis(
            user_id=current_user_id,
            symptoms_text=data['symptoms'],
            language=language,
            additional_info=data.get('additionalInfo'),
            follow_up_answers=data.get('followUpAnswers'),
            status='processing'
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        # Initialize symptom analyzer
        analyzer = SymptomAnalyzer()
        
        try:
            # Perform analysis
            result = analyzer.analyze_symptoms(
                symptoms_text=data['symptoms'],
                language=language,
                additional_info=data.get('additionalInfo')
            )
            
            if result['success']:
                # Update analysis with results
                analysis.extracted_symptoms = result.get('extractedSymptoms')
                analysis.potential_diagnoses = result.get('potentialDiagnoses')
                analysis.recommendations = result.get('recommendations')
                analysis.red_flags = result.get('redFlags')
                analysis.confidence_score = result.get('confidenceScore')
                analysis.status = 'completed'
                analysis.completed_at = datetime.utcnow()
                
                db.session.commit()
                
                # Prepare response
                response_data = {
                    'analysisId': analysis.id,
                    'extractedSymptoms': analysis.extracted_symptoms,
                    'potentialDiagnoses': analysis.potential_diagnoses,
                    'recommendations': analysis.recommendations,
                    'redFlags': analysis.red_flags,
                    'medicalDisclaimer': 'This analysis is for informational purposes only and does not replace professional medical advice. Please consult with a healthcare professional for proper diagnosis and treatment.',
                    'confidenceScore': analysis.confidence_score,
                    'analysisTimestamp': analysis.completed_at.isoformat()
                }
                
                return jsonify({
                    'success': True,
                    'data': response_data
                }), 200
            else:
                # Analysis failed
                analysis.status = 'failed'
                db.session.commit()
                return jsonify(result), 422
            
        except Exception as analysis_error:
            # Update analysis status to failed
            analysis.status = 'failed'
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ANALYSIS_FAILED',
                    'message': 'Failed to analyze symptoms. Please try again.',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 422
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 500

@symptoms_bp.route('/symptoms/<analysis_id>', methods=['GET'])
@jwt_required()
def get_symptom_analysis(analysis_id):
    """Get specific symptom analysis results"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find analysis
        analysis = SymptomAnalysis.query.filter_by(
            id=analysis_id,
            user_id=current_user_id
        ).first()
        
        if not analysis:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ANALYSIS_NOT_FOUND',
                    'message': 'Analysis not found',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': analysis.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 500

@symptoms_bp.route('/symptoms/<analysis_id>/feedback', methods=['POST'])
@jwt_required()
def submit_symptom_feedback(analysis_id):
    """Submit feedback for symptom analysis"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find analysis
        analysis = SymptomAnalysis.query.filter_by(
            id=analysis_id,
            user_id=current_user_id
        ).first()
        
        if not analysis:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ANALYSIS_NOT_FOUND',
                    'message': 'Analysis not found',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 404
        
        data = request.get_json()
        
        # Validate feedback data
        feedback = {}
        if 'helpful' in data:
            feedback['helpful'] = bool(data['helpful'])
        if 'accuracy' in data:
            accuracy = data['accuracy']
            if isinstance(accuracy, (int, float)) and 1 <= accuracy <= 5:
                feedback['accuracy'] = accuracy
            else:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Accuracy rating must be between 1 and 5',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }), 400
        if 'comments' in data:
            feedback['comments'] = str(data['comments'])[:1000]  # Limit to 1000 chars
        if 'followedRecommendations' in data:
            feedback['followedRecommendations'] = bool(data['followedRecommendations'])
        if 'soughtMedicalCare' in data:
            feedback['soughtMedicalCare'] = bool(data['soughtMedicalCare'])
        
        feedback['submittedAt'] = datetime.utcnow().isoformat()
        
        # Update analysis with feedback
        analysis.user_feedback = feedback
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 500

