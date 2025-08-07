#!/usr/bin/env python3
"""
Production deployment script for Student Retention Prediction API
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def verify_model():
    """Verify that the ML model loads correctly"""
    print("🤖 Verifying ML model...")
    try:
        import pickle
        with open('simple_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print(f"✅ Model loaded: {type(model)}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        sys.exit(1)

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    try:
        subprocess.check_call([sys.executable, "tests/system_test.py"])
        print("✅ All tests passed")
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        sys.exit(1)

def create_systemd_service(port=5000, user="www-data"):
    """Create systemd service file for production deployment"""
    service_content = f"""[Unit]
Description=Student Retention Prediction API
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={Path.cwd()}
Environment=PATH={Path.cwd()}/.venv/bin
ExecStart={Path.cwd()}/.venv/bin/python simple_api.py --port {port} --host 0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "/etc/systemd/system/student-retention-api.service"
    print(f"📝 Creating systemd service at {service_file}")
    
    try:
        with open(service_file, 'w') as f:
            f.write(service_content)
        print("✅ Systemd service created")
        print("💡 Enable with: sudo systemctl enable student-retention-api")
        print("💡 Start with: sudo systemctl start student-retention-api")
    except PermissionError:
        print("❌ Permission denied. Run with sudo for systemd service creation")
        print(f"📋 Service content saved to: {Path.cwd()}/student-retention-api.service")
        with open("student-retention-api.service", 'w') as f:
            f.write(service_content)

def setup_nginx(domain=None, port=5000):
    """Create nginx configuration"""
    server_name = domain or "localhost"
    
    nginx_config = f"""server {{
    listen 80;
    server_name {server_name};
    
    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    location /api/ {{
        proxy_pass http://127.0.0.1:{port}/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Origin, Content-Type, Accept, Authorization";
    }}
}}
"""
    
    config_file = f"/etc/nginx/sites-available/student-retention-api"
    print(f"📝 Creating nginx config at {config_file}")
    
    try:
        with open(config_file, 'w') as f:
            f.write(nginx_config)
        print("✅ Nginx config created")
        print("💡 Enable with: sudo ln -s /etc/nginx/sites-available/student-retention-api /etc/nginx/sites-enabled/")
        print("💡 Test with: sudo nginx -t")
        print("💡 Reload with: sudo systemctl reload nginx")
    except PermissionError:
        print("❌ Permission denied. Run with sudo for nginx configuration")
        print(f"📋 Config saved to: {Path.cwd()}/nginx-student-retention-api.conf")
        with open("nginx-student-retention-api.conf", 'w') as f:
            f.write(nginx_config)

def main():
    parser = argparse.ArgumentParser(description="Deploy Student Retention Prediction API")
    parser.add_argument("--port", type=int, default=5000, help="API port (default: 5000)")
    parser.add_argument("--domain", type=str, help="Domain name for nginx config")
    parser.add_argument("--user", type=str, default="www-data", help="System user for service")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--nginx", action="store_true", help="Create nginx configuration")
    parser.add_argument("--systemd", action="store_true", help="Create systemd service")
    
    args = parser.parse_args()
    
    print("🚀 Student Retention Prediction API Deployment")
    print("=" * 50)
    
    # Pre-deployment checks
    check_python_version()
    install_dependencies()
    verify_model()
    
    if not args.skip_tests:
        run_tests()
    
    # Production setup
    if args.systemd:
        create_systemd_service(args.port, args.user)
    
    if args.nginx:
        setup_nginx(args.domain, args.port)
    
    print("\n" + "=" * 50)
    print("🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Start the API server:")
    print(f"   python simple_api.py --port {args.port}")
    print("2. Test the API:")
    print(f"   curl http://localhost:{args.port}/api/health")
    print("3. Open the test interface:")
    print(f"   Open examples/api_test.html in browser")
    
    if args.systemd:
        print("4. Enable systemd service:")
        print("   sudo systemctl enable student-retention-api")
        print("   sudo systemctl start student-retention-api")
    
    if args.nginx:
        print("5. Configure nginx:")
        print("   sudo ln -s /etc/nginx/sites-available/student-retention-api /etc/nginx/sites-enabled/")
        print("   sudo nginx -t && sudo systemctl reload nginx")

if __name__ == "__main__":
    main()
