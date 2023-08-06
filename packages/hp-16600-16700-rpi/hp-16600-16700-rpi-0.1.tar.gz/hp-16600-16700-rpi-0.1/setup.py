import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hp-16600-16700-rpi",
    version="0.1",
    author="Martin Miedema",
    author_email="git@number42.net",
    description="Interface with HP / Agilent 16600A and 16700 logic analyzers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/number42net/hp-16600-16700-rpi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.6",
    install_requires=["pandas"],
    project_urls={
        "Documentation": "https://hp-16600-16700-rpi.readthedocs.io",
        "Source": "https://github.com/number42net/hp-16600-16700-rpi",
    },
)
