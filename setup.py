from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='dept-fin-app',
    version='1.0.dev1',
    author='Tony Sol',
    author_email='ortege@gmail.com',
    licence='MIT',
    description='Web app to manage employees and departments. REST API included',
    long_description=long_description,
    url='https://github.com/TonySol/fin',
    packages=find_packages(),
    # This tells setuptools to install any data files it finds in your packages from MANIFEST.
    include_package_data=True,
    # This tells not to try to run app from zip file but rather extract it first.
    zip_safe=False,
    install_requires=[
        "Flask==2.0.2"
        "Flask-SQLAlchemy==2.5.1"
        "PyMySQL==1.0.2"
        "Flask-Migrate==3.1.0"
        "Flask-RESTful==0.3.9"
        "python-dotenv==0.19.2"
    ],
    python_requires='>=3.8'
)
