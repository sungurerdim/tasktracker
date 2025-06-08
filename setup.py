from setuptools import setup, find_packages

setup(
    name="tasktracker",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["rich"],
    author="Sungur Zahid Erdim",
    author_email="sungurerdim@gmail.com",
    description="A simple and modular task tracking system for terminal-based worker/task execution.",
    python_requires=">=3.10",
    license="MIT",
)
