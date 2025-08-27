"""
KPI Dashboard System - Main Launcher
=====================================
AI-Enhanced Dashboard with OpenAI and Claude Integration
"""

import sys
from pathlib import Path

# Add project directories to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'core'))
sys.path.insert(0, str(project_root / 'modules'))

def main():
    """Launch the AI-Enhanced KPI Dashboard"""
    try:
        # Import the main dashboard
        from core.ai_enhanced_dashboard import AIEnhancedDashboard
        
        # Initialize and run
        dashboard = AIEnhancedDashboard()
        dashboard.run()
        
    except ImportError as e:
        print(f"Error importing dashboard: {e}")
        print("\nTrying alternative dashboard...")
        
        try:
            from core.enhanced_main import EnhancedKPIDashboard
            dashboard = EnhancedKPIDashboard()
            dashboard.run()
        except ImportError as e2:
            print(f"Error: {e2}")
            print("\nPlease ensure all dependencies are installed:")
            print("  pip install -r requirements_ai.txt")

if __name__ == "__main__":
    print("=" * 60)
    print("AI-Enhanced KPI Dashboard System")
    print("Powered by OpenAI GPT-4 and Claude 3 Opus")
    print("=" * 60)
    print()
    print("Starting dashboard...")
    print("Open your browser at: http://localhost:8502")
    print()
    main()