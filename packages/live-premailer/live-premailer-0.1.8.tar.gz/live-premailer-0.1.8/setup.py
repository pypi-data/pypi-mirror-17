from setuptools import setup


setup(
    name='live-premailer',
    packages=['lpremailer'],
    version='0.1.8',
    description='Live premailer for jinja2 templates',
    author='turkus',
    author_email='wojciechrola@wp.pl',
    url='https://github.com/turkus/live-premailer',
    download_url='https://github.com/turkus/live-premailer/tarball/0.1',
    keywords=['live', 'browsersync', 'jinja2', 'premailer'],
    entry_points={
        'console_scripts': [
            'lpremailer = lpremailer.main:main',
        ]
    },
    install_requires=['jinja2', 'premailer', 'watchdog', 'six'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
)
