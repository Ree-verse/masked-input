import os

from setuptools import setup, find_packages

script_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_folder)

# Use the README.md content for the long description:
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="masked-input",
    version="1.0.0",
    author="Ree-verse",
    author_email="reeversesoft@gmail.com",
    python_requires='>=3.9',
    url="https://github.com/ree-verse/masked-input",
    description="Cross-platform library to read password input with various masking options.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files = ["LICENSE"],
    keywords='console, cross-platform, getpass, input, linux, macOS, mask, masked, masked-input, password, python, secure, security, shell, terminal, windows',
    project_urls={
    "Source": "https://github.com/ree-verse/masked-input",
    "Issues": "https://github.com/ree-verse/masked-input/issues",
    "Docs": "https://github.com/ree-verse/masked-input/blob/main/README.md",
},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    test_suite="tests",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Security",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
