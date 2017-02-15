from distutils.core import setup
from hueber import __version__
from hueber import __author__


setup(
    name="hueber",
    version="{}.{}.{}".format(*__version__),  # major.minor.patch
    description="Python API and tooling for Philips Hue.",
    long_description=open("README.rst").read(),
    author=__author__,
    packages=["hueber", "hueber.api", "hueber.lib"],
    url="https://github.com/mbaltrusitis/hueber.git",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Home Automation"
    ]
)

