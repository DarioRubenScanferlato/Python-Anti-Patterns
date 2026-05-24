import marimo

__generated_with = "0.8.22"
app = marimo.App(
    width="medium",
    app_title="Non farlo",
    layout_file="layouts/non_farlo.slides.json",
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
def definizione_slide(mo):
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
def generazione_cover(draw_jagged_grid):
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
            #**Non farlo!**
            ###Evitare gli Anti-Pattern in Python
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
def chi_sono(mo):
    mo.hstack(
        [
            mo.image("images/dario.jpg", width=400, style={"border-radius": "100%"}),
            mo.md(
                """# Chi sono
                - Data Scientist & Engineer
                - Sviluppo algoritmi in Python per rilevare anomalie e simulare il funzionamento di turbine a gas
                - MSc in Ingegneria e Management al Politecnico di Torino
                - Volontario del gruppo utenti Python Torino
                - Potete parlarmi di chitarra, scacchi e open-source :)
                """
            ),
        ],
        gap=10,
    )
    return


@app.cell
def agenda(mo):
    mo.md(
        """
        # Agenda

        - Introduzione ai concetti di design pattern e anti-pattern
        - Come usare i linter per migliorare la qualità del nostro codice
        - Spiegazione di alcuni esempi di anti-pattern in Python 
        - Consigli pratici su come evitare gli anti-pattern
        """
    )
    return


@app.cell
def design_patterns_book(mo):
    mo.md(
        """
        # Design pattern
        > ###I design pattern sono soluzioni tipiche a problemi ricorrenti nella progettazione del software. Ogni pattern è un modello che puoi adattare per risolvere un particolare problema di design nel tuo codice.
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
            mo.md("#Design pattern"),
            mo.hstack(
                [
                    mo.image(
                        src="images/anti patterns catalog.png", width=1200, rounded=True
                    )
                ],
                justify="center",
            ),
            mo.md(
                "[Fonte: refactoring.guru](https://refactoring.guru/design-patterns/catalog)"
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
    # Anti-pattern
    Un *anti-pattern* è una soluzione a una classe di problemi che può essere comunemente utilizzata, ma che risulta essere inefficace o controproducente.
    ### Gli anti-pattern portano a:
    * Prestazioni sub-ottimali
    * Codice poco leggibile
    * Inaffidabilità / comportamenti inaspettati
    * Processo di sviluppo più lento
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
        # Esempi di anti-pattern nella programmazione software
        - **God object**: implementare una grossa funzionalità in un unico oggetto che esegue tutte le operazioni, invece che in più oggetti che si dividono il compito.
        - **Magic number**: inserire costanti negli algoritmi senza documentarne il significato o lo scopo
        - **Big Ball of Mud**: Un sistema software privo di un'architettura percepibile.
        - **Spaghetti code**: codice con un flusso incomprensibile 
        > Fonte: [Anti-Pattern - Wikipedia](https://it.wikipedia.org/wiki/Anti-pattern)
        """
    )
    return


@app.cell
def anti_patterns_in_python_intro(mo):
    mo.md(
        """
        # Anti-pattern in Python
        - Python è un linguaggio flessibile che ci permette di raggiungere i nostri obiettivi in molti modi diversi
        - Questa flessibilità può essere un'arma a doppio taglio
        - Secondo lo Zen di Python, dovrebbe esserci un solo modo ovvio per risolvere un problema

        <br />
        > There should be one - and preferably only one - obvious way to do it.
        > Although that way may not be obvious at first unless you're Dutch.
        > (Tim Peters - The Zen of Python)
        """
    )
    return


@app.cell
def mutable_defaults(AntiPatternSlide):
    AntiPatternSlide(
        title="Non usare argomenti di default mutabili",
        description="""
    Gli **argomenti di default mutabili** (e.g. liste o dizionari) vengono creati **una sola volta** quando la funzione viene definita,
    non ad ogni chiamata. Questo porta a uno stato condiviso tra le chiamate.
            """,
        bad_code="""
    def append_to(element, target=[]):
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [1, 2]  <--  Sebbene la 
    print(append_to(3))   # [1, 2, 3] <-- La lista continua a crescere
    """,
        good_code="""
    def append_to(element, target=None):
        if target is None:
            target = []
        target.append(element)
        return target

    print(append_to(1))   # [1]
    print(append_to(2))   # [2]  ✓
    print(append_to(3))   # [3]  ✓
    """,
        tip="""Non usare strutture dati mutabili come valore default di un argomento. Queste strutture vengono inizializzate al momento della definizione della funzione. Tutte le chiamate riutilizzano questa singola istanza, persistendo le modifiche tra di esse.""",
    )
    return


@app.cell
def evitare_antipatterns(mo):
    mo.md(
        """
        # Come evitare gli anti-pattern in Python?
        - Usa strumenti di analisi statica del codice (pylint, ruff)
        - Impara a riconoscere errori comuni — come punto di partenza, consulta il [Little Book of Python Anti-Patterns](https://github.com/quantifiedcode/python-anti-patterns/blob/master/docs/The-Little-Book-Of-Python-Anti-Patterns.pdf)
        - Migliora la tua conoscenza generale della programmazione (strutture dati, algoritmi, principi, pattern)
        - Impara di più sui moduli standard di Python e quelli che utilizzi frequentemente
        - Chiedi a un esperto (o usa un LLM) di revisionare il tuo codice
        """
    )
    return


@app.cell
def analisi_automatica(mo):
    mo.hstack(
        [
            mo.md(
                """# Strumenti di analisi automatica del codice
    - Un linter analizza il tuo codice in un AST (Abstract Syntax Tree) e poi percorre quell'albero cercando nodi che corrispondono a un anti-pattern noto. Quando ne trova uno, emette una errore con il codice della regola, il numero di riga e un messaggio.
    - I linter possono essere configurati abilitando vari set di regole per rilevare tipi specifici di errori
    - Gli anti-pattern rilevati dai linter sono identificati con un codice composto da una o più lettere che indicano la categoria dell'errore e un numero che lo differenzia. Ad esempio, pylint usa:
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
def errore_linter(mo):
    mo.image("images/linter error.gif")
    return


@app.cell
def configurare_linter(mo):
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
        # Come automatizzare i controlli con un linter
        Configurare un linter è piuttosto semplice. Consiglio [**ruff**](https://docs.astral.sh/ruff/) perché è molto veloce e ha capacità di auto-correzione. Possiamo abilitarlo per eseguirlo ad ogni commit usando pre-commit.

        Passo 1: Installa pre-commit e ruff
        ```bash
        pip install pre-commit ruff
        ```
        Passo 2: Crea .pre-commit-config.yaml
        ```yaml
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.5.0
            hooks:
              - id: ruff
              - id: ruff-format # Not related to linting, but useful nonetheless
        ```
        Passo 3: Abilita pre-commit
        ```bash
        pre-commit install
        ```
        """
    )
    return


@app.cell
def configurare_regole(mo):
    mo.hstack(
        [
            mo.md(
                r"""# Configurare le regole di linting
        - È possibile configurare il tuo linter per applicare solo set specifici di regole. Questo approccio è consigliato soprattutto quando si analizza un progetto grande per la prima volta
        - La configurazione si può modificare facilmente aggiornando il file ```pyproject.toml``` del progetto
        - Attenzione: i codici delle regole possono variare tra diversi linter

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
def bare_except(AntiPatternSlide):
    AntiPatternSlide(
        title="Non gestire gli errori con un *bare except*",
        description="""
    - Gestire gli errori con la sola clausula `except:` (senza specificare il tipo di eccezione) è pericoloso: questa sintassi cattura tutte le eccezioni, incluse `SystemExit` e `KeyboardInterrupt`, rendendo difficile interrompere il programma e mascherando altri problemi.
    - Sia pylint ([W0702](https://pylint.readthedocs.io/en/v3.3.9/user_guide/messages/warning/bare-except.html)) che ruff ([E722](https://docs.astral.sh/ruff/rules/bare-except/)) rilevano questo tipo di anti-pattern.
    - Questo anti-pattern è così noto che è stata proposta una PEP per vietarlo in Python ([PEP760](https://peps.python.org/pep-0760/))
            """,
        bad_code="""try:
        raise KeyboardInterrupt("Questa eccezione simula un utente che prova a interrompere il programma con ctrl+C")
    except:
        print("Hai provato a interrompere il codice, ma siccome hai usato un bare `except` io vado avanti")
    """,
        good_code="""try:
        do_something_that_might_break()
    except MoreSpecificException as e:
        handle_error(e)

    # Se devi catturare un errore sconosciuto, usa Exception
    try:
        some_other_fn()
    except Exception as e:
        print(f"Si è verificato questo errore inatteso: {e}")
    """,
        tip="Cattura sempre eccezioni specifiche. Come minimo usa `except Exception` oppure rilanciare l'eccezione dopo aver loggato l'errore.",
    )
    return


@app.cell
def type_vs_isinstance(AntiPatternSlide):
    AntiPatternSlide(
        title="type() vs isinstance()",
        description="""Usare `type(x) == SomeType` è rischioso perché non considera le sottoclassi.
    `isinstance()` rispetta l'ereditarietà ed è il modo Pythonico di verificare i tipi.""",
        bad_code="""
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if type(dog) == Animal:  # False: type(dog) restituisce <class '__main__.Dog'>
        print("Che magnifica bestia!")
    """,
        good_code="""
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    if isinstance(dog, Animal):  # True ✓
        print("Che magnifica bestia!")
    """,
        tip="Preferisci `isinstance()` per i controlli di tipo. Funziona correttamente con le sottoclassi e le classi base astratte. Puoi anche verificare se un oggetto appartiene a una lista di classi, es. isinstance(my_animal, [Dog, Cat])",
    )
    return


@app.cell
def oltre_i_linter(mo):
    mo.md(
        """
        # Oltre i linter
        - I linter aiutano a identificare miglioramenti nel codice, ma non ci rendono magicamente dei grandi sviluppatori.
        - I linter non riescono a identificare decisioni sbagliate di design (e.g. struttura del codice), anche se puoi configurare limiti sulla complessità
        - Spesso non rilevano scelte inappropriate per strutture dati e algoritmi
        - Non possono sostituire buone abitudini di sviluppo (es. versionare il codice, avere un ambiente riproducibile, scrivere unit-test)
        - È possibile scrivere codice pessimo che supera tutti i controlli di un linter
        """
    )
    return


@app.cell
def strutture_dati(mo):
    mo.hstack(
        [
            mo.md(
                """
        # Strutture Dati
        - Imparare le strutture dati e la loro implementazione in Python ti fa scrivere codice più veloce ed efficiente.
        - Ogni struttura dati va scelta in base a come devi accedere e interagire con i tuoi dati.
        - Usando algoritmi idiomatici e built-in, evitiamo di cadere in territori di anti-pattern.
        - I package standard `queue` e `collections` includono strutture dati aggiuntive che possiamo sfruttare nel nostro codice.

        > Prossimo esempio tratto da Effective Python di Brett Slatkin - Using Built-in Packages
        """
            ),
            mo.image(
                "https://m.media-amazon.com/images/I/81+g5+5nmWL._SL1500_.jpg",
                width=400,
                rounded=True,
            ),
        ],
        gap=5,
        align='center'
    )
    return


@app.cell
def queues(AntiPatternSlide):
    AntiPatternSlide(
        title="Non usare liste come Stack o Queue",
        description="""`list.pop(0)` (rimuovere dall'inizio) ha complessità **O(n)** perché ogni elemento deve essere spostato.
    Per operazioni di queue FIFO (first in, first out), usa `collections.deque`, che supporta append e pop con complessità costante da entrambe le estremità.""",
        bad_code="""
    queue = []
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    while queue:
        item = queue.pop(0)  # O(n) — sposta tutti gli elementi rimanenti!
        print(f"Elaborazione: {item}")
    """,
        good_code="""
    from collections import deque

    queue = deque()
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    while queue:
        item = queue.popleft()  # O(1) ✓
        print(f"Elaborazione: {item}")
    """,
        tip="Per le queue LIFO (last in first out), una lista va benissimo.",
    )
    return


@app.cell
def diagramma_mermaid(mo):
    diagram = mo.mermaid("""
        %%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#EEEDFE', 'primaryBorderColor': '#7F77DD', 'primaryTextColor': '#3C3489', 'secondaryColor': '#E1F5EE', 'tertiaryColor': '#FAEEDA'}, 'flowchart': {'curve': 'basis'}}}%%
    flowchart LR
        START([Inizio: collezione di dati])
        START --> Q1{L'ordine e' importante?}
        Q1 -->|Si| Q2{Campi nominati?}
        Q2 -->|Si| Q2M{Mutabile?}
        Q2M -->|No| R_NT([NamedTuple])
        Q2M -->|Si| R_DC([dataclass])
        Q2 -->|No| Q3{Mutabile?}
        Q3 -->|No| R_T([tuple])
        Q3 -->|Si| Q4{Pattern di accesso?}
        Q4 -->|Indice / uso generale| R_L([list])
        Q4 -->|Inserimento e rimozione\\nrapida da entrambi i lati| R_DQ([deque])
        Q1 -->|No| Q5{Valori\\nunici richiesti?}
        Q5 -->|Si| Q6{Coppie chiave → valore?}
        Q6 -->|Si| R_DICT([dict])
        Q6 -->|No| Q7{Mutabile?}
        Q7 -->|Si| R_SET([set])
        Q7 -->|No| R_FS([frozenset])
        Q5 -->|No| Q8{Mutabile?}
        Q8 -->|Si| R_L2([list])
        Q8 -->|No| R_T2([tuple])
        """)

    mo.vstack(
        [
            mo.md("# Come scegliere la struttura dati più adatta"),
            diagram,
        ],
    ).style({
        "width": "1400px",
        "max-width": "none"
    })
    return (diagram,)


@app.cell
def builtin_packages(AntiPatternSlide):
    AntiPatternSlide(
        title="Sfruttare le librerie standard di Python: itertools",
        description="""- Python offre molti strumenti per rendere i loop efficienti, idiomatici e leggibili (enumerate, zip, list comprehension)
            - I linter già ti avvisano di alcuni modi idiomatici per migliorare i tuoi loop
            - Quando le condizioni di iterazione diventano più complesse, vale la pena controllare se il package standard itertools ha già una soluzione. Un caso tipico è l'elaborazione dei dati in batch.""",
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
        tip="""Anche se si potrebbe discutere se questo sia un anti-pattern, usare batched è più leggibile, meno soggetto a errori e funziona anche con i generatori. L'iteratore batched alloca tuple invece di liste, il che è leggermente più efficiente. Nota: batched è disponibile solo su Python >= 3.12.""",
    )
    return


@app.cell
def librerie(mo):
    mo.md(
        r"""
        # Utilizza le librerie efficacemente
        - Capire il funzionamento interno dei package ti fa scrivere codice più efficiente
        - Sii consapevole degli strumenti, dei flussi di lavoro e dei pattern comuni usati per risolvere i problemi
        """
    )
    return


@app.cell
def method_chaining(AntiPatternSlide):
    AntiPatternSlide(
        title="Method chaining in Pandas",
        description="""Salvare ogni passo di trasformazione in una nuova variabile (`df1`, `df2`, …) ingombra il namespace e
    rende difficile seguire il flusso dei dati. Pandas è progettato per il **method chaining** — ogni trasformazione
    restituisce un DataFrame, quindi i passi possono essere composti in un'unica espressione leggibile.""",
        bad_code="""def prepare_data(df):
        df['age'] = (pd.Timestamp.today() - df["date_of_birth"]).dt.days // 365
        df1 = df[df['age'] > 18]
        df2 = df1.dropna(subset=['email'])
        df3 = df2.rename(columns={'name': 'full_name'})
        return df3.reset_index(drop=True)
    """,
        good_code="""def calculate_age(df):
        now = pd.Timestamp.today()
        df['age'] = (now - df['date_of_birth']).dt.days // 365
        # You can also use the assign method to add columns within a chain!
        # df = df.assign(age=lambda d: (now - d["date_of_birth"]).dt.days // 365)
        return df

    def prepare_data(df):
        return (
        df
            .pipe(calculate_age)
            .query('age > 18')
            .dropna(subset=['email'])
            .rename(columns={'name': 'full_name'})
            .reset_index(drop=True)
        )
    """,
        tip="The methods assign, query, pipe can help you rewrite your step-by-step operations in a single chained statement",
    )
    return


@app.cell
def __(mo, np, pd):
    dates = pd.date_range('2025-12-25', '2026-01-10', freq='D')
    values = np.random.randn(len(dates))

    df = pd.DataFrame({
        'date': dates,
        'value': values
    })

    mo.vstack(
        [mo.md('### Supponiamo di dover aggregare per mese o per settimana i seguenti valori'), df], align='center'
    )
    return dates, df, values


@app.cell
def resample(AntiPatternSlide):
    AntiPatternSlide(
        title="Usa resample per le aggregazioni temporali",
        description="""- Per operazioni su dataframe contenenti dati di serie storiche, conviene lavorare con un indice di tipo DateTimeIndex, soprattutto se il nostro obiettivo consiste nell'aggregare i dati in base a una determinata frequenza.
    - Quando il tuo index è un `DatetimeIndex`, `resample()` gestisce tutta la logica di aggregazione, senza che sia necessario creare colonne aggiuntive.""",
        bad_code="""\
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    monthly_total = df.groupby(['year', 'month'])['value'].sum()
    # Using this approach, calculating the weekly total becomes tricky
    # weeks that are in-between two years will be aggregated as two different records
    """,
        good_code="""\
    df = df.set_index('date')
    monthly_total = df['value'].resample('ME').sum()
    weekly_mean = df['value'].resample('W').mean()
    """,
        tip="resample() accetta qualsiasi alias di offset pandas ('D', 'W', 'ME', 'QE', 'YE', …) e si compone naturalmente con groupby(), agg(), transform() e il method chaining."
    )
    return


@app.cell
def conclusioni(mo):
    mo.md(
        """
        # Conclusioni
        - Usa un linter se non lo stai già facendo
        - Fai attenzione quando affronti un problema comune: potrebbe esistere una soluzione idiomatica e ampiamente accettata.
        - Sebbene lavorare su progetti sia un ottimo metodo per migliorare le nostre abilità come developer, dedicare tempo all'apprendimento di tecniche di programmazione, Python e delle librerie con cui si lavora è uno step fondamentale.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Fonti e altre cose interessanti
        ### Libri
        - [Design Patterns: Elements of Reusable Object-Oriented Software (1994)](https://en.wikipedia.org/wiki/Design_Patterns)
        - [AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis (1998)](https://en.wikipedia.org/wiki/AntiPatterns)
        - [Effective Python: 125 Specific Ways to Write Better Python (2022)](https://effectivepython.com/)
        ### Risorse
        - [Design Patterns - refactoring.guru](https://refactoring.guru/design-patterns)
        - [The Little Book of Python Anti-Patterns](https://docs.quantifiedcode.com/python-anti-patterns/index.html)
        ### Video
        - [Write faster Python! Common performance anti patterns - Anthony Shaw - PyCon US 2022](https://www.youtube.com/watch?v=YY7yJHo0M5I)
        - [Don't do that! - Laurenz Albe - Postgres Conference Europe 2025](https://www.youtube.com/watch?v=EKjUd7FUBSc) (non c'entra una fava con Python ma ha ispirato questo talk)
        """
    )
    return


if __name__ == "__main__":
    app.run()
