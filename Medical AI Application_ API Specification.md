# Medical AI Application: API Specification

## Overview

This document defines the comprehensive API specification for the Medical AI web application. The API follows RESTful principles with JSON request/response formats and implements robust authentication, validation, and error handling mechanisms.

## Base Configuration

**Base URL**: `https://api.medical-ai.com/v1`
**Authentication**: Bearer Token (JWT)
**Content-Type**: `application/json`
**Rate Limiting**: 100 requests per minute per user
**API Version**: v1

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "preferredLanguage": "en|ar",
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1990-01-01",
  "consentToDataProcessing": true,
  "consentToMedicalAnalysis": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid-string",
    "email": "user@example.com",
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 3600
  },
  "message": "User registered successfully"
}
```

### POST /auth/login
Authenticate user and obtain access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid-string",
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 3600,
    "user": {
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "preferredLanguage": "en"
    }
  }
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refreshToken": "refresh-token"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "new-jwt-token",
    "expiresIn": 3600
  }
}
```

### POST /auth/logout
Invalidate current session and tokens.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## User Management Endpoints

### GET /users/profile
Retrieve current user profile information.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid-string",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "preferredLanguage": "en",
    "dateOfBirth": "1990-01-01",
    "createdAt": "2024-01-01T00:00:00Z",
    "lastLoginAt": "2024-01-15T10:30:00Z"
  }
}
```

### PUT /users/profile
Update user profile information.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "preferredLanguage": "ar",
  "notificationPreferences": {
    "email": true,
    "sms": false,
    "push": true
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid-string",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Smith",
    "preferredLanguage": "ar",
    "updatedAt": "2024-01-15T10:35:00Z"
  },
  "message": "Profile updated successfully"
}
```

## Symptom Analysis Endpoints

### POST /analysis/symptoms
Analyze user-provided symptoms and return potential diagnoses.

**Headers:**
```
Authorization: Bearer jwt-token
Content-Type: application/json
```

**Request Body:**
```json
{
  "symptoms": "أعاني من صداع شديد وحمى منذ يومين",
  "language": "ar",
  "additionalInfo": {
    "age": 30,
    "gender": "male",
    "duration": "2 days",
    "severity": "severe",
    "previousConditions": ["diabetes"],
    "currentMedications": ["metformin"]
  },
  "followUpAnswers": [
    {
      "questionId": "q1",
      "answer": "yes"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis-uuid",
    "extractedSymptoms": [
      {
        "symptom": "headache",
        "severity": "severe",
        "duration": "2 days",
        "confidence": 0.95
      },
      {
        "symptom": "fever",
        "severity": "moderate",
        "duration": "2 days",
        "confidence": 0.90
      }
    ],
    "potentialDiagnoses": [
      {
        "condition": "Viral infection",
        "probability": 0.75,
        "confidence": 0.80,
        "severity": "moderate",
        "description": "Common viral infection with fever and headache",
        "icd10Code": "B34.9"
      },
      {
        "condition": "Migraine",
        "probability": 0.60,
        "confidence": 0.70,
        "severity": "moderate",
        "description": "Severe headache disorder",
        "icd10Code": "G43.9"
      }
    ],
    "recommendations": [
      {
        "type": "immediate",
        "action": "Rest and stay hydrated",
        "priority": "high"
      },
      {
        "type": "medication",
        "action": "Consider over-the-counter pain relievers",
        "priority": "medium",
        "precautions": ["Check with doctor if taking other medications"]
      },
      {
        "type": "monitoring",
        "action": "Monitor temperature and symptoms",
        "priority": "high"
      }
    ],
    "redFlags": [
      {
        "condition": "Severe headache with neck stiffness",
        "action": "Seek immediate medical attention",
        "urgency": "emergency"
      }
    ],
    "followUpQuestions": [
      {
        "questionId": "q2",
        "question": "Do you have any neck stiffness?",
        "type": "yes_no",
        "importance": "high"
      }
    ],
    "medicalDisclaimer": "This analysis is for informational purposes only and does not replace professional medical advice.",
    "confidenceScore": 0.78,
    "analysisTimestamp": "2024-01-15T10:40:00Z"
  }
}
```

