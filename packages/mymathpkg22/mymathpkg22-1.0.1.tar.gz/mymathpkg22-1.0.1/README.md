# My Math package 2022

This is a project work Python Mastery for Turing college's Data Wrangling with Python module. The purpose of this package is to practise OOP-based coding, testing and creating Python package.

The package is a simple calculator that has addition, substraction, multiplication, division, nth root of a number and reset functions. The calculator used float data-type in input and output values.

After initalizing a new calculator-object, the object will start with a value zero. All the operations are done for this value that is stored in the object.

---

## Setup

```
>>>pip install mymathpkg22
```

---

## Sample Execution

Start the calculator with importing the calculator module and initalizing the calculator-object.

```
>>>from mymathpkg22 import calculator
>>>new_calculator_object = calculator.Calculator()
```

Adding two.

```
>>> new_calculator_object.add(2)
2.0
```

Subtracting three.

```
>>> new_calculator_object.subtract(3)
-1.0
```

Dividing with two.

```
>>> new_calculator_object.divide(2)
-0.5
```
