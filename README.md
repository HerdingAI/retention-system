# Student Retention System

A machine learning proof-of-concept for predicting student dropout risk in educational institutions. This system demonstrates how academic and behavioral data can identify at-risk students for early intervention.

## Problem Context

Post-secondary institutions face significant challenges with student retention. Traditional approaches identify struggling students after critical warning signs are missed. This system demonstrates a proactive approach using predictive analytics to flag students who may benefit from early intervention.

**Potential applications:**
- Academic advisor prioritization
- Resource allocation for student success programs
- Early warning systems for registrar offices
- Analytics for institutional research

## System Overview

This is a **demonstration system** built to showcase retention prediction concepts. It includes:
- REST API for single and batch student risk assessment
- Machine learning model using Random Forest classification
- Interactive testing interface
- Complete codebase for institutional adaptation

**Important**: This system uses synthetic training data and is intended as a foundation for institutions to adapt with their own historical data.

## Quick Start

### Prerequisites
- Python 3.8+

### Installation
```bash
git clone <repository-url>
cd student-retention-prediction

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python simple_api.py
```

### Immediate Testing
```bash
# Verify system health
curl http://localhost:5001/api/health

# Test prediction
curl -X POST http://localhost:5001/api/predict/student \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "test_001",
    "current_gpa": 2.3,
    "attendance_rate": 0.68,
    "total_credits": 15
  }'
```

## Data Requirements

### Required Fields
The system expects these minimum fields for each student:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `current_gpa` | Float | Current semester GPA (0.0-4.0) | `2.75` |
| `attendance_rate` | Float | Attendance percentage (0.0-1.0) | `0.85` |
| `total_credits` | Integer | Current semester credit load | `15` |

### Optional Fields (Improve Accuracy)
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `student_id` | String | Unique identifier | `"student_12345"` |
| `gpa_trend` | Float | GPA change from previous semester | `-0.2` |
| `course_difficulty_avg` | Float | Average course difficulty (1.0-5.0) | `3.2` |
| `credits_attempted` | Integer | Total attempted credits | `45` |
| `age` | Integer | Student age | `20` |
| `is_first_generation` | Boolean | First-generation college student | `true` |

### Sample Input Format
```json
{
  "student_id": "student_001",
  "current_gpa": 2.5,
  "attendance_rate": 0.75,
  "total_credits": 15,
  "gpa_trend": -0.1,
  "course_difficulty_avg": 3.0,
  "age": 20,
  "is_first_generation": false
}
```

## API Endpoints

### Health Check
```http
GET /api/health
```
Returns system status and model information.

### Single Student Prediction
```http
POST /api/predict/student
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "data": {
    "student_id": "student_001",
    "risk_score": 0.6234,
    "risk_level": "MEDIUM",
    "confidence": 0.7891,
    "contributing_factors": [
      "Low GPA (2.50)",
      "Declining academic performance"
    ],
    "recommendations": [
      "Monitor attendance closely",
      "Provide study skills resources"
    ],
    "prediction_date": "2025-08-06T20:30:00Z"
  }
}
```

### Batch Processing
```http
POST /api/predict/batch
Content-Type: application/json
```

**Input:**
```json
{
  "students": [
    {"student_id": "001", "current_gpa": 3.7, "attendance_rate": 0.95, "total_credits": 16},
    {"student_id": "002", "current_gpa": 2.1, "attendance_rate": 0.60, "total_credits": 12}
  ]
}
```

## Risk Assessment Logic

### Risk Levels
- **HIGH** (≥0.7): Immediate intervention recommended
- **MEDIUM** (0.4-0.7): Enhanced monitoring suggested  
- **LOW** (<0.4): Standard support protocols

### Contributing Factors
The system identifies specific risk indicators:
- Academic performance (GPA below thresholds)
- Attendance patterns (irregular or declining)
- Course load stress (overloaded or underloaded)
- Performance trends (declining trajectories)

## Interactive Testing

1. Start the API: `python simple_api.py`
2. Open `examples/api_test.html` in your browser
3. Test different student profiles and scenarios

## System Performance

Based on synthetic data testing:
- **Response time**: <2 seconds for single predictions
- **Batch capacity**: 500+ students per request
- **Memory usage**: ~50MB baseline
- **Model accuracy**: Demonstrates expected correlation patterns

