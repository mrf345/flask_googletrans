"""
Flask-Googletrans
-------------
A Flask extension to add Googletrans google translation to the template 
with ability to cache translation to external pretty .json file
"""
from setuptools import setup


setup(
    name='Flask-Googletrans',
    version='0.9',
    url='https://github.com/mrf345/flask_googletrans/',
    download_url='https://github.com/mrf345/flask_googletrans/archive/0.8.tar.gz',
    license='MIT',
    author='Mohamed Feddad',
    author_email='mrf345@gmail.com',
    description='Googletrans google translation flask extension',
    long_description=__doc__,
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