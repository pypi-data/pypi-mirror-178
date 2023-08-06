# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_schema']

package_data = \
{'': ['*'], 'iscc_schema': ['models/*', 'reference/*']}

install_requires = \
['jcs>=0.2,<0.3', 'pydantic>=1.9,<2.0']

setup_kwargs = {
    'name': 'iscc-schema',
    'version': '0.4.0',
    'description': 'ISCC - JSON-LD Metadata and OpenAPI Service Descriptions',
    'long_description': '# **ISCC** - Schema\n\n*ISCC - JSON-LD Metadata and OpenAPI Service Descriptions*\n\n[![Build](https://github.com/iscc/iscc-schema/actions/workflows/tests.yml/badge.svg)](https://github.com/iscc/iscc-schema/actions/workflows/tests.yml)\n[![Version](https://img.shields.io/pypi/v/iscc-schema.svg)](https://pypi.python.org/pypi/iscc-schema/)\n\n## Introduction\n\nThis repository hosts all schema definitions of the ISCC. Schemas are defined in\n[OpenAPI v3.1.0](https://spec.openapis.org/oas/v3.1.0.html) format and serve as a\nsingle source of truth for auto-generated [JSON Schema](https://json-schema.org/)\ndefinitions, [JSON-LD](https://json-ld.org/) contexts, and other schema related\nartifacts.\n\n## Metadata for Digital Content\n\nMetadata is data about data. For digital content, metadata may describe assets for different\npurposes such as data management, data provenance, allocation of royalties, indexing,\ndisambiguation, process automation, etc.\n\n## ISCC Metadata\n\nCalculating ISCC codes requires extensive processing of media assets. As a by-product, an ISCC\nprocessor can automatically produce and retain metadata that describes the asset and helps with\ncomparing and matching digital content. ISCC creation is also an opportunity to embed metadata\ninto a digital asset. Once the metadata is embedded, an ISCC processor will automatically\nregenerate the same ISCC Meta-Code without manually supplying custom metadata for processing.\nAs the ISCC targets a broad set of use-cases, it comes with a minimal and generic metadata schema.\nThis site documents the ISCC metadata model.\n\n## Types of Metadata\n\nFor the identification of digital assets, ISCC distinguishes between two major types of metadata:\n\n### Implicit Metadata\n\nImplicit metadata is data that can be measured by analyzing a media asset. For example, an ISCC\nprocessor can infer pixel width and height from an image or duration from an audio file. The use\nof implicit metadata is very efficient and robust. It does not require a human to verify the\ncorrectness of the data because it can be measured and verified automatically.\n\n### Explicit Metadata\n\nExplicit metadata is data about media assets assembled and curated by people. It is often stored\nseparately from the files in databases but may also be embedded into media assets. In contrast to\nimplicit metadata, human-curated metadata is prone to errors, laborious to manage, and often not\nup to date. Platforms also tend to remove embedded metadata from the files they are hosting.\n\n## Documentation\n\nDocumentation is hosted at [schema.iscc.codes](https://schema.iscc.codes)\n\n## Status\n\nUnder development. Expect breaking changes until we reach a version 1.0 release.\n\n## Generated files\n\nThe source of code generation are the files at `iscc_schema/models/*`.\nThe outputs produced when running `poe build` are:\n\n- [`docs/schema/iscc.json`](https://github.com/iscc/iscc-schema/blob/main/docs/schema/iscc.json) - JSON Schema for ISCC Metadata\n- [`docs/schema/index.md`](https://github.com/iscc/iscc-schema/blob/main/docs/schema/index.md) - JSON Schema Markdown documentation\n- [`docs/context/iscc.jsonld`](https://github.com/iscc/iscc-schema/blob/main/docs/context/iscc.jsonld) - JSON-LD context for ISCC Metadata\n- [`docs/terms/index.md`](https://github.com/iscc/iscc-schema/blob/main/docs/context/index.md) - ISCC Metadata Vocabulary documentation\n- [`iscc_schema/schema.py`](https://github.com/iscc/iscc-schema/blob/main/iscc_schema/schema.py) - Pydantic models for ISCC Metadata\n- [`iscc_schema/generator.py`](https://github.com/iscc/iscc-schema/blob/main/iscc_schema/generator.py) - Pydantic models for Generator Service API\n\n\n## Published files\n\nThe generated files are published under the following canonical URLs:\n\n- [`http://purl.org/iscc/schema`](http://purl.org/iscc/schema) - JSON Schema latest version\n- [`http://purl.org/iscc/context`](http://purl.org/iscc/context) - JSON-LD Context latest version\n- [`http://purl.org/iscc/terms`](http://purl.org/iscc/terms) - ISCC Metadata Vocabulary latest version\n- [`http://pypi.org/project/iscc-schema`](http://pypi.org/project/iscc-schema) - Python package with pydantic models\n\n## OpenAPI Docs\n\n- [ISCC Generator Service](https://schema.iscc.codes/api)\n\n## OpenAPI Extensions\n\nThe OpenAPI Specification allows for\n[extending](https://spec.openapis.org/oas/latest.html#specification-extensions) the\nspecification with custom fields. Extensions must start with `x-`.\nAll ISCC extensions start with `x-iscc-`:\n\n- `x-iscc-context` - for documenting JSON-LD contexts.\n- `x-iscc-schema-doc` - for original descriptions from [schema.org](https://schema.org).\n- `x-iscc-embed` - for information on how to embed fields into media assets.\n- `x-iscc-status` - for information about status of the field\n',
    'author': 'Titusz',
    'author_email': 'tp@py7.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://iscc.codes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
