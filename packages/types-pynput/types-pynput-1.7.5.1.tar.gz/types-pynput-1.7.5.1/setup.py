from setuptools import setup

name = "types-pynput"
description = "Typing stubs for pynput"
long_description = '''
## Typing stubs for pynput

This is a PEP 561 type stub package for the `pynput` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pynput`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pynput. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `f8dfb5f725db9e3ef4f6934191bf4fa61521217c`.
'''.lstrip()

setup(name=name,
      version="1.7.5.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pynput.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pynput-stubs'],
      package_data={'pynput-stubs': ['__init__.pyi', '_info.pyi', '_util.pyi', 'keyboard/__init__.pyi', 'keyboard/_base.pyi', 'keyboard/_dummy.pyi', 'mouse/__init__.pyi', 'mouse/_base.pyi', 'mouse/_dummy.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
