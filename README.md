# Interpretador-Python

Considerando a seguinte linguagem:

```python
Expr ::= Expr '+' Expr

           | Expr '-' Expr

           | Expr '*' Expr

           | Expr '/' Expr

           | ID '=' Expr ';'

           | ID

          | NUM
          
```

Onde ID representa um nome de variável. Por simplicidade, o ID pode ser qualquer letra entre 'a-A' e 'z-Z'

Num representa um valor numérico.

Eis um exemplo de um programa feito nesta linguagem:

```python

a = 10;

b = 20;

c = 2*a + b;

c
```

Onde 'c' imprime o valor contido na pilha refênte à variável 'c'
