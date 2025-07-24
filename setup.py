from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="multiple-ai-agents",
    version="1.0.0",
    author="Aygün Varol",
    author_email="aygun.varol@tuni.fi",
    description="Hierarchical multi-agent framework for edge-enabled smart environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AygunVarol/multiple_ai_agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
        "gpu": [
            "torch[cuda]>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smart-supervisor=agents.supervisor.supervisor_agent:main",
            "smart-agent=agents.location_agents.base_agent:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.json", "*.md"],
    },
)
