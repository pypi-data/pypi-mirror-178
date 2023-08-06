# Modularizador

Instale com
> !pip install modularizador

Ap&oacute;s importado no Jupyter Notebook, permite importar arquivos .ipynb como se fossem arquivos .py, inclusive os que est&atilde;o em subpastas.

Exemplo de uso:
1. Crie um arquivo chamado **somador.ipynb** e coloque ele dentro de uma subpasta chamada **pacotes**.
2. Crie uma fun&#x00E7;&atilde;o chamada soma dentro do arquivo somador.ipynb:

```python
def soma(a, b):
    return a + b
```
3. Agora &eacute; s&oacute; importar o modularizador e voc&ecirc; poder&aacute; importar tamb&eacute;m o somador.ipynb:

```python
import modularizador
from pacotes import somador
somador.soma(2, 3)
>>> 5
```

O c&oacute;digo utilizado nesta biblioteca para obter o resultado acima foi extra&iacute;do [desta p&aacute;gina](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html) da documenta&#x00E7;&atilde;o do Jupyter Notebook. 
Daqui para baixo vamos nos referir a ele como *o script*, ou como *modularizador.py*.
---
A biblioteca modularizador conta ainda com 3 fun&#x00E7;&otilde;es &uacute;teis: **ativa()**, **desativa()** e **status_startup()**.
* ##### ativa()

```python
import modularizador
modularizador.ativa()
```
Insere *o script* na pasta startup do ipython, tornando desnecess&aacute;rio importar a biblioteca modularizador a partir das pr&oacute;ximas vezes que voc&ecirc; abrir um projeto. O efeito durar&aacute; enquanto *modularizador.py* estiver na pasta startup, portanto fechar seu Jupyter Notebook n&atilde;o o desfar&aacute;. 

No exemplo anterior, se voc&ecirc; j&aacute; tivesse, em algum momento do passado, realizado o procedimento de ativa&#x00E7;&atilde;o logo acima, poderia, em seu novo projeto importar pacotes/somador.ipynb sem a necessidade de importar o modularizador. Simplesmente assim:
```python
from pacotes import somador
somador.soma(2, 3)
>>> 5
```
* ##### desativa()
```python
import modularizador
modularizador.desativa()
```
Remove *o script modularizador.py* da pasta startup do ipyton, tirando do seu Jupyter Notebook a capacidade de importar arquivos .ipynb sem importar manualmente o modularizador em cada projeto.

* ##### status_startup()
```python
import modularizador
modularizador.status_startup()
```
Apenas informa se *o script modularizador.py* est&aacute; na pasta startup do ipyton. I.e., se est&aacute; ou n&atilde;o ativo o recurso que permite a importa&#x00E7;&atilde;o de arquivos .ipynb sem a necessidade de importar a biblioteca modularizador explicitamente em cada projeto.