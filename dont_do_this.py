import marimo

__generated_with = "0.8.22"
app = marimo.App(
    width="medium",
    app_title="Don't do this",
    layout_file="layouts/dont_do_this.slides.json",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from PIL import Image, ImageDraw
    import math
    import random

    def normalize(vx, vy, vz):
        length = math.sqrt(vx * vx + vy * vy + vz * vz)
        if length == 0:
            return (0, 0, 0)
        return (vx / length, vy / length, vz / length)


    def draw_jagged_grid(
        width=800,
        height=800,
        spacing=40,
        cx=400,
        cy=400,
        radius=200,
        max_displacement=15,
        bg_color="white",
        line_color="black",
        line_width=2,
        frame_width=0,
        seed=42,
    ):
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        rng = random.Random(seed)

        xs = list(range(-spacing, width + spacing * 2, spacing))
        ys = list(range(-spacing, height + spacing * 2, spacing))

        grid = {}
        for xi, x in enumerate(xs):
            for yi, y in enumerate(ys):
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                if dist < radius:
                    strength = 1 - dist / radius
                    grid[(xi, yi)] = (
                        x + rng.uniform(-max_displacement, max_displacement) * strength,
                        y + rng.uniform(-max_displacement, max_displacement) * strength,
                    )
                else:
                    grid[(xi, yi)] = (x, y)

        # ----------------------------
        # LIGHTING / SHADING
        # ----------------------------
        light_dir = normalize(-1, -1, 1)  # light from top-left

        for xi in range(len(xs) - 1):
            for yi in range(len(ys) - 1):
                p1 = grid[(xi, yi)]
                p2 = grid[(xi + 1, yi)]
                p3 = grid[(xi + 1, yi + 1)]
                p4 = grid[(xi, yi + 1)]

                # Base vectors
                v1 = (p2[0] - p1[0], p2[1] - p1[1], 0)
                v2 = (p4[0] - p1[0], p4[1] - p1[1], 0)

                # Fake height from displacement
                z1 = (p1[0] - xs[xi]) + (p1[1] - ys[yi])
                z2 = (p2[0] - xs[xi + 1]) + (p2[1] - ys[yi])
                z4 = (p4[0] - xs[xi]) + (p4[1] - ys[yi + 1])

                v1 = (v1[0], v1[1], z2 - z1)
                v2 = (v2[0], v2[1], z4 - z1)

                # Cross product → normal
                nx = v1[1] * v2[2] - v1[2] * v2[1]
                ny = v1[2] * v2[0] - v1[0] * v2[2]
                nz = v1[0] * v2[1] - v1[1] * v2[0]

                nx, ny, nz = normalize(nx, ny, nz)

                # Dot product → brightness
                brightness = nx * light_dir[0] + ny * light_dir[1] + nz * light_dir[2]

                # Map to grayscale
                shade = int(200 + 50 * brightness)
                shade = max(0, min(255, shade))

                color = (shade, shade, shade)

                draw.polygon([p1, p2, p3, p4], fill=color)

        # ----------------------------
        # GRID LINES ON TOP
        # ----------------------------
        for yi in range(len(ys)):
            points = [grid[(xi, yi)] for xi in range(len(xs))]
            draw.line(points, fill=line_color, width=line_width)

        for xi in range(len(xs)):
            points = [grid[(xi, yi)] for yi in range(len(ys))]
            draw.line(points, fill=line_color, width=line_width)

        if frame_width > 0:
            half = frame_width // 2
            draw.rectangle(
                [half, half, width - 1 - half, height - 1 - half],
                outline=line_color,
                width=frame_width,
            )

        return img

    return Image, ImageDraw, draw_jagged_grid, math, normalize, random


@app.cell
def __(draw_jagged_grid):
    jagged_image = draw_jagged_grid(width=1200, height=1200, cx=900, cy=900, radius=320, max_displacement=35, frame_width=6, spacing=80)
    return (jagged_image,)


@app.cell
def __(jagged_image):
    jagged_image.save('images/cover.png')
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(
            """
            #**Don't Do That!**
            ###Avoiding Anti-Patterns in Python
            """
        ),
        mo.image(
                    src='images/cover.png',
                    width=400,
                    height=400,
                    rounded=True
                ),
        mo.md(
          """##Dario Ruben Scanferlato
            ###<center>PyCon Italia 2026</center>"""
        )],
        align='center',
        gap=5
    )
    return


