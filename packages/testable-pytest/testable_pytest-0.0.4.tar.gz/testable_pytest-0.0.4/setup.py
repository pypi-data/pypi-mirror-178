from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "Testable PyTest Wrapper"
LONG_DESCRIPTION = "Testable interface for PyTest"

# Setting up
setup(
    name="testable_pytest",
    version=VERSION,
    author="Ryan de Marigny",
    author_email="testableproject@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pydantic>=1.10.2", "pytest>=7.2.0", "requests>=2.28.1", "python-dotenv>=0.21.0"],
    keywords=["python", "pytest", "testable"],
    entry_points={"pytest11": ["name_of_plugin = testable_pytest.plugin"]},
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
