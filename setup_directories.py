#!/usr/bin/env python3
import os
import sys
import sqlite3
from pathlib import Path
from database import TraitDatabase

def setup_directories():
    """Create necessary directories and files."""
    try:
        # Create image directory
        img_dir = Path('img')
        img_dir.mkdir(exist_ok=True)
        
        # Create placeholder images
        (img_dir / 'neutral_persons.png').touch()
        (img_dir / 'neutral_company.png').touch()
        
        # Initialize database and set permissions
        db_path = Path('persons.db')
        trait_db_path = Path('traits.db')
        
        # Create an empty persons database if it doesn't exist
        if not db_path.exists():
            conn = sqlite3.connect(db_path)
            conn.close()
            
        # Create an empty traits database if it doesn't exist
        if not trait_db_path.exists():
            conn = sqlite3.connect(trait_db_path)
            conn.close()
            
        # Initialize the traits database with tables
        trait_db = TraitDatabase()
        trait_db.create_tables()
        
        print("Successfully set up directories and files")
        return True
    
    except Exception as e:
        print(f"Error setting up directories: {str(e)}")
        return False

def main():
    return setup_directories()

if __name__ == '__main__':
    sys.exit(0 if main() else 1)