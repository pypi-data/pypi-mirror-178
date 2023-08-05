from setuptools import setup
from codecs import open
from os import path
import re
package_name = "irucapy"
root_dir = path.abspath(path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, "requirements.txt")).readlines()]


with open(path.join(root_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(
        r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

setup(
    name=package_name,
    version=version,
    description="API Gateway for iruca, an attendance management service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mya-Mya/irucapy",
    author="Mya-Mya",
    author_email="",
    license="MIT",
    keywords="iruca, API, Attendance, Management, Office, AttendanceManagement",
    packages=[package_name],
    install_requires=_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business :: Office Suites",
    ],
)