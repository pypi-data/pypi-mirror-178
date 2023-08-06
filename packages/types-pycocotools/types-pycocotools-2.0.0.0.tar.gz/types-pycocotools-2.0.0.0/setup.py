from setuptools import setup

name = "types-pycocotools"
description = "Typing stubs for pycocotools"
long_description = '''
## Typing stubs for pycocotools

This is a PEP 561 type stub package for the `pycocotools` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pycocotools`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pycocotools. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `a132ff215d166451a0e2e9a668ac29bd2d4ca72f`.
'''.lstrip()

setup(name=name,
      version="2.0.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pycocotools.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pycocotools-stubs'],
      package_data={'pycocotools-stubs': ['__init__.pyi', 'coco.pyi', 'cocoeval.pyi', 'mask.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
