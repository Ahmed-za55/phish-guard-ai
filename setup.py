from setuptools import setup, find_packages

setup(
    name="phishguard-ai-sovereign",
    version="70.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.28.0",
        "torch>=2.0.0",
        "opencv-python>=4.8.0"
    ],
    author="Apex Sovereign Architect",
    description="The Ultimate 100+ Cores Autonomous Cybernetic Security Ecosystem",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/phish-guard-ai",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)