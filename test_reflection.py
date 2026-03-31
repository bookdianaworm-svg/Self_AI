#!/usr/bin/env python3
"""
Simple Self-Reflection Test - Test the core AI thinking mechanism
"""
import json
import subprocess
import time

def test_simple_reflection():
    """Test if AI can do basic self-reflection"""
    print("🧪 Testing simple self-reflection...")
    
    # Simple reflection prompt
    reflection_prompt = """You are an AI that can improve itself. Think about this simple question:
    
    Question: What is one small thing you could improve about yourself?
    
    Answer in JSON format with these keys:
    {
        "thought": "your thinking process",
        "improvement": "the specific improvement",
        "reason": "why this would help"
    }
    
    Keep your answer simple and focused."""
    
    try:
        result = subprocess.run([
            'ollama', 'run', 'tinyllama',
            reflection_prompt
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"Raw response: {response[:200]}...")
            
            # Try to parse JSON
            try:
                parsed = json.loads(response)
                print("✅ Successfully parsed JSON response:")
                print(f"  Thought: {parsed.get('thought', 'N/A')}")
                print(f"  Improvement: {parsed.get('improvement', 'N/A')}")
                print(f"  Reason: {parsed.get('reason', 'N/A')}")
                return True
            except json.JSONDecodeError as e:
                print(f"⚠️  Response not valid JSON: {e}")
                print(f"Response was: {response}")
                return False
        else:
            print(f"❌ Self-reflection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Self-reflection timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Self-reflection error: {e}")
        return False

def test_complex_reflection():
    """Test the type of reflection the AI was failing on"""
    print("\n🧪 Testing complex self-reflection (what the AI was trying)...")
    
    complex_prompt = """You are an AI system designed for self-improvement. Your primary goal is: Improve your own capabilities and effectiveness

Current context: My current code has 458 lines, 2 classes, and 18 methods.

Reflection prompt: Analyze my current capabilities and identify one specific improvement I can make to become more effective at self-improvement.

Provide a thoughtful response that considers:
1. How this relates to your self-improvement goal
2. What actions you should take
3. Potential risks or considerations
4. How to measure success

Format your response as JSON with keys: 'thoughts', 'actions', 'risks', 'success_metrics'"""
    
    try:
        result = subprocess.run([
            'ollama', 'run', 'tinyllama',
            complex_prompt
        ], capture_output=True, text=True, timeout=120)  # 2 minute timeout
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"Raw response: {response[:300]}...")
            
            # Try to parse JSON
            try:
                parsed = json.loads(response)
                print("✅ Complex reflection succeeded!")
                print(f"  Thoughts: {parsed.get('thoughts', 'N/A')[:100]}...")
                print(f"  Actions: {parsed.get('actions', 'N/A')[:100]}...")
                return True
            except json.JSONDecodeError as e:
                print(f"⚠️  Complex reflection not valid JSON: {e}")
                return False
        else:
            print(f"❌ Complex reflection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Complex reflection timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"❌ Complex reflection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting self-reflection capability tests...")
    print("=" * 60)
    
    # Test 1: Simple reflection
    simple_success = test_simple_reflection()
    
    # Test 2: Complex reflection (what the AI was trying)
    complex_success = test_complex_reflection()
    
    print("\n" + "=" * 60)
    print("📊 REFLECTION TEST RESULTS")
    print("=" * 60)
    print(f"Simple reflection: {'✅ PASS' if simple_success else '❌ FAIL'}")
    print(f"Complex reflection: {'✅ PASS' if complex_success else '❌ FAIL'}")
    
    if simple_success and complex_success:
        print("🎉 AI can self-reflect! Ready for self-improvement loop.")
    elif simple_success:
        print("⚠️  AI can do simple reflection but struggles with complex reasoning.")
        print("💡 Recommendation: Start with simpler reflection prompts in main.py")
    else:
        print("❌ AI cannot self-reflect properly. Need to fix the reflection mechanism.")