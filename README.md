<!-- ---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
--- -->

<!-- #region tags=[] -->
# ConfPrint <!-- omit in toc -->
[![GitHub License](https://img.shields.io/github/license/lewiuberg/confprint?color=blue)](LICENSE)
![Python](https://img.shields.io/pypi/pyversions/confprint.svg?color=blue)
[![PyPI](https://img.shields.io/pypi/v/confprint.svg?color=blue)](https://pypi.org/project/confprint/)
[![Downloads](https://pepy.tech/badge/confprint)](https://pepy.tech/project/confprint)
[![Codecov code coverage](https://img.shields.io/codecov/c/github/lewiuberg/confprint?color=blue)](https://app.codecov.io/gh/lewiuberg/confprint)
![Github Contributors](https://img.shields.io/github/contributors/lewiuberg/confprint?color=blue)
![GitHub search hit counter](https://img.shields.io/github/search/lewiuberg/confprint/confprint?label=confprint%20searches)
[![GitHub issues](https://img.shields.io/github/issues-raw/lewiuberg/confprint)](https://github.com/lewiuberg/confprint/issues)
![GitHub last commit](https://img.shields.io/github/last-commit/lewiuberg/confprint)

[![CICD](https://github.com/lewiuberg/confprint/actions/workflows/cicd.yml/badge.svg)](https://github.com/lewiuberg/confprint/actions/workflows/cicd.yml)

Copyright 2021 [Lewi Lie Uberg](https://uberg.me/)\
_Released under the MIT license_

**ConfPrint** provides a simple way to make predefined printer configurations.

## Contents <!-- omit in toc -->

- [Citation](#citation)
  - [APA](#apa)
  - [BibTex](#bibtex)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Using Poetry](#using-poetry)
- [Usage](#usage)
  - [prefix_printer](#prefix_printer)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Citation

Please see [CITATION.cff](CITATION.cff) for the full citation information.

### APA

```apa
Lie Uberg, L., & Hjelle, G. A. (2021). confprint (Version 0.2.3) [Computer software]. https://github.com/lewiuberg/confprint
```

### BibTex

```BibTex
@software{Lie_Uberg_confprint_2021,
author = {Lie Uberg, Lewi and Hjelle, Geir Arne},
license = {MIT},
month = {10},
title = {{confprint}},
url = {https://github.com/lewiuberg/confprint},
version = {0.2.3},
year = {2021}
}
```

## Prerequisites

[Click](https://pypi.org/project/click/)

Please see [pyproject.toml](pyproject.toml) for the full citation information.

## Installation

### Using pip

```bash
python -m pip install confprint
```

### Using Poetry

```bash
poetry add confprint
```

## Usage

### prefix_printer
<!-- #endregion -->

```python
from confprint import prefix_printer

p_test1 = prefix_printer(prefix="test1")
p_test1("Preset\n")

p_test2 = prefix_printer(prefix="test2", upper=False)
p_test2("unaltered text\n")

p_test3 = prefix_printer(prefix="test3", stderr=True)
p_test3("using sys.stderr.write as the print function\n")

p_test4 = prefix_printer(prefix="test4", click=True)
p_test4("using click.echo as the print function\n")

p_test5 = prefix_printer(prefix="test5", frame_left="( ", frame_right=" )")
p_test5("using custom frame characters\n")

p_test6 = prefix_printer(prefix="test6", counter_start=1)
p_test6("By defining a 'counter_start',")
p_test6("a counter number will be appended")
p_test6("to the prefix.\n")

p_test1(
    """With new lines in strings the text is converted
to multiline, then all but the first are
indented to line up with the rest.\n"""
)

p_test1(
    "The next example wil not be ending with a `:`, "
    "since it has no input.\nAnd as you can see, this is also a multiline text.\n"
)

p_done = prefix_printer(prefix="done")
p_done()
```

```
[TEST1]: Preset

[test2]: unaltered text

[TEST3]: using sys.stderr.write as the print function

[TEST4]: using click.echo as the print function
         
( TEST5 ): using custom frame characters
           
[TEST6:1]: By defining a 'counter_start',
[TEST6:2]: a counter number will be apended
[TEST6:3]: to the prefix.
           
[TEST1]: With new lines in strings the text is converted
         to multiline, then all but the first are
         indented to line up with the rest.
         
[TEST1]: The next example wil not be ending with a `:`, since it has no input.
         And as you can see, this is also a multiline text.
         
[DONE]
```


## Authors

- **[Lewi Lie Uberg](https://github.com/lewiuberg)** - [uberg.me](https://uberg.me/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/lewiuberg/confprint/blob/main/LICENSE) file for details

## Acknowledgments

- [Geir Arne Hjelle](https://github.com/gahjelle), for his presentation on 'Introduction to Decorators' given at [PyCon 21](https://www.youtube.com/watch?v=VWZAh1QrqRE&amp;t=17m0s)
