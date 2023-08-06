![Lines of code](https://img.shields.io/tokei/lines/github/ablaternae/py-tripcode)
![Downloads](https://img.shields.io/pypi/dm/tripcode3)
[![Statistic](https://pepy.tech/badge/tripcode3/week)](https://pepy.tech/project/tripcode3)
[![GitHub](https://img.shields.io/github/license/ablaternae/py-tripcode)](https://github.com/ablaternae/py-tripcode/blob/trunk/LICENSE.md)

This module provides a function to calculate tripcodes:
```bash
pip install -U tripcode3
```
```python
>>> from tripcode import tripcode
>>> tripcode('tea')
'WokonZwxw2'
>>> tripcode(u'ｋａｍｉ')
'yGAhoNiShI'
```

It doesn't use [crypt(3)](https://man7.org/linux/man-pages/man3/crypt.3.html) implementation, but require crossplatform `passlib`

Inspired  by https://pypi.org/project/tripcode/
