#!/usr/bin/env python3
"""Minimal test to isolate MindWell issue"""

import sys
import os

# Test 1: Basic import
print("=== Test 1: Import test ===")
try:
    from ai.mindwell_bot import mindwell_reply
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Basic function call
print("\n=== Test 2: Function call test ===")
try:
    result = mindwell_reply("I'm feeling anxious and overwhelmed")
    print("✅ Function call successful")
    print(f"Response: {result['response'][:100]}...")
except Exception as e:
    print(f"❌ Function call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Flask app context
print("\n=== Test 3: Flask app context test ===")
try:
    from app import app
    with app.app_context():
        result = mindwell_reply("test message")
        print("✅ Flask context test successful")
        print(f"Response: {result['response'][:100]}...")
except Exception as e:
    print(f"❌ Flask context test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== All tests completed ===")