@app.cell
def __():
    return


@app.cell
def _(mo):
    mo.md(
        """
        # About me
        - Data Scientist & Engineer
        - Currently developing anomaly detection and simulation tools for gas turbines using Python
        - MSc in Engineering and Management at Politecnico di Torino
        - Organizer of the Python Torino user group
        - Talk to me about guitar, chess, and open-source
        """
    )
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    from datetime import datetime

    # Data
    dates = [datetime(2026, 5, 29), datetime(2026, 5, 30)]
    presentations = [0, 1]

    # Create figure
    plt.figure(figsize=(10, 6))

    # Plot line
    plt.plot(dates, presentations, marker='o')

    # Labels and title
    plt.title("Number of presentations I've given at PyCon")
    plt.xlabel("Date")
    plt.ylabel("Presentations")
    plt.xticks(dates, ["May 29, 2026", "May 30, 2026"])

    plt.grid(True)
    plt.show()
    return dates, datetime, plt, presentations


@app.cell
def _(mo):
    mo.md(
        """
        # Agenda

        - Introduce design patterns and anti-patterns
        - How to spot and address anti-patterns
        - Examples of Python anti-patterns
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # Design patterns
        > ###Design patterns are typical solutions to recurring problems in software design. Each pattern is a blueprint you can adapt to solve a particular design problem in your code.
        <p align="center">
        <img src="https://m.media-amazon.com/images/I/81IGFC6oFmL._SL1500_.jpg" alt="Design Patterns book cover" width="400"/>

        </p>
        """
    )
    return


@app.cell
def _(mo):
    mo.vstack(
        [
            mo.md("#Design patterns"),
            mo.hstack(
                [mo.image(src="images/anti patterns catalog.png", width=1200, rounded=True)],
                justify="center"
            ),
            mo.md("[Source: refactoring.guru](https://refactoring.guru/design-patterns/catalog)")
        ],
        align="center",
        gap=5
    )
    return


