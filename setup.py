from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Flask-Googletrans',
    version='0.11',
    url='https://github.com/mrf345/flask_googletrans/',
    download_url='https://github.com/mrf345/flask_googletrans/archive/0.11.tar.gz',
    license='MIT',
    author='Mohamed Feddad',
    author_email='mrf345@gmail.com',
    description='Googletrans google translation flask extension',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['translator'],
    packages=['flask_googletrans'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'googletrans'
    ],
    keywords=['flask', 'extension', 'google', 'translate', 'googletrans', 'json'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    setup_requires=['pytest-runner'],
    test_requires=['pytest']
)