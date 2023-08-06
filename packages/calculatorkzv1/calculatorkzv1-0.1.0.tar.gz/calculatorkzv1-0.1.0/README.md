# calculatorkzv1

`calculatorkzv1` is the package of automated calculator and performing simple arritmetics operations like <i>addition, subtraction, multiplication, division and n-root</i>.


## Installation

```sh
pip install calculatorkzv1
```

## How to use

### Automated calculator

Call automated calculator and package functions:

```python
>>> from calculatorkzv1.calculatorkzv1 import Calculator, calculator
>>> calculator()
Select operation: 
 0. Exit 
 1. Add 
 2. Subtract 
 3. Multiply 
 4. Divide 
 5. Take (n) root 
 6. Reset calculator
Enter choice (0/1/2/3/4/5/6):
```

After imported package function `calculator()` initiates automated calculator, which asks you select one of the action/operation you would like to be performed. Thus, enter the choise - integer number from 0 to 6. Then you will be asked to enter the number you want operation would be applied to.

Automated calculator has memory, which at the begining starts from 0. But after the operation and number entering it accumulates,
e.g. `0 + 2 = 2, 2*3 = 6, 6/2=3`, etc.

The memory can be reseted after selection of 6.

To keep the calculation further enter `yes`, to end calculation answer `no`. Exit calculation can be by entering 0 on the choise selections step.

For examples:

```python
>>> calculator()
Select operation: 
 0. Exit 
 1. Add 
 2. Subtract 
 3. Multiply 
 4. Divide 
 5. Take (n) root 
 6. Reset calculator
Enter choice (0/1/2/3/4/5/6): 1
Enter your number: 2
Result: 0.0 + 2.0 = 2.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 3
Enter your number: 3
Result: 2.0 * 3.0 = 6.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 2
Enter your number: 4
Result: 6.0 - 4.0 = 2.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 6
Reset to: 0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 5
Enter your number: 9
Result: 0.0 ^(1/9.0) = 0.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 1
Enter your number: 9
Result: 0.0 + 9.0 = 9.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 5
Enter your number: 2
Result: 9.0 ^(1/2.0) = 3.0
Let's do next calculation? (yes/no): yes
Enter choice (0/1/2/3/4/5/6): 4
Enter your number: 2
Result: 3.0 / 2.0 = 1.5
Let's do next calculation? (yes/no): no
Final result =  1.5
```

### Calculator class methods

In this package you can allso use class methods, e.g.

- Create the object of two values:
```python
>>> x1 = 2
>>> x2 = 3
>>> obj = Calculator(x1,x2)
>>> obj
<calculatorkz.Calculator object at 0x101b6dde0>
```
- Add them:
```python
>>> obj.add()
5
```

- Substract two values:
```python
>>> obj.subtract()
-1
```

- Multiply two values:
```python
>>> obj.multiply()
6
```

- Divide them:
```python
>>> obj.divide()
0.6666666666666666
```

- Take x2 root from x1:
```python
>>> obj.n_root()
1.2599210498948732
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