### GET /analysis/symptoms/{analysisId}
Retrieve specific symptom analysis results.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis-uuid",
    "createdAt": "2024-01-15T10:40:00Z",
    "symptoms": "أعاني من صداع شديد وحمى منذ يومين",
    "language": "ar",
    "extractedSymptoms": [...],
    "potentialDiagnoses": [...],
    "recommendations": [...],
    "followUpStatus": "completed",
    "userFeedback": {
      "helpful": true,
      "accuracy": 4,
      "comments": "Very helpful analysis"
    }
  }
}
```

### POST /analysis/symptoms/{analysisId}/feedback
Provide feedback on symptom analysis results.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Request Body:**
```json
{
  "helpful": true,
  "accuracy": 4,
  "comments": "The analysis was very helpful and accurate",
  "followedRecommendations": true,
  "soughtMedicalCare": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Feedback submitted successfully"
}
```

## Image Analysis Endpoints

### POST /analysis/images/upload
Upload and analyze skin condition image.

**Headers:**
```
Authorization: Bearer jwt-token
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: [binary file data]
metadata: {
  "bodyPart": "face",
  "symptoms": "red rash with itching",
  "duration": "1 week",
  "previousTreatments": ["topical cream"],
  "language": "en"
}
```

**Response (202 Accepted):**
```json
{
  "success": true,
  "data": {
    "analysisId": "image-analysis-uuid",
    "uploadId": "upload-uuid",
    "status": "processing",
    "estimatedCompletionTime": "2024-01-15T10:42:00Z"
  },
  "message": "Image uploaded successfully, analysis in progress"
}
```

### GET /analysis/images/{analysisId}/status
Check the status of image analysis.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analysisId": "image-analysis-uuid",
    "status": "completed",
    "progress": 100,
    "currentStage": "analysis_complete",
    "estimatedTimeRemaining": 0
  }
}
```

### GET /analysis/images/{analysisId}
Retrieve image analysis results.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analysisId": "image-analysis-uuid",
    "imageQuality": {
      "score": 0.85,
      "factors": {
        "sharpness": 0.90,
        "lighting": 0.80,
        "contrast": 0.85,
        "resolution": 0.90
      },
      "recommendations": ["Improve lighting for better analysis"]
    },
    "skinConditionAnalysis": {
      "primaryDiagnosis": {
        "condition": "Eczema",
        "confidence": 0.82,
        "severity": "moderate",
        "description": "Inflammatory skin condition characterized by red, itchy patches",
        "icd10Code": "L30.9"
      },
      "alternativeDiagnoses": [
        {
          "condition": "Contact dermatitis",
          "confidence": 0.65,
          "severity": "mild",
          "description": "Skin reaction to allergens or irritants"
        }
      ],
      "affectedArea": {
        "percentage": 15,
        "location": "face",
        "boundingBox": {
          "x": 120,
          "y": 80,
          "width": 200,
          "height": 150
        }
      }
    },
    "visualExplanation": {
      "heatmapUrl": "https://secure-storage.com/heatmap-uuid.png",
      "annotatedImageUrl": "https://secure-storage.com/annotated-uuid.png",
      "keyFeatures": [
        "Redness and inflammation in central area",
        "Texture changes consistent with eczema",
        "No signs of infection or malignancy"
      ]
    },
    "recommendations": [
      {
        "type": "immediate",
        "action": "Apply gentle, fragrance-free moisturizer",
        "priority": "high"
      },
      {
        "type": "lifestyle",
        "action": "Avoid known triggers and harsh soaps",
        "priority": "medium"
      },
      {
        "type": "medical",
        "action": "Consult dermatologist if symptoms persist",
        "priority": "high"
      }
    ],
    "riskAssessment": {
      "urgency": "low",
      "requiresImmediateAttention": false,
      "monitoringRequired": true,
      "followUpTimeframe": "2 weeks"
    },
    "medicalDisclaimer": "This analysis is for informational purposes only. Consult a healthcare professional for proper diagnosis and treatment.",
    "analysisTimestamp": "2024-01-15T10:42:00Z",
    "modelVersion": "skin-classifier-v2.1",
    "confidenceCalibration": {
      "calibrated": true,
      "method": "temperature_scaling",
      "reliability": 0.88
    }
  }
}
```

### POST /analysis/images/quality-check
Pre-upload image quality assessment.

**Headers:**
```
Authorization: Bearer jwt-token
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: [binary file data]
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "qualityScore": 0.75,
    "qualityFactors": {
      "sharpness": 0.80,
      "lighting": 0.70,
      "contrast": 0.75,
      "resolution": 0.85,
      "anatomicalRelevance": 0.90
    },
    "recommendations": [
      "Improve lighting - avoid shadows",
      "Move slightly closer to the skin area"
    ],
    "acceptable": true,
    "minimumQualityMet": true
  }
}
```

## Analysis History Endpoints

### GET /analysis/history
Retrieve user's analysis history.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Query Parameters:**
```
type: symptoms|images|all (default: all)
limit: number (default: 20, max: 100)
offset: number (default: 0)
startDate: ISO date string
endDate: ISO date string
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analyses": [
      {
        "analysisId": "uuid",
        "type": "symptoms",
        "createdAt": "2024-01-15T10:40:00Z",
        "status": "completed",
        "summary": "Headache and fever analysis",
        "primaryDiagnosis": "Viral infection",
        "confidence": 0.78
      },
      {
        "analysisId": "uuid",
        "type": "image",
        "createdAt": "2024-01-14T15:20:00Z",
        "status": "completed",
        "summary": "Skin condition analysis",
        "primaryDiagnosis": "Eczema",
        "confidence": 0.82
      }
    ],
    "pagination": {
      "total": 45,
      "limit": 20,
      "offset": 0,
      "hasMore": true
    }
  }
}
```

### DELETE /analysis/{analysisId}
Delete specific analysis record.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Analysis deleted successfully"
}
```

