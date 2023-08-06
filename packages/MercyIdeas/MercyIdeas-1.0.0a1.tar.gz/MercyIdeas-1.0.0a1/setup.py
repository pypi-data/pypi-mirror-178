import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='MercyIdeas',
    version='1.0.0a1',
    author='MercyNaima',
    author_email='2868681725@qq.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MercyNaima/PythonStudy',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
