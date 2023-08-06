from setuptools import setup, find_packages
readme = open('README.txt', encoding="utf8")

setup(
    name='quicksqlconnector',
    version='1.5',
    license='MIT',
    license_files='LICENSE',
    author="Anas Raza",
    author_email='anasraza1@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://quicksqlconnector.web.app/',
    keywords='quicksqlconnector, sql, database, mysql, postgres, sqlite3',
    install_requires=[
          'mysql-connector-python',
          'sqlite3',
          'psycopg2'
      ],
    description='Run MySQL, PostgresSQL, SQLite queries with just one line in python. The Ultimate SQL Library.',
    long_description=readme.read(),
    long_description_content_type='text/markdown'
)