import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ultrapy",
    version="0.1.0",
    author="FssAy",
    author_email="FssAy.AF4@protonmail.com",
    description="Simple official client for UltraSC.tk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ultra-SC/ultra-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
)
