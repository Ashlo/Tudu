from setuptools import setup

setup(
    name='tudu',
    version='0.1',
    py_modules=['tudu'],
    install_requires=[
        'plyer',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'tudu=tudu:main',
        ],
    },
    author='Ashutosh Bele',
    author_email='ashutoshbele8@gmail.com',
    description='A terminal task management app',
    url='https://github.com/Ashlo/Tudu',
)
