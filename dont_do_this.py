import marimo

__generated_with = "0.8.22"
app = marimo.App(
    width="medium",
    app_title="Don't do this",
    layout_file="layouts/dont_do_this.slides.json",
    css_file="custom.css",
)


@app.cell
def imports():
    import math
    import random

    import marimo as mo
    from PIL import Image, ImageDraw

    return Image, ImageDraw, math, mo, random


@app.cell
def slide_definition(mo):
    class AntiPatternSlide:
        def __init__(
            self,
            title,
            good_code,
            bad_code,
            description,
            pattern_id=None,
            tip=None,
            info=None,
        ):
            self.title = title
            self.good_code = good_code
            self.bad_code = bad_code
            self.description = description
            self.pattern_id = pattern_id
            self.tip = tip
            self.info = info

        def _code_block(self, text):
            return mo.md(f"""
    <style>
    pre {{
        background-color: #f3f4f6 !important;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 14px;
        overflow-x: auto;
    }}

    code {{
        font-family: "JetBrains Mono", monospace;
        font-size: 14px;
    }}
    </style>

    ```python
    {text}
    ```
    """)

        def _tip_div(self):
            if self.tip is not None:
                return mo.Html(f"""
    <div style="background:#e8f4fd; border-left:4px solid #3b82f6;
                padding:20px 16px; margin:0; border-radius:4px;">
      💡 {self.tip}
    </div>
    """)
            else:
                return ""

        def _header(self):
            return (
                f"##**{self.pattern_id}** - {self.title}"
                if self.pattern_id
                else f"## {self.title}"
            )

        def display(self):
            return mo.vstack(
                [
                    mo.md(self._header()),
                    mo.md(self.description),
                    mo.ui.tabs(
                        {
                            "❌ Anti-pattern": self._code_block(self.bad_code),
                            "✅ Fix": self._code_block(self.good_code),
                        }
                    ),
                    self._tip_div(),
                ],
                gap=3,
            )

        def _repr_html_(self):
            return self.display().text

    return (AntiPatternSlide,)


@app.cell
def g_1(Image, ImageDraw, math, random):
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

    return draw_jagged_grid, normalize


@app.cell
def __(draw_jagged_grid):
    jagged_image = draw_jagged_grid(
        width=1200,
        height=1200,
        cx=900,
        cy=900,
        radius=320,
        max_displacement=35,
        frame_width=6,
        spacing=80,
    )
    jagged_image.save("images/cover.png")
    return (jagged_image,)


@app.cell
def cover(mo):
    mo.vstack(
        [
            mo.md(
                """
            #**Don't Do That!**
            ###Avoiding Anti-Patterns in Python
            """
            ),
            mo.image(src="images/cover.png", width=400, height=400, rounded=True),
            mo.md(
                """##Dario Ruben Scanferlato
            ###<center>PyCon Italia 2026</center>"""
            ),
        ],
        align="center",
        gap=5,
    )
    return


@app.cell
def __():
    return


@app.cell
def about_me(mo):
    mo.hstack(
        [
            mo.image("images/dario.jpg", width=400, style={"border-radius": "100%"}),
            mo.md(
                """# About me
                - Data Scientist & Engineer
                - Currently developing anomaly detection and simulation tools for gas turbines using Python
                - MSc in Engineering and Management at Politecnico di Torino
                - Organizer of the Python Torino user group
                - Talk to me about guitar, chess, and open-source
                """
            ),
        ],
        gap=10,
    )
    return


@app.cell
def intro_graph():
    from datetime import datetime

    import matplotlib.pyplot as plt

    # Data
    dates = [datetime(2026, 5, 29), datetime(2026, 5, 30)]
    presentations = [0, 1]

    # Create figure
    plt.figure(figsize=(10, 6))

    # Plot line
    plt.plot(dates, presentations, marker="o")

    # Labels and title
    plt.title("Number of presentations I've given at PyCon")
    plt.xlabel("Date")
    plt.ylabel("Presentations")
    plt.xticks(dates, ["May 29, 2026", "May 30, 2026"])

    plt.grid(True)
    plt.show()
    return dates, datetime, plt, presentations


