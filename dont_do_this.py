import marimo

__generated_with = "0.23.4"
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
    import pandas as pd
    import numpy as np

    import marimo as mo
    from PIL import Image, ImageDraw

    return Image, ImageDraw, math, mo, np, pd, random


@app.cell
def anti_pattern_slide_class(mo):
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
        font-size: 24px
    }}

    pre code {{
        font-family: "JetBrains Mono", monospace !important;
        font-size: 24px !important;
        line-height: 1.5 !important;
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

    return (draw_jagged_grid,)


@app.cell
def save_cover_image(draw_jagged_grid):
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
    return


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
def _():
    return


@app.cell
def about_me(mo):
    mo.vstack([mo.md('# About Me'), mo.hstack(
        [
            mo.image("images/dario.jpg", width=400, style={"border-radius": "100%"}),
            mo.md(
                """
                - Data Scientist & Engineer
                - Currently developing anomaly detection and simulation tools for gas turbines using Python
                - MSc in Engineering and Management at Politecnico di Torino
                - Volunteer of the Python Torino user group
                - Talk to me about guitar, chess, and open-source
                """
            ),
        ],
        gap=10, align='center'
    )], align='center', gap=4, justify='center')
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
    return


@app.cell
def agenda(mo):
    mo.md("""
    # Agenda

    - Introduce design patterns and anti-patterns
    - Explain how to detect anti-patterns with linters
    - Learn about Python and its libraries through some anti-patterns examples
    - Provide some guidance on how to avoid anti-patterns
    """)
    return


@app.cell
def design_patterns_book(mo):
    mo.md("""
    # Design patterns
    > ###Design patterns are typical solutions to recurring problems in software design. Each pattern is a blueprint you can adapt to solve a particular design problem in your code.
    <p align="center">
        <img src="https://m.media-amazon.com/images/I/81IGFC6oFmL._SL1500_.jpg" alt="Design Patterns book cover" width="400"/>
    </p>
    """)
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
                width=400,
                rounded=True,
            ),
        ]
    )
    return


@app.cell
def anti_patterns_examples(mo):
    mo.md(r"""
    # Examples of anti-patterns in software programming
    - **God object**: A single class handles all control in a program rather than control being distributed across multiple classes.
    - **Magic number**: A literal value with an important yet unexplained meaning which could be replaced with a named constant.
    - **Big Ball of Mud**: A software system that lacks a perceivable architecture.
    - **Spaghetti code**: code characterized by an incomprehensible flow
    > [Anti-Pattern - Wikipedia](https://it.wikipedia.org/wiki/Anti-pattern)
    """)
    return


@app.cell
def anti_patterns_in_python_intro(mo):
    mo.md("""
    #Anti-patterns in Python
    - Python is a flexible language that allows us to achieve our programming goals in many different ways
    - This flexibility can be a double-edged sword
    - According to the Zen of Python, there should only be one obvious way to fix a problem
    <br />
    > There should be one - and preferably only one - obvious way to do it.
    > Although that way may not be obvious at first unless you're Dutch.
    > (Tim Peters - The Zen of Python)
    """)
    return


@app.cell
def mutable_default_args(AntiPatternSlide):
    AntiPatternSlide(
        title="Don't use mutable default arguments",
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
    )
    return


@app.cell
def avoiding_antipatterns(mo):
    mo.md("""
    #How do we avoid anti-patterns in Python?
    - Use static code analysis tools (pylint, ruff)
    - Be aware of common mistakes - as a starting point, you can check out the [Little Book of Python Anti-Patterns](https://github.com/quantifiedcode/python-anti-patterns/blob/master/docs/The-Little-Book-Of-Python-Anti-Patterns.pdf)
    - Improve your general programming knowledge (data structures, algorithms, principles, patterns)
    - Learn more about your modules - either built-in or external
    - Ask an expert (or use an LLM) to review your code
    """)
    return


@app.cell
def automatic_code_analysis(mo):
    mo.hstack(
            [
                mo.vstack([mo.md(
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
                )]),
                mo.image(
                    src="http://media.makeameme.org/created/linter-and-formatter.jpg",
                    width=350,
                    height=500
                ),
            ], gap=3, align='center'
        )
    return


@app.cell
def linter_error_animation(mo):
    mo.image("images/linter error.gif")
    return


@app.cell
def linter_setup_1(mo):
    mo.md("""
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
    ##Setting up an automated linter
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
    """)
    return


