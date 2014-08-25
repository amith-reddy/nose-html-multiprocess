import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'nose',
    'Jinja2'
]


setup(name='nose_htmlmp',
      version='0.0.1',
      description='Html output plugin for nose supporting multiprocess',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Testing",
      ],
      license='MIT',
      author='Roy Klinger',
      author_email='roy@taykey.com',
      url='',
      keywords='nosetest html multiprocessing',
      py_modules=['nose_htmlmp'],
      include_package_data=True,
      zip_safe=True,
      entry_points="""\
      [nose.plugins.0.10]
      htmlmp = nose_htmlmp:HtmlMp
      """,
      install_requires=requires)