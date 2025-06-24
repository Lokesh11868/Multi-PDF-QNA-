import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False
    return True

def check_env():
    """Check environment setup"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("Create .env file with: GOOGLE_API_KEY=your_key_here")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not set in .env file")
        return False
    
    print("✅ Environment configured correctly!")
    return True

def run_app():
    """Run the Streamlit app"""
    if install_requirements() and check_env():
        print("🚀 Starting app...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "scripts/app.py"])
    else:
        print("❌ Setup incomplete. Please fix the issues above.")

if __name__ == "__main__":
    run_app()