@app.cell
def _(mo):
    mo.hstack(
        [
            mo.vstack([
                mo.md(r"""
    # Anti-patterns
    An *anti-pattern* is a solution to a class of problem which may be commonly used but is likely to be ineffective or counterproductive. 
    ### Anti-patterns lead to:
    * Bad Performance
    * Unreadable code
    * Unreliability / unexpected behaviors
    * Slower development process
    """)
            ]),

            mo.image(
                src="https://m.media-amazon.com/images/I/51Jc+OkE2dL._UF1000,1000_QL80_.jpg",
                width=600,
                rounded=True
            )
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Examples of anti-patterns in software programming
        - ###**God object**: A single class handles all control in a program rather than control being distributed across multiple classes.
        - ### **Magic number**: A literal value with an important yet unexplained meaning which could be replaced with a named constant.
        - ###**Big Ball of Mud**: A software system that lacks a perceivable architecture.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        #Anti-patterns in Python
        - Python is a flexible language that allows us to achieve our programming goals in many different ways
        - This flexibility can be a double-edged sword
        - According to the Zen of Python, there should only be one obvious way to fix a problem
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        #How do we avoid anti-patterns in Python?
        - Use a static code analysis tools ()
        - Be aware of common mistakes
        - Improve your general programming knowledge (data structures, algorithms, principles, patterns)
        - Learn more about your modules - either built-in or external
        - Ask an expert (or use an LLM) to review your code
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""# Automatic code analysis tools""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        <style>
        pre {
            background-color: #1e1e1e !important;
            color: #d4d4d4 !important;
            padding: 12px;
            border-radius: 8px;
        }
        </style>
        #Setting up an automated linter

        Step 1: Install pre-commit
        ```bash
        pip install pre-commit
        ```
        Step 2: Create .pre-commit-config.yaml
        ```bash
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.5.0
            hooks:
              - id: ruff
              - id: ruff-format
        ```
        Step 3: Enable pre-commit
        ```bash
        pre-commit install
        ```
        """
    )
    return


@app.cell
def _(mo):
    antipattern_topics = mo.ui.dropdown(
        options=[
            "Mutable Default Arguments",
            "Using type() instead of isinstance()",
            "Bare except Clauses",
            "Not Using Context Managers",
            "String Concatenation in Loops",
            "Checking len() Instead of Truthiness",
            "Using list as a Stack or Queue",
            "Overusing Global Variables",
            "Not Using Enumerate",
            "Returning None Implicitly vs Explicitly",
        ],
        value="Mutable Default Arguments",
        label="📚 Choose an Antipattern",
        full_width=True,
    )
    return (antipattern_topics,)


@app.cell
def _():
    antipatterns = {
        "Mutable Default Arguments": {
            "emoji": "🪤",
            "description": """
    **Mutable default arguments** (like lists or dicts) are created **once** when the function is defined,
    not each time it is called. This leads to shared state across calls — a very subtle bug.
            """,
            "bad_code": '''\
    # ❌ Antipattern: mutable default argument
    def append_to(element, target=[]):
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [1, 2]  <-- Unexpected!
    print(append_to(3))   # [1, 2, 3] <-- The list keeps growing!
    ''',
            "good_code": '''\
    # ✅ Fix: use None as the default, create inside the function
    def append_to(element, target=None):
        if target is None:
            target = []
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [2]  ✓
    print(append_to(3))   # [3]  ✓
    ''',
            "tip": "💡 Use `None` as the default for any mutable argument, then initialize it inside the function body.",
        },
        "Using type() instead of isinstance()": {
            "emoji": "🔍",
            "description": """
    Using `type(x) == SomeType` breaks **polymorphism** and ignores subclasses.
    `isinstance()` respects inheritance and is the Pythonic way to check types.
            """,
            "bad_code": '''\
    # ❌ Antipattern: using type() for type checking
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if type(dog) == Animal:  # False — misses subclasses!
        print("It's an animal")
    else:
        print("Not recognized as an animal")
    ''',
            "good_code": '''\
    # ✅ Fix: use isinstance() to respect inheritance
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if isinstance(dog, Animal):  # True — correctly identifies subclass
        print("It's an animal ✓")
    ''',
            "tip": "💡 Prefer `isinstance()` for type checks. It works correctly with subclasses and abstract base classes.",
        },
        "Bare except Clauses": {
            "emoji": "🚨",
            "description": """
    A **bare `except:`** clause catches *everything*, including `SystemExit`, `KeyboardInterrupt`,
    and `GeneratorExit`. This can swallow critical errors and make debugging nearly impossible.
            """,
            "bad_code": '''\
    # ❌ Antipattern: bare except catches everything, even Ctrl+C!
    try:
        result = 10 / 0
    except:
        print("Something went wrong")  # What went wrong? No idea.
    ''',
            "good_code": '''\
    # ✅ Fix: catch specific exceptions
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Math error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        # At minimum, use Exception (excludes system-exiting exceptions)
        print(f"Unexpected error: {e}")
        raise  # Re-raise if you can't handle it
    ''',
            "tip": "💡 Always catch specific exceptions. At minimum use `except Exception`, and always log or re-raise.",
        },
        "Not Using Context Managers": {
            "emoji": "📂",
            "description": """
    Manually managing resources (files, DB connections, locks) is error-prone.
    If an exception occurs before `.close()`, the resource **leaks**.
    **Context managers** (`with` statements) guarantee cleanup.
            """,
            "bad_code": '''\
    # ❌ Antipattern: manual resource management
    f = open("data.txt", "w")
    f.write("hello")
    # If an exception occurs here, f.close() is never called!
    f.close()
    ''',
            "good_code": '''\
    # ✅ Fix: use a context manager — file is always closed
    with open("data.txt", "w") as f:
        f.write("hello")
    # f is automatically closed here, even if an exception occurs

    # You can also write your own context managers:
    from contextlib import contextmanager

    @contextmanager
    def managed_resource():
        print("Acquiring resource")
        try:
            yield "resource"
        finally:
            print("Releasing resource")  # Always runs

    with managed_resource() as r:
        print(f"Using {r}")
    ''',
            "tip": "💡 Use `with` statements for files, database connections, locks, and any resource that needs cleanup.",
        },
        "String Concatenation in Loops": {
            "emoji": "🔗",
            "description": """
    Strings in Python are **immutable**. Each `+=` creates a brand-new string object,
    copying all previous content. In a loop, this results in **O(n²)** time complexity.
            """,
            "bad_code": '''\
    # ❌ Antipattern: O(n²) string concatenation in a loop
    words = ["Python", "is", "awesome", "and", "fast"]

    result = ""
    for word in words:
        result += word + " "   # Creates a new string every iteration!

    print(result.strip())
    ''',
            "good_code": '''\
    # ✅ Fix 1: use str.join() — O(n) and idiomatic
    words = ["Python", "is", "awesome", "and", "fast"]
    result = " ".join(words)
    print(result)

    # ✅ Fix 2: collect into a list, then join
    parts = []
    for word in words:
        parts.append(word.upper())
    result2 = " ".join(parts)
    print(result2)

    # ✅ Fix 3: use a list comprehension + join
    result3 = " ".join(w.upper() for w in words)
    print(result3)
    ''',
            "tip": "💡 Use `str.join()` to concatenate strings. It is O(n) and far more readable than repeated `+=`.",
        },
        "Checking len() Instead of Truthiness": {
            "emoji": "📏",
            "description": """
    In Python, empty containers (`[]`, `{}`, `""`, `()`) are **falsy** by default.
    Checking `len(x) == 0` is verbose and not Pythonic. Just use the object directly in a boolean context.
            """,
            "bad_code": '''\
    # ❌ Antipattern: explicitly checking length
    my_list = []

    if len(my_list) == 0:
        print("List is empty")

    if len(my_list) > 0:
        print("List has items")

    # Also bad: len(x) != 0
    ''',
            "good_code": '''\
    # ✅ Fix: leverage Python's truthiness
    my_list = []

    if not my_list:
        print("List is empty ✓")

    my_list = [1, 2, 3]
    if my_list:
        print("List has items ✓")

    # Works for dicts, sets, strings, tuples too!
    my_dict = {}
    if not my_dict:
        print("Dict is empty ✓")
    ''',
            "tip": "💡 Python containers implement `__bool__` or `__len__`. Trust the truthiness model — it's faster and more readable.",
        },
        "Using list as a Stack or Queue": {
            "emoji": "📦",
            "description": """
    `list.pop(0)` (removing from the front) is **O(n)** because every element must be shifted.
    For queue (FIFO) operations, use `collections.deque`, which supports O(1) appends and pops from both ends.
            """,
            "bad_code": '''\
    # ❌ Antipattern: using a list as a queue (O(n) per dequeue)
    queue = []
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    while queue:
        item = queue.pop(0)  # O(n) — shifts all remaining elements!
        print(f"Processing: {item}")
    ''',
            "good_code": '''\
    # ✅ Fix: use collections.deque for queues
    from collections import deque

    queue = deque()
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    while queue:
        item = queue.popleft()  # O(1) ✓
        print(f"Processing: {item}")

    # For stacks (LIFO), a plain list is actually fine:
    stack = []
    stack.append("a")
    stack.append("b")
    top = stack.pop()   # O(1) — popping from the end is fast
    ''',
            "tip": "💡 Use `list` for stacks (LIFO), `collections.deque` for queues (FIFO), and `heapq` for priority queues.",
        },
        "Overusing Global Variables": {
            "emoji": "🌐",
            "description": """
    Global variables create **hidden dependencies** between functions, making code hard to test,
    debug, and reason about. Functions that rely on globals are not self-contained.
            """,
            "bad_code": '''\
    # ❌ Antipattern: relying on and mutating global state
    counter = 0

    def increment():
        global counter
        counter += 1

    def reset():
        global counter
        counter = 0

    increment()
    increment()
    print(counter)  # 2 — but any function anywhere can change this!
    ''',
            "good_code": '''\
    # ✅ Fix 1: pass state as parameters and return results
    def increment(counter):
        return counter + 1

    def reset():
        return 0

    counter = 0
    counter = increment(counter)
    counter = increment(counter)
    print(counter)  # 2 ✓

    # ✅ Fix 2: encapsulate state in a class
    class Counter:
        def __init__(self):
            self._value = 0

        def increment(self):
            self._value += 1

        def reset(self):
            self._value = 0

        @property
        def value(self):
            return self._value

    c = Counter()
    c.increment()
    c.increment()
    print(c.value)  # 2 ✓
    ''',
            "tip": "💡 Pass state explicitly as function arguments. If you need shared state, encapsulate it in a class.",
        },
        "Not Using Enumerate": {
            "emoji": "🔢",
            "description": """
    Manually managing an index variable alongside a loop is verbose and error-prone.
    Python's built-in `enumerate()` gives you both the index and the value cleanly.
            """,
            "bad_code": '''\
    # ❌ Antipattern: manual index tracking
    fruits = ["apple", "banana", "cherry"]

    i = 0
    for fruit in fruits:
        print(f"{i}: {fruit}")
        i += 1

    # Also bad: range(len(...))
    for i in range(len(fruits)):
        print(f"{i}: {fruits[i]}")
    ''',
            "good_code": '''\
    # ✅ Fix: use enumerate()
    fruits = ["apple", "banana", "cherry"]

    for i, fruit in enumerate(fruits):
        print(f"{i}: {fruit}")

    # You can also set the start index
    for i, fruit in enumerate(fruits, start=1):
        print(f"{i}. {fruit}")
    ''',
            "tip": "💡 Prefer `enumerate()` over `range(len(...))`. It's more readable and less error-prone.",
        },
        "Returning None Implicitly vs Explicitly": {
            "emoji": "🕳️",
            "description": """
    Functions that sometimes return a value and sometimes return `None` implicitly
    create confusing APIs. Be explicit about what a function returns — always.
            """,
            "bad_code": '''\
    # ❌ Antipattern: inconsistent return values
    def find_user(users, name):
        for user in users:
            if user["name"] == name:
                return user
        # Implicitly returns None — caller may not realize this!

    users = [{"name": "Alice"}, {"name": "Bob"}]
    result = find_user(users, "Charlie")
    print(result["name"])  # 💥 TypeError: NoneType has no attribute 'name'
    ''',
            "good_code": '''\
    # ✅ Fix 1: return None explicitly and document it
    def find_user(users, name):
        """Returns user dict or None if not found."""
        for user in users:
            if user["name"] == name:
                return user
        return None  # Explicit is better than implicit

    users = [{"name": "Alice"}, {"name": "Bob"}]
    result = find_user(users, "Charlie")
    if result is not None:
        print(result["name"])
    else:
        print("User not found")

    # ✅ Fix 2: raise an exception for truly unexpected absence
    def get_user(users, name):
        for user in users:
            if user["name"] == name:
                return user
        raise ValueError(f"User {name!r} not found")
    ''',
            "tip": "💡 Always return explicitly. Consider raising exceptions for error cases instead of returning `None`.",
        },
    }
    return (antipatterns,)


@app.cell
def _(antipattern_topics, antipatterns, mo):
    selected = antipatterns[antipattern_topics.value]

    mo.vstack([
        antipattern_topics,
        mo.md(f"## {selected['emoji']} {antipattern_topics.value}"),
        mo.md(selected["description"]),
        mo.tabs({
            "❌ Antipattern": mo.md(f"```python\n{selected['bad_code']}\n```"),
            "✅ Fix": mo.md(f"```python\n{selected['good_code']}\n```"),
        }),
        mo.callout(mo.md(selected["tip"]), kind="info"),
    ])
    return (selected,)


@app.cell
def _(mo):
    mo.md(
        """
        ---
        ## 📋 Quick Reference Table

        | Antipattern | Risk | Fix |
        |---|---|---|
        | Mutable default args | Hidden shared state | Use `None` as default |
        | `type()` checks | Breaks subclassing | Use `isinstance()` |
        | Bare `except:` | Swallows all errors | Catch specific exceptions |
        | Manual resource mgmt | Resource leaks | Use `with` statement |
        | String `+=` in loops | O(n²) performance | Use `str.join()` |
        | `len(x) == 0` checks | Verbose, un-Pythonic | Use truthiness directly |
        | `list.pop(0)` as queue | O(n) dequeue | Use `collections.deque` |
        | Global variables | Hidden dependencies | Pass args or use a class |
        | `range(len(...))` loops | Verbose, error-prone | Use `enumerate()` |
        | Implicit `None` returns | Confusing API | Return explicitly or raise |

        ---
        > 💬 *"Code is read more often than it is written."* — Guido van Rossum
        """
    )
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(""" """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
