---
marp: false
theme: gaia
---

# Don't Do That
Avoiding Anti-Patterns in Python

PyCon Italia 2026

---

# About me
- Freelance Data Scientist & Engineer
- Currently developing anomaly detection and simulation tools for gas turbines using Python
- MSc in Engineering and Management at Politecnico di Torino
- Organizer of the Python Torino user group
- Talk to me about guitar, chess, and open-source

---

# Agenda

- Explain what code patterns and anti-patterns are
- How to spot and address anti-patterns
- Examples of Python anti-patterns


---

# Design patterns
![bg right 75%](https://m.media-amazon.com/images/I/81IGFC6oFmL._SL1500_.jpg)
- Design patterns are typical solutions to recurring problems in software design. Each pattern is a blueprint you can adapt to solve a particular design problem in your code.
---

# Design patterns
![bg 70%](images/anti%20patterns%20catalog.png)


[Source: refactoring.guru](https://refactoring.guru/design-patterns/catalog)

---
# Anti-patterns
An anti-pattern is a solution to a class of problem which may be commonly used but is likely to be ineffective or counterproductive. 

Anti-patterns generally hurt:
- Performance
- Readability
- Reliability
- Development process

---
# Anti-patterns in software programming
- God object:
A single class handles all control in a program rather than control being distributed across multiple classes.
- Magic number:
A literal value with an important yet unexplained meaning which could be replaced with a named constant.
- Big Ball of Mud:
A software system that lacks a perceivable architecture.
---
# Example of an anti-pattern

```python
# Listing elements by their index
fruits = ['apple', 'banana', 'cherry']
for i in range(len(fruits)):
    print(i, fruits[i])

for i, fruit in enumerate(fruits):
    print(i, fruit)

# Iterating over multiple lists
for i in range(len(names)):
    print(names[i], scores[i])

for name, score in zip(names, scores):
    print(name, score)
```
---
# How do we avoid writing anti-patterns in Python?
- Use linters
- Improve your knowledge of the language
- Improve your knowledge of data structures
---
# Linting and style checks
- mutable default argument
---
# Little book of Python anti-patterns
---
# Loops

---

## List comprehensions
- Use them when it can fit in one line
- You don't always have to use them inside a list

```python
# Anti-pattern: manual append loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# Pythonic: list comprehension
squares = [x ** 2 for x in range(10)]

# No need for a list — use a generator expression
total = sum(x ** 2 for x in range(10))
unique = set(x % 3 for x in range(10))
```
---

# Using appropriate data structures
![alt text](image.png)
- What operations are you going to do on the data? Use an appropriate data structure accordingly
---

# Performance
- Readability counts
- 

---

# Optimizing before measuring

```python
import cProfile

def slow_function():
    return sum(i ** 2 for i in range(1_000_000))

cProfile.run('slow_function()')
```

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.089    0.089 <string>:1(<module>)
        1    0.054    0.054    0.089    0.089 script.py:3(slow_function)
  1000001    0.035    0.000    0.035    0.000 script.py:4(<genexpr>)
```

---
# Reliability
---
# type vs. isinstance

```python
# Anti-pattern: type() breaks with subclasses
class Animal: pass
class Dog(Animal): pass

dog = Dog()
print(type(dog) == Animal)       # False — unexpected!
print(isinstance(dog, Animal))   # True

# isinstance also accepts a tuple of types
class Cat(Animal): pass

print(isinstance(dog, (Dog, Cat)))  # True
```
---
# Returning None in a function

```python
# Anti-pattern: silent None return
def find_user(users, name):
    for user in users:
        if user['name'] == name:
            return user
    # Implicitly returns None — caller may not handle it

result = find_user(users, 'ghost')
print(result['email'])  # AttributeError: 'NoneType' ...

# Better: raise an explicit exception
def find_user(users, name):
    for user in users:
        if user['name'] == name:
            return user
    raise ValueError(f"User '{name}' not found")
```
---
# Not using a context manager

```python
# Anti-pattern: manual resource management
f = open('data.txt', 'r')
data = f.read()
f.close()  # Never runs if an exception is raised!

# Pythonic: context manager guarantees cleanup
with open('data.txt', 'r') as f:
    data = f.read()

# Works for DB connections, locks, network sockets...
with sqlite3.connect('db.sqlite') as conn:
    conn.execute('SELECT * FROM users')
```
---
# Mutable default argument

```python
# Anti-pattern: mutable default is shared across calls
def append_item(item, lst=[]):
    lst.append(item)
    return lst

print(append_item(1))  # [1]
print(append_item(2))  # [1, 2]  ← unexpected!
print(append_item(3))  # [1, 2, 3]  ← same list reused

# Fix: use None as sentinel
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```
---

# Data Science examples

---

# Chaining pandas operations

```python
# Anti-pattern: intermediate variables
df1 = df[df['age'] > 18]
df2 = df1.dropna(subset=['email'])
df3 = df2.rename(columns={'name': 'full_name'})
result = df3.reset_index(drop=True)

# Pythonic: method chaining
result = (
    df
    .query('age > 18')
    .dropna(subset=['email'])
    .rename(columns={'name': 'full_name'})
    .reset_index(drop=True)
)
```

---

# Using resample for date aggregations

```python
# Anti-pattern: manual date groupby
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
monthly = df.groupby(['year', 'month'])['value'].sum()
# Result has a MultiIndex — awkward to work with

# Pythonic: resample preserves the DatetimeIndex
df = df.set_index('date')
monthly = df['value'].resample('ME').sum()
weekly_mean = df['value'].resample('W').mean()
```

---

# Vectorized operations

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5])

# Vectorized: operates on the whole array at once
result = data * 2 + 1  # array([3, 5, 7, 9, 11])

# Also works with pandas Series
df['scaled'] = (df['value'] - df['value'].mean()) / df['value'].std()
```

---

# Non-vectorized operations

```python
import numpy as np

data = [1, 2, 3, 4, 5]

# Anti-pattern: Python loop over numeric data
result = []
for x in data:
    result.append(x * 2 + 1)

# Benchmark (1M elements):
# Loop:      ~300ms
# Vectorized: ~3ms  → ~100x faster
```

---
# Summary
- Be aware of common pitfalls in Python programming
- Use linters to avoid common anti-patterns
- Learn how to use language features appropriately
