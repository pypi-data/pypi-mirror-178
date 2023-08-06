from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='test-27-11',
    version='0.1',
    description='Test: work with PyPi',
    long_description= long_description,
    long_description_content_type  = "text/markdown",
    author='Marko Đukanović',
    author_email='marko.djukanovic@pmf.unibl.org',
    url='https://github.com/markodjukanovic90/',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ],
    python_requires= ">=3.6",
    py_modules=["test-27-11"],
    package_dir = {'test-27-11':'test-27-11'}, 
    install_requires=[ "sympy" ],
)
