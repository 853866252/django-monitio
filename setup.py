import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-monitio',
    version='0.1',
    description='Unified, persistent and dynamic user messages/notifications for Django',
    long_description=read('README.md'),
    author='mpasternak',
    license='BSD',
    url='http://github.com/mpasternak/django-monitio',
    keywords = ['messages', 'django', 'persistent', 'sse'],
    packages=find_packages(exclude=['test_app', 'test_project']),
    package_data={'monitio': [
        'locale/*/LC_MESSAGES/*',
        'static/monitio/js/*.js',
        'static/monitio/css/*.css',
        'templates/*/*.html',
        'templates/*/*/*.html',
        'templates/*/*/*/*.html']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
