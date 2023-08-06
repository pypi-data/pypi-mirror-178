# import export
## декоратор методов и классов модуля, которые необходимо "экспортировать"

* работает очень просто: заполняет внутреннюю переменную `__all__`
* сам не импортируется в область видимости модуля
* использует только `sys`
* запускается во всех версиях питона (кажется)
* написано в [Чудо-Тексте](https://cudatext.github.io/) :: https://github.com/Alexey-T/CudaText/
* по методу stackoverflow-programming https://stackoverflow.com/q/44834
* конкурент и первоисточник [export](https://pypi.org/project/export/0.1.2/) подсмотрел логику и переписал проект


```bash
pip install import-export
```

```python
"""mypack.py"""
import export

def fee():
    return 'twee'
	
@export
def moo():
    return 'moow'
```

```python
> from mypack import *
> print(fee())
NameError: name 'fee' is not defined
> print(moo())
moow
```


![Lines of code](https://img.shields.io/tokei/lines/github/ablaternae/py-export)
![Downloads](https://img.shields.io/pypi/dm/import-export)
[![Statistic](https://pepy.tech/badge/import-export/week)](https://pepy.tech/project/import-export)
![GitHub](https://img.shields.io/github/license/ablaternae/py-export)
