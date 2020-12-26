from setuptools import setup, find_packages


setup(
    name='tconvert',
    version='1.1.0',
    url='https://github.com/sebwarnke/tconvert',
    license='MIT',
    author='Sebastian Warnke',
    author_email='',
    description='A Tomorrow Bank Statement Converter for Money Money',
    install_requires=['py_pdf_parser'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tconvert=tomorrow_pdf_converter.converter:main'
        ]
    }
)
