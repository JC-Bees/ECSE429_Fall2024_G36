import requests
import pytest
import pytest_randomly

# Can run all tests by running this file

def test_all_modules():
    test_modules = ["Todo_Module_Tests.py", "Projects_Module_Tests.py", "Categories_Module_Tests.py"]
    pytest.main(test_modules)

if __name__ == "__main__":
    test_all_modules()