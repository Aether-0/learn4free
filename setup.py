from setuptools import setup, find_packages

setup(
    name='learn4free',
    version='1.0.0',
    author='Aether',
    author_email='sanwana12.conceptx@gmail.com',
    description='A scraper for free courses from coursekingdom.xyz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Aether-0/learn4free',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'fake-useragent',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'learn4free=learn4free.__init__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
