from setuptools import setup



packages = ['loyalcat.types']

setup(
    name='loyalcat',
    version='0.0.1',
    install_requires=['aiohttp'],
    author='yupix',
    author_email='yupi0982@outlook.jp',
    license='MIT',
    python_requires='>=3.10, <4.0',
    packages=packages,
    entry_points={'console_scripts': ['loyalcat = loyalcat.cli:main']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.10',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
    ],
)

