#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage:
# pip install https://github.com/jfbercher/jupyter_latex_envs/archive/master.zip --user
# verbose mode can be enabled with -v switch eg pip -v install ...
# upgrade with a --upgrade.
# A system install can be done by omitting the --user switch.

from __future__ import print_function
import io

from setuptools import setup, find_packages
from os.path import join, dirname
from sys import exit, prefix, argv


msg="""
----------------- INSTALLATION -------------------------
step 1: pip3 install jupyter_latex_envs [--user][--upgrade]
--> Now:
step 2: install the notebook extension
jupyter nbextension install --py latex_envs [--user]
step 3: and enable it
jupyter nbextension enable latex_envs [--user] --py
----------------------------------------------------------
"""

readme_file = open('README.rst', 'r')
try:
    detailed_description = readme_file.read()
finally:
    readme_file.close()

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(name='jupyter_latex_envs',
      version='1.2.10',
      description=("Jupyter notebook extension which supports (some) LaTeX environments "  # noqa
      "within markdown cells. Also provides support for labels and crossreferences, "  # noqa
      "document wide numbering, bibliography, and more..."),
      # '\n'.join(__doc__.split("\n")[2:]).strip(),
      long_description=detailed_description,
      url='http://github.com/jfbercher/jupyter_latex_envs',
      author='Jean-François Bercher',
      author_email='jf.bercher@gmail.com',
      license='Modified BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'nbconvert.exporters': [
            'html_with_lenvs = latex_envs.latex_envs:LenvsHTMLExporter',
            'latex_with_lenvs = latex_envs.latex_envs:LenvsLatexExporter',
            'html_with_toclenvs = latex_envs.latex_envs:LenvsTocHTMLExporter',
                 ],
      },
      classifiers=[
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: BSD License',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Programming Language :: JavaScript',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Topic :: Utilities',
            ],
  )


if 'install' in argv:
    print(msg)
