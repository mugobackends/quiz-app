import sys
import os
import pytest
from lib.cli import main_menu
from lib.helpers import initialize_database

# Set up the path for module imports
# This ensures that 'lib' is recognized as a package
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

def run_cli():
    print("Welcome to the Quiz App!")
    main_menu()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "initdb":
            initialize_database()
        elif command == "runtests":
            print("Running tests...")
            # Use pytest.main to run tests programmatically
            # Pass tests/ directory as argument to discover tests
            pytest.main(["tests"]) 
        else:
            print(f"Unknown command: {command}")
            print("Usage: python main.py [initdb|runtests]")
    else:
        run_cli()