@app.cell
def agenda(mo):
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
def design_patterns_book(mo):
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
def design_patterns_catalogue(mo):
    mo.vstack(
        [
            mo.md("#Design patterns"),
            mo.hstack(
                [
                    mo.image(
                        src="images/anti patterns catalog.png", width=1200, rounded=True
                    )
                ],
                justify="center",
            ),
            mo.md(
                "[Source: refactoring.guru](https://refactoring.guru/design-patterns/catalog)"
            ),
        ],
        align="center",
        gap=5,
    )
    return


@app.cell
def anti_patterns_book(mo):
    mo.hstack(
        [
            mo.vstack(
                [
                    mo.md(r"""
    # Anti-patterns
    An *anti-pattern* is a solution to a class of problem which may be commonly used but is likely to be ineffective or counterproductive.
    ### Anti-patterns lead to:
    * Bad Performance
    * Unreadable code
    * Unreliability / unexpected behaviors
    * Slower development process
    """)
                ]
            ),
            mo.image(
                src="https://m.media-amazon.com/images/I/51Jc+OkE2dL._UF1000,1000_QL80_.jpg",
                width=600,
                rounded=True,
            ),
        ]
    )
    return


@app.cell
def anti_patterns_examples(mo):
    mo.md(
        r"""
        # Examples of anti-patterns in software programming
        - **God object**: A single class handles all control in a program rather than control being distributed across multiple classes.
        - **Magic number**: A literal value with an important yet unexplained meaning which could be replaced with a named constant.
        - **Big Ball of Mud**: A software system that lacks a perceivable architecture.
        """
    )
    return


@app.cell
def anti_patterns_in_python_intro(mo):
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
def __(AntiPatternSlide):
    AntiPatternSlide(
        title="Mutable Default Arguments",
        description="""
    **Mutable default arguments** (like lists or dicts) are created **once** when the function is defined,
    not each time it is called. This leads to shared state across calls — a very subtle bug.
            """,
        bad_code="""
    # ❌ Antipattern: mutable default argument
    def append_to(element, target=[]):
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [1, 2]  <-- Unexpected!
    print(append_to(3))   # [1, 2, 3] <-- The list keeps growing!
    """,
        good_code="""\
    # ✅ Fix: use None as the default, create inside the function
    def append_to(element, target=None):
        if target is None:
            target = []
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [2]  ✓
    print(append_to(3))   # [3]  ✓
    """,
        tip="""Do not use mutable data structures for argument defaults. They are created during function definition time. All calls to the function reuse this one instance of that data structure, persisting changes between them.""",
        pattern_id="B006",
    )
    return


@app.cell
def avoiding_antipatterns(mo):
    mo.md(
        """
        #How do we avoid anti-patterns in Python?
        - Use static code analysis tools (pylint, ruff)
        - Be aware of common mistakes
        - Improve your general programming knowledge (data structures, algorithms, principles, patterns)
        - Learn more about your modules - either built-in or external
        - Ask an expert (or use an LLM) to review your code
        """
    )
    return


@app.cell
def automatic_code_analysis(mo):
    mo.hstack(
        [
            mo.md(
                """# Automatic code analysis tools
    - A linter parses your code into an AST (Abstract Syntax Tree) and then walks that tree looking for nodes that match a known bad pattern. When it finds one, it emits a violation with the rule code, line number, and a message.
    - Linters can be configured enabling rule sets to detect specific types of errors
    - Anti-patterns detected by linters are identified with a code. The code is composed of one (or more) letter(s) that indicates the error category, and a number to differentiate within the category. For example, pylint uses the following:
        - **C** — convention
        - **R** — refactor
        - **W** — warning
        - **E** — error
        - **F** — fatal
        """
            ),
            mo.image(
                src="http://media.makeameme.org/created/linter-and-formatter.jpg",
                width=600,
            ),
        ]
    )
    return


