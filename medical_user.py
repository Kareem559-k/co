from src.models.user import db
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class MedicalUser(db.Model):
    __tablename__ = 'medical_users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    preferred_language = db.Column(db.String(5), default='en', nullable=False)  # 'en' or 'ar'
    date_of_birth = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Consent tracking
    consent_to_data_processing = db.Column(db.Boolean, default=False, nullable=False)
    consent_to_medical_analysis = db.Column(db.Boolean, default=False, nullable=False)
    consent_date = db.Column(db.DateTime, nullable=True)
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    sms_notifications = db.Column(db.Boolean, default=False, nullable=False)
    push_notifications = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    symptom_analyses = db.relationship('SymptomAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    image_analyses = db.relationship('ImageAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<MedicalUser {self.email}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'preferredLanguage': self.preferred_language,
            'dateOfBirth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'createdAt': self.created_at.isoformat(),
            'lastLoginAt': self.last_login_at.isoformat() if self.last_login_at else None,
            'isActive': self.is_active,
            'consentToDataProcessing': self.consent_to_data_processing,
            'consentToMedicalAnalysis': self.consent_to_medical_analysis,
            'consentDate': self.consent_date.isoformat() if self.consent_date else None,
            'notificationPreferences': {
                'email': self.email_notifications,
                'sms': self.sms_notifications,
                'push': self.push_notifications
            }
        }
        
        if include_sensitive:
            data['passwordHash'] = self.password_hash
            
        return data

    @staticmethod
    def create_user(email, password, first_name=None, last_name=None, 
                   preferred_language='en', consent_to_data_processing=False,
                   consent_to_medical_analysis=False):
        """Create a new user"""
        user = MedicalUser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            preferred_language=preferred_language,
            consent_to_data_processing=consent_to_data_processing,
            consent_to_medical_analysis=consent_to_medical_analysis,
            consent_date=datetime.utcnow() if (consent_to_data_processing or consent_to_medical_analysis) else None
        )
        user.set_password(password)
        return user


class SymptomAnalysis(db.Model):
    __tablename__ = 'symptom_analyses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('medical_users.id'), nullable=False)
    
    # Input data
    symptoms_text = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(5), nullable=False)
    additional_info = db.Column(db.JSON, nullable=True)  # Age, gender, duration, etc.
    
    # Analysis results
    extracted_symptoms = db.Column(db.JSON, nullable=True)
    potential_diagnoses = db.Column(db.JSON, nullable=True)
    recommendations = db.Column(db.JSON, nullable=True)
    red_flags = db.Column(db.JSON, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)
    
    # Status and metadata
    status = db.Column(db.String(20), default='processing', nullable=False)  # processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Follow-up
    follow_up_questions = db.Column(db.JSON, nullable=True)
    follow_up_answers = db.Column(db.JSON, nullable=True)
    
    # User feedback
    user_feedback = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<SymptomAnalysis {self.id}>'

    def to_dict(self):
        return {
            'analysisId': self.id,
            'userId': self.user_id,
            'symptomsText': self.symptoms_text,
            'language': self.language,
            'additionalInfo': self.additional_info,
            'extractedSymptoms': self.extracted_symptoms,
            'potentialDiagnoses': self.potential_diagnoses,
            'recommendations': self.recommendations,
            'redFlags': self.red_flags,
            'confidenceScore': self.confidence_score,
            'status': self.status,
            'createdAt': self.created_at.isoformat(),
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'followUpQuestions': self.follow_up_questions,
            'followUpAnswers': self.follow_up_answers,
            'userFeedback': self.user_feedback
        }


class ImageAnalysis(db.Model):
    __tablename__ = 'image_analyses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('medical_users.id'), nullable=False)
    
    # Image data
    image_path = db.Column(db.String(255), nullable=False)
    image_metadata = db.Column(db.JSON, nullable=True)  # Body part, symptoms, etc.
    
    # Quality assessment
    image_quality = db.Column(db.JSON, nullable=True)
    
    # Analysis results
    skin_condition_analysis = db.Column(db.JSON, nullable=True)
    visual_explanation = db.Column(db.JSON, nullable=True)
    recommendations = db.Column(db.JSON, nullable=True)
    risk_assessment = db.Column(db.JSON, nullable=True)
    
    # Status and metadata
    status = db.Column(db.String(20), default='processing', nullable=False)  # processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Model information
    model_version = db.Column(db.String(50), nullable=True)
    confidence_calibration = db.Column(db.JSON, nullable=True)
    
    # User feedback
    user_feedback = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<ImageAnalysis {self.id}>'

    def to_dict(self):
        return {
            'analysisId': self.id,
            'userId': self.user_id,
            'imagePath': self.image_path,
            'imageMetadata': self.image_metadata,
            'imageQuality': self.image_quality,
            'skinConditionAnalysis': self.skin_condition_analysis,
            'visualExplanation': self.visual_explanation,
            'recommendations': self.recommendations,
            'riskAssessment': self.risk_assessment,
            'status': self.status,
            'createdAt': self.created_at.isoformat(),
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'modelVersion': self.model_version,
            'confidenceCalibration': self.confidence_calibration,
            'userFeedback': self.user_feedback
        }

