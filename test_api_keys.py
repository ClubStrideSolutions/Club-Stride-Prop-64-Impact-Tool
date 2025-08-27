"""
Test API Keys Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_keys():
    """Test if API keys are configured and valid format"""
    results = []
    
    # Check OpenAI API Key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        if openai_key.startswith('sk-'):
            results.append("[OK] OpenAI API Key: Found and formatted correctly")
            results.append(f"   Key starts with: {openai_key[:10]}...")
        else:
            results.append("[WARNING] OpenAI API Key: Found but may be invalid format")
    else:
        results.append("[ERROR] OpenAI API Key: Not found in .env file")
    
    # Check Anthropic Claude API Key
    claude_key = os.getenv('ANTHROPIC_API_KEY')
    if claude_key:
        if claude_key.startswith('sk-ant-'):
            results.append("[OK] Anthropic API Key: Found and formatted correctly")
            results.append(f"   Key starts with: {claude_key[:15]}...")
        else:
            results.append("[WARNING] Anthropic API Key: Found but may be invalid format")
    else:
        results.append("[ERROR] Anthropic API Key: Not found in .env file")
    
    # Check optional settings
    mode = os.getenv('DEFAULT_AI_MODE', 'not set')
    results.append(f"\nOptional Settings:")
    results.append(f"  DEFAULT_AI_MODE: {mode}")
    results.append(f"  OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'not set')}")
    results.append(f"  CLAUDE_MODEL: {os.getenv('CLAUDE_MODEL', 'not set')}")
    
    return '\n'.join(results)

def test_api_connections():
    """Test actual API connections"""
    results = []
    
    # Test OpenAI connection
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.models.list()
        results.append("[OK] OpenAI API: Connection successful!")
    except Exception as e:
        results.append(f"[ERROR] OpenAI API Error: {str(e)[:100]}")
    
    # Test Anthropic connection
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        # Note: Anthropic doesn't have a simple list models endpoint
        # We'll just verify the client initializes
        results.append("[OK] Anthropic API: Client initialized successfully!")
    except Exception as e:
        results.append(f"[ERROR] Anthropic API Error: {str(e)[:100]}")
    
    return '\n'.join(results)

if __name__ == "__main__":
    print("=" * 60)
    print("API Keys Configuration Test")
    print("=" * 60)
    print("\nConfiguration Check:")
    print(test_api_keys())
    
    print("\nConnection Test:")
    print(test_api_connections())
    print("\n" + "=" * 60)