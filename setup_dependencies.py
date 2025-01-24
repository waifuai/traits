#!/usr/bin/env python3
import sys
import subprocess
import platform
import os

def install_dependencies_ubuntu():
    """Install dependencies on Ubuntu systems."""
    try:
        # Update package lists
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        
        # Install system packages
        packages = [
            'python3',
            'python3-scipy',
            'python3-tk',
            'python3-matplotlib',
            'python3-pip'
        ]
        subprocess.run(['sudo', 'apt-get', 'install', '-y'] + packages, check=True)
        
        # Install Python packages
        pip_packages = ['scikit-learn', 'numpy', 'matplotlib', 'scipy']
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '-U'] + pip_packages, check=True)
        
        print("Successfully installed Ubuntu dependencies")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Ubuntu dependencies: {str(e)}")
        return False

def install_dependencies_windows():
    """Install dependencies on Windows systems."""
    try:
        # Install Python packages using pip
        pip_packages = ['scikit-learn', 'numpy', 'matplotlib', 'scipy']
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '-U'] + pip_packages, check=True)
        
        print("Successfully installed Windows dependencies")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Windows dependencies: {str(e)}")
        return False

def main():
    system = platform.system().lower()
    
    if system == 'linux':
        # Check if it's specifically Ubuntu
        try:
            with open('/etc/os-release') as f:
                if 'ubuntu' in f.read().lower():
                    return install_dependencies_ubuntu()
                else:
                    print("This script is optimized for Ubuntu. Other Linux distributions may need different packages.")
                    return False
        except FileNotFoundError:
            print("Cannot determine Linux distribution")
            return False
    elif system == 'windows':
        return install_dependencies_windows()
    else:
        print(f"Unsupported operating system: {system}")
        return False

if __name__ == '__main__':
    sys.exit(0 if main() else 1)