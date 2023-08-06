from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flaskr_xwj',
    version='1.0.0',
    author='Attack825',
    author_email='2707138687@qq.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
# 命令python.exe setup.py sdist
