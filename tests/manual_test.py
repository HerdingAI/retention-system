"""
Manual Test Script - Simple validation of API functionality
"""

import json

def manual_test():
    """Manual test with sample data"""
    print("🧪 Manual API Test")
    print("=" * 40)
    
    # Test data samples
    test_cases = [
        {
            "name": "High Risk Student",
            "data": {
                "student_id": "high_risk_001",
                "current_gpa": 2.0,
                "attendance_rate": 0.55,
                "total_credits": 12,
                "gpa_trend": -0.4
            },
            "expected_risk": "HIGH"
        },
        {
            "name": "Low Risk Student", 
            "data": {
                "student_id": "low_risk_001",
                "current_gpa": 3.8,
                "attendance_rate": 0.95,
                "total_credits": 16,
                "gpa_trend": 0.2
            },
            "expected_risk": "LOW"
        },
        {
            "name": "Medium Risk Student",
            "data": {
                "student_id": "medium_risk_001",
                "current_gpa": 2.7,
                "attendance_rate": 0.78,
                "total_credits": 15,
                "gpa_trend": -0.1
            },
            "expected_risk": "MEDIUM"
        }
    ]
    
    print("📊 Test Cases for Manual Validation:")
    print()
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. {case['name']}:")
        print(f"   Data: {json.dumps(case['data'], indent=6)}")
        print(f"   Expected Risk Level: {case['expected_risk']}")
        print(f"   API Test Command:")
        print(f"   python -c \"")
        print(f"import requests, json")
        print(f"r = requests.post('http://localhost:5000/api/predict/student',")
        print(f"                  json={json.dumps(case['data'])},")
        print(f"                  headers={{'Content-Type': 'application/json'}}")
        print(f"print('Status:', r.status_code)")
        print(f"print('Response:', json.dumps(r.json(), indent=2))\"")
        print()
    
    # Batch test
    batch_data = {
        "students": [case["data"] for case in test_cases]
    }
    
    print("4. Batch Prediction Test:")
    print(f"   Data: {len(batch_data['students'])} students")
    print(f"   API Test Command:")
    print(f"   python -c \"")
    print(f"import requests, json")
    print(f"r = requests.post('http://localhost:5000/api/predict/batch',")
    print(f"                  json={json.dumps(batch_data)},")
    print(f"                  headers={{'Content-Type': 'application/json'}}")
    print(f"print('Status:', r.status_code)")
    print(f"print('Response:', json.dumps(r.json(), indent=2))\"")
    print()
    
    print("🔍 Manual Testing Instructions:")
    print("1. Start the API server: python simple_api.py")
    print("2. In another terminal, run each test command above")
    print("3. Verify that:")
    print("   - High risk student gets risk_score > 0.6")
    print("   - Low risk student gets risk_score < 0.4") 
    print("   - All responses include required fields")
    print("   - Batch processing returns all students")

if __name__ == "__main__":
    manual_test()
