#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("Starting Django application for Railway...")
    
    # Run migrations
    print("Running migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
    
    # Collect static files
    print("Collecting static files...")
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
    
    # Get PORT from environment
    port = os.environ.get('PORT', '8000')
    print(f"Starting gunicorn on port {port}...")
    
    # Start gunicorn
    cmd = [
        "gunicorn",
        "blog_projet.wsgi:application",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "2",
        "--timeout", "120"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    os.execvp("gunicorn", cmd)

if __name__ == "__main__":
    main()