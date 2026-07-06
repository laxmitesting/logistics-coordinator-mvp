import os
import sys
from dotenv import load_dotenv

# 1. Point the tests to your 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# 2. Load the API keys for your geo tests
load_dotenv()