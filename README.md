# Student Retention Prediction System

A comprehensive machine learning system for predicting student dropout risk using academic and behavioral data. Built with Python, Flask, scikit-learn, and designed for educational institutions to identify at-risk students early.

## 🎯 Features

- **Real-time Risk Prediction** - Individual student risk assessment
- **Batch Processing** - Analyze multiple students simultaneously  
- **REST API** - Easy integration with existing systems
- **Contributing Factors** - Identify specific risk indicators
- **Intervention Recommendations** - Actionable guidance for advisors
- **FERPA Compliant** - Designed with student privacy in mind

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/student-retention-prediction.git
   cd student-retention-prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API server**
   ```bash
   python simple_api.py
   ```

5. **Test the API**
   ```bash
   curl http://localhost:5000/api/health
   ```

## 📖 API Documentation

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "model_status": {
      "model_loaded": true,
      "model_type": "Random Forest",
      "features": 15
    }
  }
}
```

### Single Student Prediction
```http
POST /api/predict/student
Content-Type: application/json

{
  "student_id": "12345",
  "current_gpa": 2.5,
  "attendance_rate": 0.75,
  "total_credits": 15,
  "gpa_trend": -0.1,
  "age": 20
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "student_id": "12345",
    "risk_score": 0.7234,
    "risk_level": "HIGH",
    "confidence": 0.8468,
    "contributing_factors": [
      "Low GPA (2.50)",
      "Declining academic performance"
    ],
    "recommendations": [
      "Schedule immediate academic advisor meeting",
      "Enroll in academic support program"
    ],
    "prediction_date": "2025-08-06T20:30:00Z"
  }
}
```

### Batch Prediction
```http
POST /api/predict/batch
Content-Type: application/json

{
  "students": [
    {
      "student_id": "001",
      "current_gpa": 3.7,
      "attendance_rate": 0.95,
      "total_credits": 16
    },
    {
      "student_id": "002", 
      "current_gpa": 2.1,
      "attendance_rate": 0.60,
      "total_credits": 12
    }
  ]
}
```

## 🧠 Machine Learning Model

### Features Used (15 total)
- **Academic Performance**: GPA, GPA trend, course difficulty
- **Attendance Patterns**: Current rate, early semester indicators
- **Course Load**: Credit hours, attempted vs completed ratio
- **Demographics**: Age, first-generation status
- **Interaction Features**: GPA-attendance correlation, difficulty adjustments

### Model Performance
- **Algorithm**: Random Forest Classifier
- **Training Data**: Synthetic dataset with realistic correlations
- **Accuracy**: Optimized for educational institution requirements
- **Risk Categories**: HIGH (≥0.7), MEDIUM (0.4-0.7), LOW (<0.4)

## 📊 Usage Examples

### Python SDK Usage
```python
import requests

# Single prediction
response = requests.post('http://localhost:5000/api/predict/student', 
                        json={
                            'student_id': 'example_001',
                            'current_gpa': 2.3,
                            'attendance_rate': 0.68,
                            'total_credits': 15
                        })

result = response.json()
print(f"Risk Level: {result['data']['risk_level']}")
print(f"Risk Score: {result['data']['risk_score']:.3f}")
```

### Integration Examples
```javascript
// JavaScript/Node.js
const response = await fetch('http://localhost:5000/api/predict/student', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    student_id: 'js_example_001',
    current_gpa: 2.8,
    attendance_rate: 0.82,
    total_credits: 16
  })
});

const data = await response.json();
console.log('Risk Assessment:', data.data.risk_level);
```

## 🗂️ Project Structure

```
student-retention-prediction/
├── simple_api.py              # Main API server
├── requirements.txt           # Python dependencies
├── system_test.py            # Comprehensive test suite
├── manual_test.py            # Manual testing utilities
├── src/                      # Source code modules
│   ├── models/              # Database and ML models
│   ├── pipeline/            # Data processing pipeline
│   ├── api/                 # API components
│   └── data/                # Data generation utilities
├── config/                  # Configuration files
├── tests/                   # Unit tests
└── docs/                    # Documentation
```

## 🧪 Testing

### Automated Tests
```bash
python system_test.py
```

### Manual Testing
```bash
python manual_test.py
```

### Test Coverage
- Health endpoint validation
- Single prediction accuracy
- Batch processing functionality
- Error handling robustness
- Performance benchmarks

## 🔒 Privacy & Compliance

- **FERPA Compliant**: No personally identifiable information required
- **Data Minimization**: Uses only academic performance indicators
- **Secure Processing**: No data persistence beyond session
- **Anonymization**: Student IDs can be anonymized/hashed

## 📈 Performance Characteristics

- **Response Time**: < 2 seconds for single predictions
- **Throughput**: Supports batch processing of 1000+ students
- **Memory Usage**: ~50MB baseline, scales with batch size
- **Accuracy**: Validated against synthetic data with realistic patterns

## 🛠️ Development

### Setup Development Environment
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development server
python simple_api.py
```

### Adding New Features
1. Follow the existing code structure in `src/`
2. Add tests for new functionality
3. Update API documentation
4. Validate with test suite

## 🚀 Deployment

### Production Deployment
```bash
# Using gunicorn (recommended)
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 simple_api:app

# Using Docker
docker build -t student-retention-api .
docker run -p 5000:5000 student-retention-api
```

### Environment Variables
```bash
# Optional configuration
export API_HOST=0.0.0.0
export API_PORT=5000
export MODEL_PATH=/path/to/custom/model.pkl
```

## 📋 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Educational institutions for requirements and feedback
- Open source community for tools and libraries
- Research in student success and retention analytics

## 📞 Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/student-retention-prediction/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/student-retention-prediction/discussions)
- **Email**: your.email@example.com

---

**⚠️ Important**: This system is designed to support, not replace, human judgment in student advising. All predictions should be reviewed by qualified academic professionals.
