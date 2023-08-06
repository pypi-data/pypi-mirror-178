import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="peekStock",
    version="0.0.1",
    author="Nancy Hsu",
    author_email="yutinghsu0411@gmail.com",
    description="A easy tool to track your stock on your work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nancy-Hsu/Peek-Stock/tree/main",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  
)
