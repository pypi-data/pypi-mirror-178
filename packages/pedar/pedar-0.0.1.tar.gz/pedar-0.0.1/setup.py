from setuptools import setup

setup(
    name='pedar',
    version='0.0.1',
    description='',
    author='Amirali Esfandiari',
    author_email='amiralinull@gmail.com',
    py_modules=['pedar'],
    packages=['pedar'],
    package_dir={'pedar': 'pedar'},
    python_requires='>=3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        ],
    entry_points = '''
        [console_scripts]
        pedar=pedar.cli:main
    ''',
)
