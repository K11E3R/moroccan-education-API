#!/usr/bin/env python3
"""
API Tests for Moroccan Education Public API
"""

import requests
import pytest
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class TestAPI:
    """Test suite for Moroccan Education API"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert "status" in data
        assert data["status"] == "operational"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["data_loaded"] == True
    
    def test_get_all_levels(self):
        """Test getting all education levels"""
        response = requests.get(f"{BASE_URL}/api/v1/levels")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "count" in data
        assert "data" in data
        assert data["count"] > 0
        
        # Check level structure
        level = data["data"][0]
        assert "id" in level
        assert "name" in level
        assert "name_ar" in level
    
    def test_get_specific_level(self):
        """Test getting specific level by ID"""
        # First get all levels
        response = requests.get(f"{BASE_URL}/api/v1/levels")
        levels = response.json()["data"]
        
        if levels:
            level_id = levels[0]["id"]
            response = requests.get(f"{BASE_URL}/api/v1/levels/{level_id}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["data"]["id"] == level_id
    
    def test_get_all_subjects(self):
        """Test getting all subjects"""
        response = requests.get(f"{BASE_URL}/api/v1/subjects")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["count"] > 0
        
        # Check subject structure
        subject = data["data"][0]
        assert "id" in subject
        assert "name" in subject
        assert "name_ar" in subject
        assert "color" in subject
        assert "icon" in subject
    
    def test_filter_subjects_by_level(self):
        """Test filtering subjects by level"""
        response = requests.get(f"{BASE_URL}/api/v1/subjects?level_id=primaire")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        # All subjects should have level_id=primaire
        for subject in data["data"]:
            if subject["level_id"] != "unknown":
                assert subject["level_id"] == "primaire"
    
    def test_get_specific_subject(self):
        """Test getting specific subject by ID"""
        # First get all subjects
        response = requests.get(f"{BASE_URL}/api/v1/subjects")
        subjects = response.json()["data"]
        
        if subjects:
            subject_id = subjects[0]["id"]
            response = requests.get(f"{BASE_URL}/api/v1/subjects/{subject_id}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["data"]["id"] == subject_id
    
    def test_search_french(self):
        """Test search in French"""
        response = requests.get(f"{BASE_URL}/api/v1/search?q=math&language=fr")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "query" in data
        assert "total_results" in data
        assert "results" in data
    
    def test_search_arabic(self):
        """Test search in Arabic"""
        response = requests.get(f"{BASE_URL}/api/v1/search?q=الرياضيات&language=ar")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["total_results"] >= 0
    
    def test_get_stats(self):
        """Test getting API statistics"""
        response = requests.get(f"{BASE_URL}/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        
        stats = data["data"]
        assert "total_items" in stats
        assert "levels_count" in stats
        assert "subjects_count" in stats
        assert "quality_score" in stats
        assert stats["total_items"] > 0
    
    def test_404_not_found(self):
        """Test 404 for non-existent resource"""
        response = requests.get(f"{BASE_URL}/api/v1/levels/nonexistent")
        assert response.status_code == 404
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = requests.get(f"{BASE_URL}/api/v1/levels")
        assert "access-control-allow-origin" in response.headers
    
    def test_response_format(self):
        """Test all endpoints return proper JSON format"""
        endpoints = [
            "/api/v1/levels",
            "/api/v1/subjects",
            "/api/v1/stats",
            "/health"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}")
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/json"
            
            # Should be valid JSON
            data = response.json()
            assert isinstance(data, dict)

def run_tests():
    """Run all tests"""
    print("🧪 Running API Tests...")
    print("="*60)
    
    test = TestAPI()
    tests = [
        ("Root Endpoint", test.test_root_endpoint),
        ("Health Endpoint", test.test_health_endpoint),
        ("Get All Levels", test.test_get_all_levels),
        ("Get Specific Level", test.test_get_specific_level),
        ("Get All Subjects", test.test_get_all_subjects),
        ("Filter Subjects by Level", test.test_filter_subjects_by_level),
        ("Get Specific Subject", test.test_get_specific_subject),
        ("Search French", test.test_search_french),
        ("Search Arabic", test.test_search_arabic),
        ("Get Stats", test.test_get_stats),
        ("404 Not Found", test.test_404_not_found),
        ("CORS Headers", test.test_cors_headers),
        ("Response Format", test.test_response_format),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            failed += 1
    
    print("="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

