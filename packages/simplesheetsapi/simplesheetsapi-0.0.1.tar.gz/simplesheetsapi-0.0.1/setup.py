from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='simplesheetsapi',
    version='0.0.1',
    description='Simple lib to work with google sheets api',
    long_description="Can read, write and find in spreadsheets",
    url='',
    author='Sheets Try',
    author_email='sheetsapitry@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='spreadsheets',
    packages=find_packages(),
    install_requires=['google-api-core==2.10.2', "google-api-python-client==2.66.0", "google-auth==2.14.1", "google-auth-httplib2==0.1.0", "google-auth-oauthlib==0.7.1", "googleapis-common-protos==1.57.0"]
)