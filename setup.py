import os
import setuptools

with open(os.path.join("docs", "PYPIREADME.md"), "r") as f:
    long_description = f.read()

with open("VERSION", "r") as f:
    version_num = f.read()

setuptools.setup(
    name="lichs",
    version=version_num,
    author="Casimir Rönnlöf",
    author_email="casimirr04@gmail.com",
    description="Play chess against other real players in your terminal using Lichess",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cqsi/lichs",
    packages=["lichs"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9',
    install_requires=["chess>=1.11.0", "berserk>=0.14.0"],
    entry_points={
        "console_scripts": [
            "lichs=lichs.__main__:main"
        ]
    },
    
)