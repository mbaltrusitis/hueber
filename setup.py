from distutils.core import setup
from hueber import __version__
from hueber import __author__


VER = "{}.{}.{}".format(*__version__)  # major.minor.patch
URL = "https://github.com/mbaltrusitis/hueber.git"

setup(
    name="hueber",
    version=VER,
    description="Python API and tooling for Philips Hue.",
    long_description=open("README.rst").read(),
    author=__author__,
    author_email="matthew@baltrusitis.com",
    packages=["hueber", "hueber.api", "hueber.lib"],
    url=URL,
    download_url="{}/tarball/{}".format(URL, VER),
    data_files=[
        ("", ["README.rst"])
    ],
    license="MIT",
    keywords=["philips", "hue", "api"],
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

