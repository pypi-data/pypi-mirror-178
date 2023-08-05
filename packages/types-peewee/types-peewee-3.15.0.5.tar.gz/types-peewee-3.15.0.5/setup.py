from setuptools import setup

name = "types-peewee"
description = "Typing stubs for peewee"
long_description = '''
## Typing stubs for peewee

This is a PEP 561 type stub package for the `peewee` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `peewee`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/peewee. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `5b4adfde207f3673d726271e15b0609a8200d3cf`.
'''.lstrip()

setup(name=name,
      version="3.15.0.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/peewee.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['peewee-stubs'],
      package_data={'peewee-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