@app.cell
def linter_setup_1(mo):
    mo.md(
        """
        <style>
        pre {
            background-color: #f3f4f6 !important;
            padding: 12px;
            border-radius: 8px;
        }
        code {{
            font-family: "JetBrains Mono", monospace;
            font-size: 14px;
        }}
        </style>
        #Setting up an automated linter
        Configuring a linter is pretty straightforward. I recommend [**ruff**](https://docs.astral.sh/ruff/) as it's very fast and has auto-fix capabilities. We can enable the linter to run every time we commit our code using pre-commit

        Step 1: Install pre-commit and ruff
        ```bash
        pip install pre-commit ruff
        ```
        Step 2: Create .pre-commit-config.yaml
        ```yaml
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
def linter_config(mo):
    mo.hstack(
        [
            mo.md(
                r"""# Configuring linting rules
        - You might want to configure your linter to only enforce specific sets of rules, especially if you're linting a large codebase for the first time
        - This can be done easily by updating your package ```pyproject.toml``` file
        - Note that rule codes may vary across different linters

        ```toml
        [tool.ruff.lint]
        select = [
            "E",
            "W",
            ...
        ]

        ignore = [
            "E501",
            ...
        ]
        ```
        """
            ),
            mo.image("images/done_linting.jpg").center(),
        ],
        gap=5,
        align="center",
    )
    return


@app.cell
def __(AntiPatternSlide):
    AntiPatternSlide(
        title="Bare except clause",
        description="""
    - Handling errors with a **bare `except:`** clause might be dangerous, as this syntax catches all exceptions, including `SystemExit`, `KeyboardInterrupt`, which makes it hard to interrupt the program and can disguise other problems.
    - Both pylint ([W0702](https://pylint.readthedocs.io/en/v3.3.9/user_guide/messages/warning/bare-except.html)) and ruff ([E722](https://docs.astral.sh/ruff/rules/bare-except/)) detect this kind of anti-pattern.
    - This anti-pattern is well-known and some people even proposed to disallow it in Python ([PEP76](https://peps.python.org/pep-0760/))
        """,
        bad_code="""try:
        raise KeyboardInterrupt("You probably don't mean to break CTRL-C.")
    except:
        print("But a bare `except` will ignore keyboard interrupts.")
    """,
        good_code="""try:
        do_something_that_might_break()
    except MoreSpecificException as e:
        handle_error(e)

    # If you need to catch an unknown error use Exception
    try:
        some_other_fn()
    except Exception as e:
        print(f"This unexpected error occurred: {e}")
    """,
        tip="Always catch specific exceptions. At minimum use `except Exception` or re-raise after logging.",
    )
    return


@app.cell
def __(AntiPatternSlide):
    AntiPatternSlide(
        title="type() vs isinstance()",
        description="""Using `type(x) == SomeType` breaks **polymorphism** and ignores subclasses.
    `isinstance()` respects inheritance and is the Pythonic way to check types.""",
        bad_code="""# ❌ Antipattern: using type() for type checking
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if type(dog) == Animal:  # False — misses subclasses!
        print("It's an animal")
    else:
        print("Not recognized as an animal")
    """,
        good_code="""# ✅ Fix: use isinstance() to respect inheritance
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if isinstance(dog, Animal):  # True — correctly identifies subclass
        print("It's an animal ✓")
    """,
        tip="Prefer `isinstance()` for type checks. It works correctly with subclasses and abstract base classes.",
        pattern_id="E721",
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        # Beyond linters
        Linters can greatly help identifying ways to improve our code, they don't magically make you a great developer.

        - Linters fail to capture bad design decisions, e.g. code structure, although you can configure limits on code complexity
        - Linters don't usually detect inappropriate choices for data structures and algorithms
        - Linters don't enforce good development habits (e.g. having a reproducible environment, automating checks and formatting, implementing unit-tests to make your code reliable)
        """
    )
    return


@app.cell
def __(mo):
    mo.hstack(
        [
            mo.md(
                """
        # Data Structures
        - Learning about data structures and their implementation in Python makes you write faster and more efficient code.
        - Each data structure must be picked according to how you need to access and interact with your data.
        - By sticking with built-in algorithms, we avoid straying into anti-pattern territory
        - The `queue` and `collections` standard packages include additional data structures that can be leveraged in our code.


        > Reference: Effective Python by Brett Slatkin - Using Built-in Packages
        """
            ),
            mo.image(
                "https://m.media-amazon.com/images/I/81+g5+5nmWL._SL1500_.jpg",
                width=300,
                rounded=True,
            ),
        ],
        gap=5,
    )
    return


@app.cell
def __(AntiPatternSlide):
    AntiPatternSlide(
        title="Using list as a Stack or Queue",
        description="""`list.pop(0)` (removing from the front) is **O(n)** because every element must be shifted.
    For queue (FIFO) operations, use `collections.deque`, which supports O(1) appends and pops from both ends.""",
        bad_code="""
    queue = []
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    while queue:
        item = queue.pop(0)  # O(n) — shifts all remaining elements!
        print(f"Processing: {item}")
    """,
        good_code="""
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
    """,
    )
    return


@app.cell
def __(mo):
    diagram = mo.mermaid("""
        %%{init: {'theme': 'default', 'flowchart': {'curve': 'basis'}}}%%
        flowchart LR
            START([You have a collection of data])

            START --> Q1{Order matters?}

            Q1 -->|Yes| Q2{Mutable?}
            Q1 -->|No| Q5{Unique values?}

            Q2 -->|No - immutable| QN{Named fields?}
            QN -->|Yes| R_NT([typing.NamedTuple])
            QN -->|No| R_T([tuple])

            Q2 -->|Yes - mutable| Q3{Access pattern?}
            Q3 -->|Index read/write| R_L([list])
            Q3 -->|Insert/remove at both ends| R_D([collections.deque])

            Q5 -->|Yes - unique| Q6{Key → value pairs?}
            Q6 -->|Yes| R_DICT([dict])
            Q6 -->|No| Q9{Mutable?}
            Q9 -->|Yes| R_SET([set])
            Q9 -->|No| R_FS([frozenset])
        """)

    mo.Html(f"""
    <div style="width: 1400px;">
        {diagram.text}
    </div>
    """)

    mo.vstack(
        [
            mo.md("#Picking the right data-structure"),
            mo.Html(f"""
    <div style="width: 1400px;">
        {diagram.text}
    </div>
    """),
        ],
        gap=5,
    )
    return (diagram,)


@app.cell
def __(AntiPatternSlide):
    AntiPatternSlide(
        title="More on built-in packages",
        description="""- Python provides a wide array of tools to make your loops efficient and readable (enumerate, zip, list comprehensions)
        - Linters already notify you about some idiomatic ways to improve your loops
        - As looping conditions become more complex, it might be worthwhile to check whether the itertools standard package has a solution. One of such cases arises when we want to process data in batches""",
        bad_code="""batch_size = 100

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        process(batch)
    """,
        good_code="""from itertools import batched

    batch_size = 100
    for batch in batched(records, batch_size):
        process(batch)
    """,
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Get to know your packages
        - Understanding the inner workings of the packages makes you write more efficient code
        - Be aware of common workflows and patterns used to solve problems
        """
    )
    return


@app.cell
def __():
    # pandas chaining
    return


@app.cell
def __():
    # pandas iterrows
    return


@app.cell
def __():
    # scikit pipeline
    return


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Performance anti-patterns
        - Performance matters, but readability counts
        - Rather than optimizing prematurely, it's always better to profile your code to identify the bottleneck. The standard package **cProfile** can help us with this task.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        # slides

        - ✅ type vs isinstance
        - perflint Inappropriate use of data structures W8301 : Use tuple instead of list for a non-mutated sequence. (use-tuple-over-list)
        - ✅ are there any antipatterns that are not detected by linters?
            - Linters fail to capture bad design decisions, e.g. code structure, although you can configure limits on code complexity
            - ✅ inappropriate choices for data structures and algorithms
        - ✅ slide with types of data structures you should use. If you want to check if an item belongs to a group, use set to check in constant time
        - ✅ queue vs list antipattern - beyond the usual data structures
        - Methodology anti-patterns - these are bad development habits
            - Repetitive manual work that can be automated (unit-tests, formatting, builds)
            - Having a non-reproducible environment
            - Premature optimization
        - Performance anti-patterns
        - Library-specific anti-patterns
            - pandas
            - scikit-learn
        """
    )
    return


@app.cell
def antipattern_topics(mo):
    antipattern_topics = mo.ui.dropdown(
        options=[
            "Using type() instead of isinstance()Not Using Context Managers",
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
def anti_patterns_list():
    antipatterns = {
        "Using type() instead of isinstance()": {
            "emoji": "🔍",
            "description": """

            """,
            "bad_code": """\

    """,
            "good_code": """\

    """,
            "tip": "💡 ",
        },
        "Not Using Context Managers": {
            "emoji": "📂",
            "description": """
    Manually managing resources (files, DB connections, locks) is error-prone.
    If an exception occurs before `.close()`, the resource **leaks**.
    **Context managers** (`with` statements) guarantee cleanup.
            """,
            "bad_code": """\
    # ❌ Antipattern: manual resource management
    f = open("data.txt", "w")
    f.write("hello")
    # If an exception occurs here, f.close() is never called!
    f.close()
    """,
            "good_code": """\
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
    """,
            "tip": "💡 Use `with` statements for files, database connections, locks, and any resource that needs cleanup.",
        },
        "String Concatenation in Loops": {
            "emoji": "🔗",
            "description": """
    Strings in Python are **immutable**. Each `+=` creates a brand-new string object,
    copying all previous content. In a loop, this results in **O(n²)** time complexity.
            """,
            "bad_code": """\
    # ❌ Antipattern: O(n²) string concatenation in a loop
    words = ["Python", "is", "awesome", "and", "fast"]

    result = ""
    for word in words:
        result += word + " "   # Creates a new string every iteration!

    print(result.strip())
    """,
            "good_code": """\
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
    """,
            "tip": "💡 Use `str.join()` to concatenate strings. It is O(n) and far more readable than repeated `+=`.",
        },
        "Checking len() Instead of Truthiness": {
            "emoji": "📏",
            "description": """
    In Python, empty containers (`[]`, `{}`, `""`, `()`) are **falsy** by default.
    Checking `len(x) == 0` is verbose and not Pythonic. Just use the object directly in a boolean context.
            """,
            "bad_code": """\
    # ❌ Antipattern: explicitly checking length
    my_list = []

    if len(my_list) == 0:
        print("List is empty")

    if len(my_list) > 0:
        print("List has items")

    # Also bad: len(x) != 0
    """,
            "good_code": """\
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
    """,
            "tip": "💡 Python containers implement `__bool__` or `__len__`. Trust the truthiness model — it's faster and more readable.",
        },
        "Overusing Global Variables": {
            "emoji": "🌐",
            "description": """
    Global variables create **hidden dependencies** between functions, making code hard to test,
    debug, and reason about. Functions that rely on globals are not self-contained.
            """,
            "bad_code": """\
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
    """,
            "good_code": """\
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
    """,
            "tip": "💡 Pass state explicitly as function arguments. If you need shared state, encapsulate it in a class.",
        },
        "Not Using Enumerate": {
            "emoji": "🔢",
            "description": """
    Manually managing an index variable alongside a loop is verbose and error-prone.
    Python's built-in `enumerate()` gives you both the index and the value cleanly.
            """,
            "bad_code": """\
    # ❌ Antipattern: manual index tracking
    fruits = ["apple", "banana", "cherry"]

    i = 0
    for fruit in fruits:
        print(f"{i}: {fruit}")
        i += 1

    # Also bad: range(len(...))
    for i in range(len(fruits)):
        print(f"{i}: {fruits[i]}")
    """,
            "good_code": """\
    # ✅ Fix: use enumerate()
    fruits = ["apple", "banana", "cherry"]

    for i, fruit in enumerate(fruits):
        print(f"{i}: {fruit}")

    # You can also set the start index
    for i, fruit in enumerate(fruits, start=1):
        print(f"{i}. {fruit}")
    """,
            "tip": "💡 Prefer `enumerate()` over `range(len(...))`. It's more readable and less error-prone.",
        },
        "Returning None Implicitly vs Explicitly": {
            "emoji": "🕳️",
            "description": """
    Functions that sometimes return a value and sometimes return `None` implicitly
    create confusing APIs. Be explicit about what a function returns — always.
            """,
            "bad_code": """\
    # ❌ Antipattern: inconsistent return values
    def find_user(users, name):
        for user in users:
            if user["name"] == name:
                return user
        # Implicitly returns None — caller may not realize this!

    users = [{"name": "Alice"}, {"name": "Bob"}]
    result = find_user(users, "Charlie")
    print(result["name"])  # 💥 TypeError: NoneType has no attribute 'name'
    """,
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
def __():
    return


if __name__ == "__main__":
    app.run()
