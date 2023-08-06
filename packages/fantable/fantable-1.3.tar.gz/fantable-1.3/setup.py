from setuptools import setup

long_description = open("README.md", "r", encoding="utf-8").read()
setup(
    name="fantable",
    version="1.3",
    description="Table Builder For Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sptty-chan/fantable",
    license="MIT",
    author="Sptty Chan",
    author_email="sptty_chan@ccmail.uk",
    packages=["fantable"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.10",
    ],
)
