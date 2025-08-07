"""
Standalone API Server for Student Retention Prediction
Simple, functional, and reliable API with minimal dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
from datetime import datetime
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Simple prediction model
class SimplePredictor:
    """Simple student risk predictor"""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'current_gpa', 'attendance_rate', 'total_credits', 'gpa_trend',
            'attendance_gpa_interaction', 'gpa_difficulty_interaction',
            'course_difficulty_avg', 'credits_attempted', 'credit_load_status',
            'gpa_status', 'attendance_status', 'academic_progress_rate',
            'risk_factor_count', 'age', 'is_first_generation'
        ]
        self._create_model()
    
    def _create_model(self):
        """Create a simple demonstration model"""
        try:
            # Try to load existing model
            if os.path.exists('simple_model.pkl'):
                with open('simple_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("Loaded existing simple model")
                return
            
            # Create new model
            logger.info("Creating simple demonstration model...")
            
            # Generate synthetic training data
            np.random.seed(42)
            n_samples = 1000
            n_features = len(self.feature_names)
            
            # Create correlated features
            X = np.random.randn(n_samples, n_features)
            
            # Create risk labels with realistic correlations
            risk_scores = (
                -X[:, 0] * 0.4 +  # Lower GPA = higher risk
                -X[:, 1] * 0.3 +  # Lower attendance = higher risk
                X[:, 12] * 0.2 +  # More risk factors = higher risk
                np.random.randn(n_samples) * 0.3
            )
            y = (risk_scores > 0).astype(int)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=50,
                max_depth=8,
                random_state=42
            )
            self.model.fit(X, y)
            
            # Save model
            with open('simple_model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            
            logger.info("Simple model created and saved")
            
        except Exception as e:
            logger.error(f"Model creation failed: {str(e)}")
            self.model = None
    
    def engineer_features(self, data):
        """Engineer features from student data"""
        try:
            # Handle different input types
            if isinstance(data, dict):
                # Single student - convert to DataFrame
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                # Multiple students - convert to DataFrame
                df = pd.DataFrame(data)
            else:
                # Already a DataFrame
                df = data.copy()
            
            features = pd.DataFrame(index=df.index)
            
            # Helper function to safely get column values with defaults
            def safe_get(column_name, default_value):
                if column_name in df.columns:
                    return df[column_name].fillna(default_value)
                else:
                    return pd.Series([default_value] * len(df), index=df.index)
            
            # Basic features with defaults
            features['current_gpa'] = safe_get('current_gpa', 2.5)
            features['attendance_rate'] = safe_get('attendance_rate', 0.8)
            features['total_credits'] = safe_get('total_credits', 15)
            features['gpa_trend'] = safe_get('gpa_trend', 0.0)
            
            # Interaction features
            features['attendance_gpa_interaction'] = (
                features['attendance_rate'] * features['current_gpa']
            )
            
            course_difficulty = safe_get('course_difficulty_avg', 3.0)
            features['course_difficulty_avg'] = course_difficulty
            features['gpa_difficulty_interaction'] = (
                features['current_gpa'] / (course_difficulty + 0.1)
            )
            
            # More features
            features['credits_attempted'] = safe_get('credits_attempted', 45)
            features['credit_load_status'] = np.where(features['total_credits'] >= 15, 1, 0)
            features['gpa_status'] = np.where(features['current_gpa'] >= 3.0, 1, 0)
            features['attendance_status'] = np.where(features['attendance_rate'] >= 0.8, 1, 0)
            features['academic_progress_rate'] = features['current_gpa'] * features['attendance_rate']
            
            # Risk factors
            risk_count = (
                (features['current_gpa'] < 2.5).astype(int) +
                (features['attendance_rate'] < 0.7).astype(int) +
                (features['total_credits'] > 18).astype(int)
            )
            features['risk_factor_count'] = risk_count
            
            # Demographics
            features['age'] = safe_get('age', 20)
            features['is_first_generation'] = safe_get('is_first_generation', False).astype(int)
            
            # Ensure all expected features are present and in correct order
            expected_features = self.feature_names
            for feature in expected_features:
                if feature not in features.columns:
                    features[feature] = 0.0
            
            return features[expected_features].fillna(0.0)
            
        except Exception as e:
            logger.error(f"Feature engineering failed: {str(e)}")
            raise
    
    def predict(self, data):
        """Make risk prediction"""
        try:
            if self.model is None:
                raise ValueError("Model not available")
            
            # Engineer features
            features = self.engineer_features(data)
            
            # Make prediction
            risk_probabilities = self.model.predict_proba(features)[:, 1]
            risk_score = float(risk_probabilities[0])
            
            # Determine risk level
            if risk_score >= 0.7:
                risk_level = "HIGH"
            elif risk_score >= 0.4:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            # Calculate confidence
            confidence = min(abs(risk_score - 0.5) * 2, 1.0)
            
            # Generate factors and recommendations
            factors = self._get_factors(features.iloc[0], risk_score)
            recommendations = self._get_recommendations(risk_level, factors)
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'confidence': confidence,
                'contributing_factors': factors,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def _get_factors(self, features, risk_score):
        """Get contributing factors"""
        factors = []
        
        if features['current_gpa'] < 2.5:
            factors.append(f"Low GPA ({features['current_gpa']:.2f})")
        
        if features['attendance_rate'] < 0.7:
            factors.append(f"Poor attendance ({features['attendance_rate']:.1%})")
        
        if features['total_credits'] > 18:
            factors.append(f"Heavy course load ({features['total_credits']} credits)")
        
        if features['gpa_trend'] < -0.1:
            factors.append("Declining academic performance")
        
        if not factors:
            factors.append("Multiple minor risk indicators")
        
        return factors[:3]
    
    def _get_recommendations(self, risk_level, factors):
        """Get intervention recommendations"""
        if risk_level == "HIGH":
            return [
                "Schedule immediate academic advisor meeting",
                "Enroll in academic support program",
                "Consider course load reduction"
            ]
        elif risk_level == "MEDIUM":
            return [
                "Monitor attendance closely",
                "Provide study skills resources",
                "Schedule regular check-ins"
            ]
        else:
            return [
                "Continue regular monitoring",
                "Maintain current support level"
            ]

# Initialize predictor
predictor = SimplePredictor()

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "success": True,
            "data": {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": "1.0.0-simple",
                "model_status": {
                    "model_loaded": predictor.model is not None,
                    "model_type": "Simple Random Forest",
                    "features": len(predictor.feature_names)
                },
                "endpoints": [
                    "GET /api/health",
                    "POST /api/predict/student",
                    "POST /api/predict/batch"
                ]
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "message": "Health check failed",
                "code": "HEALTH_CHECK_FAILED",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }), 503

@app.route('/api/predict/student', methods=['POST'])
def predict_student():
    """Predict risk for single student"""
    try:
        if not request.json:
            return jsonify({
                "success": False,
                "error": {
                    "message": "Request body must be JSON",
                    "code": "INVALID_REQUEST",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }), 400
        
        # Validate required fields
        required = ['current_gpa', 'attendance_rate', 'total_credits']
        missing = [f for f in required if f not in request.json]
        
        if missing:
            return jsonify({
                "success": False,
                "error": {
                    "message": f"Missing required fields: {', '.join(missing)}",
                    "code": "MISSING_FIELDS",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }), 400
        
        # Make prediction
        result = predictor.predict(request.json)
        
        response_data = {
            "student_id": request.json.get('student_id', 'unknown'),
            "risk_score": round(result['risk_score'], 4),
            "risk_level": result['risk_level'],
            "confidence": round(result['confidence'], 4),
            "contributing_factors": result['contributing_factors'],
            "recommendations": result['recommendations'],
            "prediction_date": datetime.utcnow().isoformat() + "Z"
        }
        
        return jsonify({
            "success": True,
            "data": response_data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error(f"Single prediction failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": {
                "message": "Prediction failed",
                "code": "PREDICTION_ERROR",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }), 500

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Predict risk for multiple students"""
    try:
        if not request.json:
            return jsonify({
                "success": False,
                "error": {
                    "message": "Request body must be JSON",
                    "code": "INVALID_REQUEST",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }), 400
        
        # Handle different input formats
        if 'students' in request.json:
            students_data = request.json['students']
        elif isinstance(request.json, list):
            students_data = request.json
        else:
            return jsonify({
                "success": False,
                "error": {
                    "message": "Expected 'students' array or direct array",
                    "code": "INVALID_FORMAT",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }), 400
        
        if not isinstance(students_data, list) or len(students_data) == 0:
            return jsonify({
                "success": False,
                "error": {
                    "message": "Students data must be non-empty array",
                    "code": "INVALID_DATA",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }), 400
        
        # Make predictions
        predictions = []
        for i, student_data in enumerate(students_data):
            try:
                result = predictor.predict(student_data)
                predictions.append({
                    "student_id": student_data.get('student_id', f'student_{i+1}'),
                    "risk_score": round(result['risk_score'], 4),
                    "risk_level": result['risk_level'],
                    "confidence": round(result['confidence'], 4),
                    "contributing_factors": result['contributing_factors'],
                    "recommendations": result['recommendations']
                })
            except Exception as e:
                logger.error(f"Failed to predict for student {i}: {str(e)}")
                predictions.append({
                    "student_id": student_data.get('student_id', f'student_{i+1}'),
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "data": {
                "predictions": predictions,
                "total_students": len(predictions),
                "batch_processed_at": datetime.utcnow().isoformat() + "Z"
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": {
                "message": "Batch prediction failed",
                "code": "BATCH_ERROR",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": {
            "message": "Endpoint not found",
            "code": "NOT_FOUND",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": {
            "message": "Internal server error",
            "code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Student Retention Prediction API')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5001, help='Port to bind to (default: 5001)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting Simple Student Retention Prediction API")
    logger.info("📊 Available Endpoints:")
    logger.info("  GET  /api/health          - API health status")
    logger.info("  POST /api/predict/student - Single student prediction")
    logger.info("  POST /api/predict/batch   - Batch student predictions")
    logger.info("")
    logger.info(f"🔗 Server: http://{args.host}:{args.port}")
    logger.info("📝 Sample Request:")
    logger.info(f"  curl -X POST http://{args.host}:{args.port}/api/predict/student \\")
    logger.info("       -H 'Content-Type: application/json' \\")
    logger.info("       -d '{\"current_gpa\": 2.5, \"attendance_rate\": 0.75, \"total_credits\": 15}'")
    
    try:
        app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        print(f"❌ Server startup failed: {e}")
        print("💡 Try checking for port conflicts or firewall issues")
