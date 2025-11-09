"""
Test script for Travel Journal Hub
Verifies that the Flask app is properly configured
"""

import sys
import os

# Set USE_SQLITE to avoid MySQL connection requirement during tests
os.environ['USE_SQLITE'] = 'true'

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import flask
        from flask import Flask, render_template, request, jsonify
        from flask_cors import CORS
        print("✓ All required Flask modules imported successfully")
        
        # Test optional MySQL import
        try:
            import mysql.connector
            print("✓ MySQL connector available")
        except ImportError:
            print("ℹ MySQL connector not available (using SQLite)")
        
        # Test SQLite import
        import sqlite3
        print("✓ SQLite3 available")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_structure():
    """Test that the Flask app structure is correct"""
    try:
        from app import app, get_db_connection, init_db, DB_TYPE
        print(f"✓ Flask app structure is correct (using {DB_TYPE})")
        return True
    except Exception as e:
        print(f"✗ App structure error: {e}")
        return False

def test_templates():
    """Test that all required templates exist"""
    templates = ['templates/index.html', 'templates/journals.html', 'templates/editor.html']
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✓ Template exists: {template}")
        else:
            print(f"✗ Template missing: {template}")
            all_exist = False
    return all_exist

def test_static_files():
    """Test that all required static files exist"""
    static_files = [
        'static/styles.css',
        'static/home.js',
        'static/journals.js',
        'static/editor.js'
    ]
    all_exist = True
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✓ Static file exists: {static_file}")
        else:
            print(f"✗ Static file missing: {static_file}")
            all_exist = False
    return all_exist

def main():
    """Run all tests"""
    print("=" * 50)
    print("Travel Journal Hub - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("App Structure", test_app_structure),
        ("Templates", test_templates),
        ("Static Files", test_static_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        results.append(test_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
