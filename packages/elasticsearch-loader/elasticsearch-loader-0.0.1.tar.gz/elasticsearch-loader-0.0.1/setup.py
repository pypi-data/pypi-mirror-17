from setuptools import setup
import pypandoc
try:
    long_description = pypandoc.convert('README.md', 'rst')
except Exception:
    long_description = ''


setup(
    name='elasticsearch-loader',
    version='0.0.1',
    py_modules=['elasticsearch_loader'],
    keywords=['elastic', 'elasticsearch', 'csv', 'json', 'parquet', 'bulk', 'loader'],
    url='https://github.com/MosheZada/elasticsearch_loader',
    license='',
    long_description=long_description,
    description='A pythonic tool for batch loading data files (json, parquet, csv, tsv) into ElasticSearch',
    install_requires=[
        'elasticsearch',
        'click',
        'futures'
    ],
    tests_require=[
        'pytest'
    ],
    extras_require={
        'parquet': ['parquet']
    },
    entry_points={
        'console_scripts': [
            'elasticsearch_loader = elasticsearch_loader:cli',
        ]
    }
)
