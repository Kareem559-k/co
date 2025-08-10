from flask import Blueprint, jsonify
from datetime import datetime
from src.models.medical_user import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    # Check AI services (placeholder - would check actual AI service endpoints)
    ai_services_status = 'healthy'  # In production, this would ping actual AI services
    
    # Check storage (placeholder)
    storage_status = 'healthy'
    
    overall_status = 'healthy' if all(
        status == 'healthy' for status in [db_status, ai_services_status, storage_status]
    ) else 'unhealthy'
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'database': db_status,
            'aiServices': ai_services_status,
            'storage': storage_status
        },
        'version': '1.0.0'
    }), 200 if overall_status == 'healthy' else 503

@health_bp.route('/status', methods=['GET'])
def system_status():
    """Detailed system status information"""
    try:
        from src.models.medical_user import MedicalUser, SymptomAnalysis, ImageAnalysis
        
        # Get basic statistics
        total_users = MedicalUser.query.count()
        active_users = MedicalUser.query.filter_by(is_active=True).count()
        total_symptom_analyses = SymptomAnalysis.query.count()
        total_image_analyses = ImageAnalysis.query.count()
        
        # Get recent activity (last 24 hours)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_analyses = SymptomAnalysis.query.filter(
            SymptomAnalysis.created_at >= yesterday
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'statistics': {
                    'totalUsers': total_users,
                    'activeUsers': active_users,
                    'totalSymptomAnalyses': total_symptom_analyses,
                    'totalImageAnalyses': total_image_analyses,
                    'recentAnalyses24h': recent_analyses
                },
                'systemInfo': {
                    'version': '1.0.0',
                    'environment': 'development',
                    'uptime': 'N/A',  # Would calculate actual uptime in production
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to retrieve system status',
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 500