@app.cell
def linter_config(mo):
    mo.vstack([mo.md('#Configuring your linter'), mo.hstack(
        [
            mo.md(
                r"""
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
        widths="equal"
    )], align='center', gap=5)
    return


@app.cell
def bare_except(AntiPatternSlide):
    AntiPatternSlide(
        title="Don't handle errors with bare except clauses",
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
def type_vs_isinstance(AntiPatternSlide):
    AntiPatternSlide(
        title="type() vs isinstance()",
        description="""Using `type(x) == SomeType` breaks **polymorphism** and ignores subclasses.
    `isinstance()` respects inheritance and is the Pythonic way to check types.""",
        bad_code="""
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if type(dog) == Animal:  # Evaluates to False, since type(dog) returns <class '__main__.Dog'>
        print("What a magnificent beast!")
    """,
        good_code="""
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if isinstance(dog, Animal):  # evaluates to True
        print("What a magnificent beast!")
    """,
        tip="Prefer `isinstance()` for type checks. It works correctly with subclasses and abstract base classes. You can also check if an object belongs to a list of classes, e.g. isinstance(my_animal, [Dog, Cat])",
    )
    return


@app.cell
def beyond_linters(mo):
    mo.md("""
    # Beyond linters
    Linters can greatly help identifying ways to improve our code, they don't magically make you a great developer.

    - Linters fail to capture bad design decisions, e.g. code structure, although you can configure limits on code complexity
    - Linters don't usually detect inappropriate choices for data structures and algorithms
    - Linters don't enforce good development habits (e.g. versioning code, having a reproducible environment, implementing unit-tests to make your code reliable)
    - It's possible to write awful code that passes all linter checks
    """)
    return


@app.cell
def data_structures(mo):
    mo.hstack(
        [
            mo.vstack([mo.md(
                """
        # Data Structures
        - Learning about data structures and their implementation in Python makes you write faster and more efficient code.
        - Each data structure must be picked according to how you need to access and interact with your data.
        - By sticking with idiomatic, built-in algorithms, we avoid straying into anti-pattern territory
        - The `queue` and `collections` standard packages include additional data structures that can be leveraged in our code.


        > Reference: Effective Python by Brett Slatkin - Using Built-in Packages
        """
            )]),
            mo.image(
                "https://m.media-amazon.com/images/I/81+g5+5nmWL._SL1500_.jpg",
                width=400,
                rounded=True,
            ),
        ],
        gap=5,
    )
    return


@app.cell
def lists_as_queue(AntiPatternSlide):
    AntiPatternSlide(
        title="Don't use lists as a Stack or Queue",
        description="""`list.pop(0)` (removing from the front) has **O(n)** complexity because every element must be shifted.
    For FIFO (first in, first out) queue operations, use `collections.deque`, which supports O(1) appends and pops from both ends.""",
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
    """,
        tip="Note that for LIFO (last in first out) queues, a list would actually be fine",
    )
    return


@app.cell
def _():
    return


@app.cell
def data_structure_diagram(mo):
    diagram = mo.mermaid("""
        %%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#EEEDFE', 'primaryBorderColor': '#7F77DD', 'primaryTextColor': '#3C3489', 'secondaryColor': '#E1F5EE', 'tertiaryColor': '#FAEEDA'}, 'flowchart': {'curve': 'basis'}}}%%
    flowchart LR
        START([Start: collection of data])
        START --> Q1{Order matters?}
        Q1 -->|Yes| Q2{Named fields?}
        Q2 -->|Yes| Q2M{Mutable?}
        Q2M -->|No| R_NT([NamedTuple])
        Q2M -->|Yes| R_DC([collections.OrderedDict])
        Q2 -->|No| Q3{Mutable?}
        Q3 -->|No| R_T([tuple])
        Q3 -->|Yes| Q4{Access pattern?}
        Q4 -->|Index / general use| R_L([list])
        Q4 -->|Fast insert & remove\\nat both ends| R_DQ([deque])
        Q1 -->|No| Q5{Require\\nunique values?}
        Q5 -->|Yes| Q6{Key → value pairs?}
        Q6 -->|Yes| R_DICT([dict])
        Q6 -->|No| Q7{Mutable?}
        Q7 -->|Yes| R_SET([set])
        Q7 -->|No| R_FS([frozenset])
        Q5 -->|No| Q8{Mutable?}
        Q8 -->|Yes| R_L2([list])
        Q8 -->|No| R_T2([tuple])
        """)

    mo.vstack([mo.md("## Picking the right data structure"), diagram], gap=5)
    return


@app.cell
def itertools_batched(AntiPatternSlide):
    AntiPatternSlide(
        title="More on built-in packages",
        description="""- Python provides a wide array of tools to make your loops efficient, idiomatic, and readable (enumerate, zip, list comprehensions)
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
        tip="""While it might be debatable whether this is an anti-pattern, using batched is more readable, less error prone, and also applies to generators. The batched iterator allocates tuples rather than lists, which is slightly cheaper. Note that batched is only available on Python >3.12""",
    )
    return


@app.cell
def performance_intro(mo):
    mo.md(r"""
    # Premature optimization — an anti-pattern

    > *"Premature optimization is the root of all evil."* — Donald Knuth

    Rewriting code "to make it faster" before measuring is itself an anti-pattern. It:

    - Wastes effort on code paths that may not even be the bottleneck
    - Makes code harder to read and maintain
    - Bakes in assumptions instead of measurements
    - Can introduce subtle bugs while chasing imaginary gains

    **Before you optimize: profile.** Python's standard library gives you two great tools for free:

    - **`cProfile`** — deterministic CPU profiler. Shows how much time each function call takes.
    - **`tracemalloc`** — memory allocation tracker. Shows current and peak memory used, and where it was allocated.

    Both are built in, both work on any Python program, and both can be wrapped around the suspect code in a handful of lines.
    """)
    return


@app.cell
def profiling_setup(mo):
    # Setup cell — defines the two batching implementations from the itertools
    # slide (each calling a placeholder `process_data`), and the code snippets
    # shown in each tab (which include the cProfile / tracemalloc wrapping so
    # the audience sees a minimal end-to-end example). Produces no visible
    # output: in slide mode, exclude this cell from the layout.
    import textwrap

    def process_data(batch):
        pass

    def process_with_batched(records, batch_size):
        from itertools import batched

        for batch in batched(records, batch_size):
            process_data(batch)

    def process_with_slicing(records, batch_size):
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            process_data(batch)

    batched_cprofile_code = textwrap.dedent("""\
        from itertools import batched
        import cProfile, pstats

        def process_with_batched(records, batch_size):
            for batch in batched(records, batch_size):
                process_data(batch)

        profiler = cProfile.Profile()
        profiler.enable()
        process_with_batched(records, batch_size)
        profiler.disable()

        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats(5)""")

    slicing_cprofile_code = textwrap.dedent("""\
        import cProfile, pstats

        def process_with_slicing(records, batch_size):
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                process_data(batch)

        profiler = cProfile.Profile()
        profiler.enable()
        process_with_slicing(records, batch_size)
        profiler.disable()

        stats = pstats.Stats(profiler).sort_stats("cumulative")
        stats.print_stats(5)""")

    batched_tracemalloc_code = textwrap.dedent("""\
        from itertools import batched
        import tracemalloc

        def process_with_batched(records, batch_size):
            for batch in batched(records, batch_size):
                process_data(batch)

        tracemalloc.start()
        process_with_batched(records, batch_size)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Current memory: {current / 1024:.2f} KB")
        print(f"Peak memory:    {peak / 1024:.2f} KB")""")

    slicing_tracemalloc_code = textwrap.dedent("""\
        import tracemalloc

        def process_with_slicing(records, batch_size):
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                process_data(batch)

        tracemalloc.start()
        process_with_slicing(records, batch_size)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Current memory: {current / 1024:.2f} KB")
        print(f"Peak memory:    {peak / 1024:.2f} KB")""")

    btn_cprofile = mo.ui.run_button(label="▶ Run cProfile", kind="success")
    btn_tracemalloc = mo.ui.run_button(label="▶ Run tracemalloc", kind="success")
    btn_comparison = mo.ui.run_button(label="▶ Run comparison", kind="success")
    return (
        batched_cprofile_code,
        batched_tracemalloc_code,
        btn_comparison,
        btn_cprofile,
        btn_tracemalloc,
        process_with_batched,
        process_with_slicing,
        slicing_cprofile_code,
        slicing_tracemalloc_code,
    )


@app.cell
def performance_comparison(
    batched_cprofile_code,
    batched_tracemalloc_code,
    btn_comparison,
    btn_cprofile,
    btn_tracemalloc,
    mo,
    process_with_batched,
    process_with_slicing,
    slicing_cprofile_code,
    slicing_tracemalloc_code,
):
    import cProfile
    import io
    import pstats
    import time
    import tracemalloc

    _records = list(range(10_000_000))
    _batch_size = 1000

    def _run_cprofile(fn):
        _profiler = cProfile.Profile()
        _profiler.enable()
        fn(_records, _batch_size)
        _profiler.disable()
        _s = io.StringIO()
        # strip_dirs() shortens absolute paths so a single long filename
        # cannot push the column wider than its share of the hstack.
        (
            pstats.Stats(_profiler, stream=_s)
            .strip_dirs()
            .sort_stats("cumulative")
            .print_stats(5)
        )
        return _s.getvalue()

    def _run_tracemalloc(fn):
        tracemalloc.start()
        fn(_records, _batch_size)
        _current, _peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return (
            f"Current memory: {_current / 1024:.2f} KB\n"
            f"Peak memory:    {_peak / 1024:.2f} KB"
        )

    cp_batched_out = ""
    cp_slicing_out = ""
    if btn_cprofile.value:
        cp_batched_out = _run_cprofile(process_with_batched)
        cp_slicing_out = _run_cprofile(process_with_slicing)

    tm_batched_out = ""
    tm_slicing_out = ""
    if btn_tracemalloc.value:
        tm_batched_out = _run_tracemalloc(process_with_batched)
        tm_slicing_out = _run_tracemalloc(process_with_slicing)

    comparison_md = ""
    if btn_comparison.value:
        _t0 = time.perf_counter()
        process_with_batched(_records, _batch_size)
        _t_batched = time.perf_counter() - _t0

        _t0 = time.perf_counter()
        process_with_slicing(_records, _batch_size)
        _t_slicing = time.perf_counter() - _t0

        tracemalloc.start()
        process_with_batched(_records, _batch_size)
        _, _peak_b = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        process_with_slicing(_records, _batch_size)
        _, _peak_s = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        comparison_md = (
            "| Method | Time (s) | Peak Memory (KB) |\n"
            "|---|---|---|\n"
            f"| `itertools.batched` | {_t_batched:.4f} | {_peak_b / 1024:.2f} |\n"
            f"| `range + slicing` | {_t_slicing:.4f} | {_peak_s / 1024:.2f} |\n"
            "\n"
            f"**Setup:** {len(_records):,} integers, batch size = {_batch_size}."
        )

    _code_style = """
    <style>
    pre { background-color: #f3f4f6 !important; border: 1px solid #d1d5db;
      border-radius: 10px; padding: 14px; overflow-x: auto;
      max-width: 100%; }
    pre code { font-family: "JetBrains Mono", monospace !important;
           font-size: 14px !important; line-height: 1.4 !important; }
    </style>
    """

    def code_block(code):
        return mo.md(f"{_code_style}\n```python\n{code}\n```")

    def output_block(output):
        if output:
            return mo.md(f"**Output:**\n\n```\n{output}\n```")
        return mo.Html(
            "<br>"
        )

    def _side_by_side(code_batched, code_slicing, btn, out_batched, out_slicing):
        return mo.vstack(
            [
                mo.hstack(
                    [
                        mo.vstack(
                            [
                                mo.md("### `itertools.batched`"),
                                code_block(code_batched),
                            ]
                        ),
                        mo.vstack(
                            [
                                mo.md("### `range + slicing`"),
                                code_block(code_slicing),
                            ]
                        ),
                    ],
                    gap=2,
                    widths="equal",
                ),
                btn,
                mo.hstack(
                    [output_block(out_batched), output_block(out_slicing)],
                    gap=2,
                    widths="equal",
                ),
            ],
            gap=2,
        )

    cprofile_tab = _side_by_side(
        batched_cprofile_code,
        slicing_cprofile_code,
        btn_cprofile,
        cp_batched_out,
        cp_slicing_out,
    )

    tracemalloc_tab = _side_by_side(
        batched_tracemalloc_code,
        slicing_tracemalloc_code,
        btn_tracemalloc,
        tm_batched_out,
        tm_slicing_out,
    )

    comparison_body = (
        mo.md(comparison_md)
        if comparison_md
        else mo.md('<br>')
    )
    comparison_tab = mo.vstack(
        [
         btn_comparison,
            comparison_body
        ],
        gap=4,
    )

    mo.vstack([
        mo.md("## Profiling demo — cProfile vs tracemalloc <br>"),
        mo.md("""With just a few lines of code we can get in-depth statistics on our code's performance"""
        ),
        mo.ui.tabs({
            "With cProfile": cprofile_tab,
            "With tracemalloc": tracemalloc_tab,
            "Comparison": comparison_tab,
        }),
    ])
    return (io,)


@app.cell
def get_to_know_packages(mo):
    mo.md(r"""
    # Get to know your packages
    - Understanding the inner workings of the packages makes you write more efficient code
    - Be aware of common tools, workflows, and patterns used to solve problems
    """)
    return


@app.cell
def pandas_intro(mo):
    mo.md("""
    # Pandas anti-patterns
    - Pandas is one of the most widely used Python libraries for data analysis
    - Its flexible API makes it easy to write code that is correct but slow or hard to read
    - Several common Pandas anti-patterns have a simple, idiomatic fix that makes code faster and cleaner
    """)
    return


@app.cell
def pandas_chaining(AntiPatternSlide):
    AntiPatternSlide(
        title="Method chaining in Pandas",
        description="""Salvare ogni passo di trasformazione in una nuova variabile (`df1`, `df2`, …) ingombra il namespace e
    rende difficile seguire il flusso dei dati. Pandas è progettato per il **method chaining** — ogni trasformazione
    restituisce un DataFrame, quindi i passi possono essere composti in un'unica espressione leggibile.""",
        bad_code="""def prepare_data(df):
        df['age'] = (pd.Timestamp.today() - df["date_of_birth"]).dt.days // 365
        df1 = df[df['age'] > 18]
        df2 = df1.dropna(subset=['email'])
        df3 = df2.drop(columns=['address'])
        return df3.set_index('user_id')
    """,
        good_code="""def calculate_age(df):
        now = pd.Timestamp.today()
        df['age'] = (now - df['date_of_birth']).dt.days // 365
        return df

    def prepare_data(df):
        return (
        df
            .pipe(calculate_age) 
            .query('age > 18')
            .dropna(subset=['email'])
            .drop(columns=['address'])
            .set_index('user_id')
        )
    """,
        tip="The methods assign, query, pipe can help you rewrite your step-by-step operations in a single chained statement",
    )
    return


@app.cell
def _(mo, np, pd):
    daily_dates = pd.date_range('2025-12-25', '2026-01-10', freq='D')
    values = np.random.randn(len(daily_dates))

    df = pd.DataFrame({
        'date': daily_dates,
        'value': values
    })

    mo.vstack(
        [mo.md('### Suppose you need to aggregate these time series values by month, or by week'), df], align='center'
    )
    return


@app.cell
def pandas_resample(AntiPatternSlide):
    AntiPatternSlide(
        title="Use resample for time-based aggregations",
        description="""- To aggregate time series data by month, a developer might try by extracting year/month columns and using them in a groupby operation. This approach has some drawbacks, and it doesn't work for a weekly aggregation - consider the case in which a week spans two different years.
    - Using the .resample() method allows you to aggregate time series with an arbitrary frequency, provided that the index is of datetime type""",
        bad_code="""\
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    monthly_total = df.groupby(['year', 'month'])['value'].sum()
    """,
        good_code="""\
    df = df.set_index('date')
    monthly_total = df['value'].resample('MS').sum() # MS = Month Start 
    weekly_mean = df['value'].resample('W').mean()
    """,
        tip="resample() accepts any pandas offset alias ('D', 'W', 'ME', 'QE', 'YE', …) and composes naturally with groupby(), agg(), transform(), and method chaining. <br><a href='https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects'>Link to Pandas DateOffset documentation</a>",
    )
    return


@app.cell
def summary(mo):
    mo.md("""
    # Summary and closing remarks
    - Use linters, they are cool
    - Be mindful when approaching a common problem for which an idiomatic, widely-accepted solution might exist.
    - Spending time learning, rather than building stuff, is not a bad idea. You might end up writing beatiful, elegant, and reliable code.
    """)
    return


@app.cell
def qr_code(io, mo):
    import qrcode
    import base64

    url = "https://github.com/DarioRubenScanferlato/Python-Anti-Patterns"

    buf = io.BytesIO()
    qrcode.make(url).save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    mo.vstack([
        mo.md("# Link to the presentation (GitHub)"),
        mo.Html(f'<img src="data:image/png;base64,{b64}" width="600"/>')
    ],
            align='center')
    return


@app.cell
def references(mo):
    mo.md("""
    # References and useful links
    ### Books
    - [Design Patterns: Elements of Reusable Object-Oriented Software (1994)](https://en.wikipedia.org/wiki/Design_Patterns)
    - [AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis (1998)](https://en.wikipedia.org/wiki/AntiPatterns)
    - [Effective Python: 125 Specific Ways to Write Better Python (2022)](https://effectivepython.com/)
    ### Resources
    - [Design Patterns - refactoring.guru](https://refactoring.guru/design-patterns)
    - [The Little Book of Python Anti-Patterns](https://docs.quantifiedcode.com/python-anti-patterns/index.html)
    ### Talks
    - [Write faster Python! Common performance anti patterns - Anthony Shaw - PyCon US 2022](https://www.youtube.com/watch?v=YY7yJHo0M5I)
    - [Don't do that! - Laurenz Albe - Postgres Conference Europe 2025](https://www.youtube.com/watch?v=EKjUd7FUBSc) (not Python-related to, but a great inspiration for this talk)
    """)
    return


if __name__ == "__main__":
    app.run()