**Note**: Performance with real institutional data will vary based on data quality and feature completeness.

## Adapting for Your Institution

### 1. Data Pipeline Integration
```python
# Example: Connect to your SIS
def get_student_data(student_id):
    # Your SIS integration here
    return {
        'current_gpa': fetch_from_sis(student_id, 'gpa'),
        'attendance_rate': calculate_attendance(student_id),
        'total_credits': get_current_credits(student_id)
    }
```

### 2. Model Retraining
```python
# Use your historical data
from scripts.train_model import train_and_save

# Load your institutional data
your_data = load_student_outcomes_data()  # Your implementation
train_and_save(your_data, output_path='institution_model.pkl')
```

### 3. Custom Features
```python
# Add institution-specific features
class InstitutionPredictor(SimplePredictor):
    def engineer_features(self, data):
        features = super().engineer_features(data)
        
        # Add your custom indicators
        features['program_specific_risk'] = calculate_program_risk(data)
        features['financial_aid_status'] = get_aid_indicator(data)
        
        return features
```

## Use Case Examples

### Academic Advisors
```python
# Daily risk assessment workflow
import requests

def daily_risk_check(advisor_students):
    response = requests.post('/api/predict/batch', 
                           json={'students': advisor_students})
    
    high_risk = [s for s in response.json()['data']['predictions'] 
                if s['risk_level'] == 'HIGH']
    
    return high_risk  # Prioritize these for meetings
```

### Registrar Analytics
```python
# Semester-level population analysis
def analyze_semester_cohort():
    all_students = get_enrolled_students()
    predictions = batch_predict_students(all_students)
    
    return {
        'total_at_risk': count_high_risk(predictions),
        'by_program': group_by_program(predictions),
        'intervention_candidates': filter_actionable_cases(predictions)
    }
```

## Privacy Considerations

- **FIPPA Compliance**: System designed for FERPA privacy regulations
- **Minimal Data**: Works with academic data only, no personal identifiers required
- **No Persistence**: Student data not stored beyond session scope
- **Anonymization Ready**: Student IDs can be hashed or tokenized

## Technical Architecture

### Model Details
- **Algorithm**: Random Forest (100 estimators, max depth 8)
- **Features**: 15 engineered features from academic and behavioral data
- **Training**: Synthetic dataset with realistic educational correlations
- **Validation**: Cross-validation on demonstration data

### Code Structure
```
student-retention-prediction/
├── simple_api.py              # Main API server
├── simple_model.pkl           # Trained model
├── requirements.txt           # Dependencies
├── examples/api_test.html     # Interactive testing
├── tests/system_test.py       # Automated validation
└── scripts/                   # Training utilities
```

## Deployment Options

### Development
```bash
python simple_api.py --port 5001 --debug
```

### Production
```bash
# Using deployment script
python deploy.py --nginx --systemd --port 5001

# Or with gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5001 simple_api:app
```

### Docker
```bash
docker build -t retention-prediction .
docker run -p 5001:5001 retention-prediction
```

## Validation and Testing

### Automated Tests
```bash
python tests/system_test.py
```
Validates API functionality, error handling, and performance.

### Manual Testing
```bash
python tests/manual_test.py
```
Provides test cases and sample data for validation.

## Limitations and Considerations

### Current Limitations
- **Synthetic training data**: Requires retraining with institutional data for production use
- **Feature assumptions**: Some features may not be readily available in all SIS platforms
- **No real-time streaming**: Designed for batch and on-demand processing

### Implementation Considerations
- **Data quality**: Predictions accuracy depends on clean, consistent input data
- **Historical validation**: Test against past student outcomes before deployment
- **Advisor training**: Staff need training on interpreting and acting on predictions
- **Continuous monitoring**: Model performance should be monitored over time

## Contributing and Support

This system is provided as an open foundation for institutional adaptation. Key areas for enhancement:
- Institution-specific feature engineering
- Real data model training and validation
- Integration with specific SIS platforms
- Advanced analytics and reporting interfaces

**License**: MIT License - suitable for institutional use and modification.

---

**Built for Ontario educational institutions seeking to implement predictive analytics for student success.**
