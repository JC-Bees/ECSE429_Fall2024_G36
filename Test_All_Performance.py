import requests
import pytest


# Can run all tests by running this file

def test_all_modules():
    test_modules = ["Todo_Performance_Tests.py"]
    pytest.main(test_modules)

if __name__ == "__main__":
    test_all_modules()

"""
    #ShutDown the API after tests
    url = "http://localhost:4567/shutdown"
    response = requests.get(url)
"""


