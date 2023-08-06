from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'USRModem'

setup(
    name='USRModem',
    version='1.0.0',
    author='Abirami',
    author_email='abiramig1930@gmail.com',
    url='',
    description='Analog Voice Modem Testing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'callAndAnswer = USRModem.callAndAnswer:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='analog_modem',
    install_requires=requirements,
    zip_safe=False
)