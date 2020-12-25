from setuptools import setup, find_packages


setup(
    name='tomorrow-pdf-converter',
    version='0.1.1',
    url='https://github.com/sebwarnke/tomorrow-bank-statement-converter',
    license='MIT',
    author='Sebastian Warnke',
    author_email='',
    description='',
    install_requires=['py_pdf_parser'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tconverter=tomorrow_pdf_converter.converter:main'
        ]
    }
)