## Knowledge Base Endpoints

### GET /knowledge/conditions/{conditionId}
Retrieve detailed information about a specific medical condition.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Query Parameters:**
```
language: en|ar (default: user preference)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "conditionId": "condition-uuid",
    "name": "Eczema",
    "nameArabic": "الأكزيما",
    "description": "Detailed description of the condition",
    "symptoms": ["itching", "redness", "dry skin"],
    "causes": ["genetics", "allergens", "stress"],
    "treatments": [
      {
        "type": "topical",
        "name": "Moisturizers",
        "description": "Regular application of fragrance-free moisturizers"
      }
    ],
    "prevention": ["Avoid triggers", "Use gentle skincare"],
    "whenToSeekCare": ["Severe symptoms", "Signs of infection"],
    "icd10Code": "L30.9",
    "lastUpdated": "2024-01-01T00:00:00Z"
  }
}
```

### GET /knowledge/search
Search medical knowledge base.

**Headers:**
```
Authorization: Bearer jwt-token
```

**Query Parameters:**
```
query: search term
language: en|ar
type: conditions|symptoms|treatments
limit: number (default: 10)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "result-uuid",
        "type": "condition",
        "title": "Eczema",
        "description": "Inflammatory skin condition...",
        "relevanceScore": 0.95
      }
    ],
    "totalResults": 25,
    "searchTime": 0.15
  }
}
```

## System Health and Monitoring

### GET /health
System health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:45:00Z",
  "services": {
    "database": "healthy",
    "aiServices": "healthy",
    "storage": "healthy"
  },
  "version": "1.0.0"
}
```

### GET /metrics
System metrics (admin only).

**Headers:**
```
Authorization: Bearer admin-jwt-token
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "activeUsers": 1250,
    "analysesPerDay": 450,
    "averageResponseTime": 2.3,
    "systemLoad": 0.65,
    "errorRate": 0.02
  }
}
```

## Error Handling

### Standard Error Response Format

All API endpoints return errors in a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "timestamp": "2024-01-15T10:45:00Z",
    "requestId": "req-uuid"
  }
}
```

### Common Error Codes

- `AUTHENTICATION_REQUIRED` (401): Valid authentication token required
- `AUTHORIZATION_FAILED` (403): Insufficient permissions
- `VALIDATION_ERROR` (400): Request validation failed
- `RESOURCE_NOT_FOUND` (404): Requested resource not found
- `RATE_LIMIT_EXCEEDED` (429): Too many requests
- `INTERNAL_SERVER_ERROR` (500): Unexpected server error
- `SERVICE_UNAVAILABLE` (503): Service temporarily unavailable
- `ANALYSIS_FAILED` (422): AI analysis could not be completed
- `IMAGE_QUALITY_INSUFFICIENT` (422): Image quality too low for analysis
- `UNSUPPORTED_LANGUAGE` (400): Language not supported
- `MEDICAL_EMERGENCY_DETECTED` (200): Potential emergency condition identified

## Rate Limiting

The API implements rate limiting to ensure fair usage and system stability:

- **General endpoints**: 100 requests per minute per user
- **Analysis endpoints**: 10 requests per minute per user
- **Upload endpoints**: 5 requests per minute per user
- **Authentication endpoints**: 20 requests per minute per IP

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

## Security Considerations

### Input Validation
- All inputs are validated against strict schemas
- File uploads are scanned for malware
- Image files are validated for format and content
- Text inputs are sanitized to prevent injection attacks

### Data Privacy
- All medical data is encrypted at rest and in transit
- Personal information is anonymized in logs
- User consent is tracked and enforced
- Data retention policies are automatically enforced

### Authentication Security
- JWT tokens have short expiration times
- Refresh tokens are rotated on use
- Failed authentication attempts are logged and monitored
- Multi-factor authentication is supported

This comprehensive API specification provides a robust foundation for the medical AI application, ensuring secure, scalable, and user-friendly access to advanced medical analysis capabilities while maintaining the highest standards of data privacy and medical ethics.

