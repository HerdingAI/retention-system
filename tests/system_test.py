"""
Comprehensive System Test Suite
Tests all functionality and generates reports for GitHub preparation
"""

import requests
import json
import time
import sys
from datetime import datetime

class StudentRetentionAPITester:
    """Comprehensive API testing class"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
    
    def log_test(self, test_name, passed, details=None, response_data=None):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = {
            "test_name": test_name,
            "status": status,
            "passed": passed,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} - {test_name}")
        if details:
            print(f"      {details}")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("\n🔍 Testing Health Check Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                model_loaded = data.get('data', {}).get('model_status', {}).get('model_loaded', False)
                
                if model_loaded:
                    self.log_test(
                        "Health Check - Model Loaded", 
                        True, 
                        f"Status: {response.status_code}, Model: Loaded",
                        data
                    )
                else:
                    self.log_test(
                        "Health Check - Model Status", 
                        False, 
                        "Model not loaded properly"
                    )
            else:
                self.log_test(
                    "Health Check - HTTP Status", 
                    False, 
                    f"Expected 200, got {response.status_code}"
                )
                
        except requests.exceptions.ConnectionError:
            self.log_test(
                "Health Check - Connection", 
                False, 
                "Cannot connect to API server"
            )
        except Exception as e:
            self.log_test(
                "Health Check - General", 
                False, 
                f"Unexpected error: {str(e)}"
            )
    
    def test_single_prediction_basic(self):
        """Test single student prediction with basic data"""
        print("\n🎯 Testing Single Student Prediction (Basic)...")
        
        test_student = {
            "student_id": "test_001_basic",
            "current_gpa": 2.5,
            "attendance_rate": 0.75,
            "total_credits": 15
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/predict/student",
                json=test_student,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('data', {})
                
                # Validate required fields
                required_fields = ['risk_score', 'risk_level', 'confidence', 'contributing_factors', 'recommendations']
                missing_fields = [f for f in required_fields if f not in prediction]
                
                if not missing_fields:
                    # Validate data types and ranges
                    valid_data = True
                    risk_score = prediction.get('risk_score', 0)
                    confidence = prediction.get('confidence', 0)
                    
                    if not (0 <= risk_score <= 1):
                        valid_data = False
                    if not (0 <= confidence <= 1):
                        valid_data = False
                    if prediction.get('risk_level') not in ['HIGH', 'MEDIUM', 'LOW']:
                        valid_data = False
                    
                    if valid_data:
                        self.log_test(
                            "Single Prediction - Basic Data",
                            True,
                            f"Risk: {prediction['risk_level']} ({risk_score:.3f}), Confidence: {confidence:.3f}",
                            prediction
                        )
                    else:
                        self.log_test(
                            "Single Prediction - Data Validation",
                            False,
                            "Invalid data ranges or types in response"
                        )
                else:
                    self.log_test(
                        "Single Prediction - Response Format",
                        False,
                        f"Missing fields: {missing_fields}"
                    )
            else:
                self.log_test(
                    "Single Prediction - HTTP Status",
                    False,
                    f"Expected 200, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Single Prediction - Basic Test",
                False,
                f"Request failed: {str(e)}"
            )
    
    def test_single_prediction_comprehensive(self):
        """Test single student prediction with comprehensive data"""
        print("\n📊 Testing Single Student Prediction (Comprehensive)...")
        
        test_student = {
            "student_id": "test_002_comprehensive",
            "current_gpa": 2.1,
            "attendance_rate": 0.65,
            "total_credits": 16,
            "course_difficulty_avg": 3.2,
            "gpa_trend": -0.3,
            "credits_attempted": 48,
            "age": 22,
            "is_first_generation": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/predict/student",
                json=test_student,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('data', {})
                
                # Should detect high risk based on low GPA and attendance
                risk_score = prediction.get('risk_score', 0)
                contributing_factors = prediction.get('contributing_factors', [])
                
                # Check if system correctly identifies risk factors
                risk_detected = risk_score > 0.5  # Should be higher risk
                factors_identified = len(contributing_factors) > 0
                
                self.log_test(
                    "Single Prediction - Comprehensive Data",
                    risk_detected and factors_identified,
                    f"Risk Score: {risk_score:.3f}, Factors: {len(contributing_factors)}",
                    prediction
                )
            else:
                self.log_test(
                    "Single Prediction - Comprehensive HTTP",
                    False,
                    f"Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Single Prediction - Comprehensive Test",
                False,
                f"Request failed: {str(e)}"
            )
    
    def test_batch_prediction(self):
        """Test batch student predictions"""
        print("\n📦 Testing Batch Student Predictions...")
        
        batch_students = {
            "students": [
                {
                    "student_id": "batch_001",
                    "current_gpa": 3.7,
                    "attendance_rate": 0.95,
                    "total_credits": 15,
                    "age": 19
                },
                {
                    "student_id": "batch_002",
                    "current_gpa": 2.0,
                    "attendance_rate": 0.55,
                    "total_credits": 12,
                    "gpa_trend": -0.5,
                    "age": 23
                },
                {
                    "student_id": "batch_003",
                    "current_gpa": 2.8,
                    "attendance_rate": 0.82,
                    "total_credits": 18,
                    "age": 20
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/predict/batch",
                json=batch_students,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                batch_result = data.get('data', {})
                predictions = batch_result.get('predictions', [])
                
                if len(predictions) == 3:
                    # Validate that different students get different risk levels
                    risk_levels = [p.get('risk_level') for p in predictions]
                    unique_levels = len(set(risk_levels))
                    
                    # Student 1 should be low risk, student 2 should be high risk
                    first_student_risk = predictions[0].get('risk_score', 0)
                    second_student_risk = predictions[1].get('risk_score', 0)
                    
                    logical_ranking = first_student_risk < second_student_risk
                    
                    self.log_test(
                        "Batch Prediction - Processing",
                        True,
                        f"Processed {len(predictions)} students, {unique_levels} risk levels",
                        batch_result
                    )
                    
                    self.log_test(
                        "Batch Prediction - Risk Logic",
                        logical_ranking,
                        f"Low-risk student: {first_student_risk:.3f}, High-risk student: {second_student_risk:.3f}"
                    )
                else:
                    self.log_test(
                        "Batch Prediction - Count",
                        False,
                        f"Expected 3 predictions, got {len(predictions)}"
                    )
            else:
                self.log_test(
                    "Batch Prediction - HTTP Status",
                    False,
                    f"Status: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Batch Prediction - Request",
                False,
                f"Request failed: {str(e)}"
            )
    
    def test_error_handling(self):
        """Test API error handling"""
        print("\n🛡️ Testing Error Handling...")
        
        # Test missing required fields
        try:
            response = requests.post(
                f"{self.base_url}/api/predict/student",
                json={"student_id": "incomplete"},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 400:
                data = response.json()
                error_present = not data.get('success', True)
                
                self.log_test(
                    "Error Handling - Missing Fields",
                    error_present,
                    f"Correctly returned 400 status"
                )
            else:
                self.log_test(
                    "Error Handling - Missing Fields",
                    False,
                    f"Expected 400, got {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Missing Fields Test",
                False,
                f"Test failed: {str(e)}"
            )
        
        # Test invalid JSON
        try:
            response = requests.post(
                f"{self.base_url}/api/predict/student",
                data="invalid json",
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            error_status = response.status_code >= 400
            self.log_test(
                "Error Handling - Invalid JSON",
                error_status,
                f"Status: {response.status_code}"
            )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Invalid JSON Test",
                False,
                f"Test failed: {str(e)}"
            )
    
    def test_performance(self):
        """Test API performance"""
        print("\n⚡ Testing API Performance...")
        
        test_student = {
            "student_id": "perf_test",
            "current_gpa": 3.0,
            "attendance_rate": 0.85,
            "total_credits": 15
        }
        
        # Test response time
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/predict/student",
                json=test_student,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200 and response_time < 2000:  # Under 2 seconds
                self.log_test(
                    "Performance - Response Time",
                    True,
                    f"Response time: {response_time:.0f}ms"
                )
            else:
                self.log_test(
                    "Performance - Response Time",
                    False,
                    f"Too slow: {response_time:.0f}ms or failed request"
                )
                
        except Exception as e:
            self.log_test(
                "Performance - Response Time Test",
                False,
                f"Test failed: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive System Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        self.test_health_endpoint()
        self.test_single_prediction_basic()
        self.test_single_prediction_comprehensive()
        self.test_batch_prediction()
        self.test_error_handling()
        self.test_performance()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Generate summary report
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        print(f"Total Time: {total_time:.2f} seconds")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r['passed']]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   - {test['test_name']}: {test['details']}")
        
        # Show sample successful predictions
        successful_predictions = [r for r in self.test_results if r['passed'] and r['response_data']]
        if successful_predictions:
            print(f"\n✅ SAMPLE PREDICTIONS:")
            for i, test in enumerate(successful_predictions[:2]):
                if 'risk_score' in str(test['response_data']):
                    data = test['response_data']
                    print(f"   {i+1}. {test['test_name']}:")
                    print(f"      Risk Level: {data.get('risk_level', 'N/A')}")
                    print(f"      Risk Score: {data.get('risk_score', 'N/A'):.3f}")
                    print(f"      Confidence: {data.get('confidence', 'N/A'):.3f}")
        
        print("\n🎯 SYSTEM STATUS:")
        if self.passed_tests == self.total_tests:
            print("   ✅ ALL TESTS PASSED - System ready for GitHub!")
        elif self.passed_tests / self.total_tests >= 0.8:
            print("   🟡 MOSTLY FUNCTIONAL - Minor issues to address")
        else:
            print("   ❌ SIGNIFICANT ISSUES - Needs debugging")
        
        return self.passed_tests == self.total_tests

def main():
    """Main test execution"""
    print("🧪 Student Retention Prediction API - System Test")
    print("Testing API at http://localhost:5000")
    print("Make sure the API server is running: python simple_api.py")
    print("")
    
    tester = StudentRetentionAPITester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
