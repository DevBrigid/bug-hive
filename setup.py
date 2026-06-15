from setuptools import setup, find_packages

setup(
    name="bughive",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["cli", "storage"],
    include_package_data=True,
    install_requires=[
        "click",
        "tabulate",
        "colorama",
        "pytest"
    ],
    entry_points={
        "console_scripts": [
            "bughive=cli:bughive",
        ],
    },
)