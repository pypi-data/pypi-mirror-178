from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='trebasiccalculator',
    version='0.0.1',
    description='A basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Tre Robinson',
    author_email='trerrobinson@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['']
)