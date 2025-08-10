from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
from src.models.medical_user import MedicalUser, db
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'consentToDataProcessing', 'consentToMedicalAnalysis']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'Missing required field: {field}',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid email format',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Validate password
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': message,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Check if user already exists
        existing_user = MedicalUser.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_EXISTS',
                    'message': 'User with this email already exists',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 409
        
        # Validate consent
        if not data['consentToDataProcessing'] or not data['consentToMedicalAnalysis']:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'CONSENT_REQUIRED',
                    'message': 'Both data processing and medical analysis consent are required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Create new user
        user = MedicalUser.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            preferred_language=data.get('preferredLanguage', 'en'),
            consent_to_data_processing=data['consentToDataProcessing'],
            consent_to_medical_analysis=data['consentToMedicalAnalysis']
        )
        
        # Set date of birth if provided
        if data.get('dateOfBirth'):
            try:
                user.date_of_birth = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid date format. Use YYYY-MM-DD',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }), 400
        
        # Save user to database
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'userId': user.id,
                'email': user.email,
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'expiresIn': 3600
            },
            'message': 'User registered successfully'
        }), 201
        
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

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return tokens"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email and password are required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Find user
        user = MedicalUser.query.filter_by(email=data['email']).first()
        
        # Check credentials
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'AUTHENTICATION_FAILED',
                    'message': 'Invalid email or password',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ACCOUNT_DISABLED',
                    'message': 'Account has been disabled',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 403
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'userId': user.id,
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'expiresIn': 3600,
                'user': {
                    'email': user.email,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'preferredLanguage': user.preferred_language
                }
            }
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

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user still exists and is active
        user = MedicalUser.query.get(current_user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': 'User not found or inactive',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 404
        
        # Create new access token
        access_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            'success': True,
            'data': {
                'accessToken': access_token,
                'expiresIn': 3600
            }
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

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (in a real implementation, you'd blacklist the token)"""
    try:
        # In a production environment, you would add the token to a blacklist
        # For now, we'll just return a success message
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
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

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if the current token is valid"""
    try:
        current_user_id = get_jwt_identity()
        user = MedicalUser.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': 'User not found or inactive',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'userId': user.id,
                'email': user.email,
                'isValid': True
            }
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

