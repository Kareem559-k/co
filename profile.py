from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.medical_user import MedicalUser, db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
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
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
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

@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
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
        
        data = request.get_json()
        
        # Update allowed fields
        if 'firstName' in data:
            user.first_name = data['firstName']
        
        if 'lastName' in data:
            user.last_name = data['lastName']
        
        if 'preferredLanguage' in data:
            if data['preferredLanguage'] in ['en', 'ar']:
                user.preferred_language = data['preferredLanguage']
            else:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid language. Must be "en" or "ar"',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }), 400
        
        if 'dateOfBirth' in data and data['dateOfBirth']:
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
        
        # Update notification preferences
        if 'notificationPreferences' in data:
            prefs = data['notificationPreferences']
            if 'email' in prefs:
                user.email_notifications = bool(prefs['email'])
            if 'sms' in prefs:
                user.sms_notifications = bool(prefs['sms'])
            if 'push' in prefs:
                user.push_notifications = bool(prefs['push'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': 'Profile updated successfully'
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

@profile_bp.route('/profile/password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
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
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('currentPassword') or not data.get('newPassword'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Current password and new password are required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Verify current password
        if not user.check_password(data['currentPassword']):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'AUTHENTICATION_FAILED',
                    'message': 'Current password is incorrect',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 401
        
        # Validate new password
        from src.routes.auth import validate_password
        is_valid, message = validate_password(data['newPassword'])
        if not is_valid:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': message,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Update password
        user.set_password(data['newPassword'])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
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

@profile_bp.route('/profile/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete user account and all associated data"""
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
        
        data = request.get_json()
        
        # Require password confirmation for account deletion
        if not data.get('password'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Password confirmation is required',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 400
        
        # Verify password
        if not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'AUTHENTICATION_FAILED',
                    'message': 'Password is incorrect',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }), 401
        
        # Delete user (cascade will delete related analyses)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
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

