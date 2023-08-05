import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="sword_mound",
    version="0.0.2",
    author="Linjie Xing",
    author_email="jin.951107@gmail.com",
    description="工具库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xlj997/sword-mound",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sm=sword_mound.converter:run'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)