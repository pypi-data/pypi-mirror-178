from setuptools import setup
from setuptools import setup, find_packages



setup(
    name='loyalcat',
    version='0.0.3',
    install_requires=['aiohttp'],
    author='yupix',
    author_email='yupi0982@outlook.jp',
    license='MIT',
    python_requires='>=3.10, <4.0',
    packages=find_packages(),
    entry_points={'console_scripts': ['loyalcat = loyalcat.cli:main']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.10',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
    ],
)

