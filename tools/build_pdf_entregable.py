from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "entregables"
OUT.mkdir(exist_ok=True)
PDF = OUT / "TAREA-CONTROL-DE-VERSIONES-contestada.pdf"

BLUE = colors.HexColor("#1A365D")
LIGHT_BLUE = colors.HexColor("#E8EEF5")
LIGHT_GRAY = colors.HexColor("#F2F4F7")
BORDER = colors.HexColor("#DADCE0")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=BLUE,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="SubtitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="H1Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=BLUE,
        spaceBefore=14,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=12.2,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Question",
        parent=styles["BodyCustom"],
        fontName="Helvetica-Bold",
        textColor=BLUE,
        spaceBefore=6,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Cell",
        parent=styles["BodyCustom"],
        fontSize=8.1,
        leading=9.8,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="CellBold",
        parent=styles["Cell"],
        fontName="Helvetica-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="Link",
        parent=styles["BodyCustom"],
        textColor=colors.HexColor("#0563C1"),
    )
)


def p(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def table(headers, rows, widths, header_fill=LIGHT_GRAY):
    data = [[p(h, "CellBold") for h in headers]]
    for row in rows:
        data.append([p(str(v), "Cell") for v in row])
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="CENTER")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_fill),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


story = []
story.append(p("TAREA - CONTROL DE VERSIONES", "TitleCustom"))
story.append(p("Practica guiada: Portafolio Web Express", "SubtitleCustom"))

story.append(
    table(
        ["Dato", "Contenido"],
        [
            ("Estudiante", "EmilianoSP1"),
            ("Asignatura", "Desarrollo Web Integral"),
            ("Repositorio", "https://github.com/EmilianoSP1/portafolio-profesional"),
            ("Fecha", "26 de junio de 2026"),
        ],
        [1.35, 5.15],
        LIGHT_BLUE,
    )
)
story.append(Spacer(1, 10))

story.append(p("1. Evidencia de la practica realizada", "H1Custom"))
story.append(
    p(
        "Se desarrollo un portafolio web basico con HTML y CSS, se inicializo el repositorio local, se conecto con GitHub, "
        "se subieron los cambios a la rama main y se simulo un conflicto real entre un cambio remoto y un cambio local sobre el titulo principal."
    )
)
story.append(
    table(
        ["Commit", "Mensaje", "Evidencia"],
        [
            ("e0fdc8e", "feat: setup inicial del portafolio", "Creacion de index.html y primer hito local."),
            ("bb1e5c3", "style: diseno visual y seccion de contacto", "Vinculo CSS, estilos y seccion de contacto."),
            ("b7a9e1d", "hotfix: actualizacion remota del titulo", "Cambio remoto simulado desde una segunda copia."),
            ("77ba37c", "fix: actualizacion de titulo local", "Cambio local simultaneo sobre la misma linea."),
            ("9c690e0", "merge: resolucion de conflicto en titulo principal", "Conflicto resuelto y fusion confirmado."),
            ("ca55f51", "ci: despliegue automatico en github pages", "Workflow de Pages para despliegue estatico."),
            ("0813a72", "docs: agregar enlaces de entrega", "README con repositorio, commits y sitio Pages."),
        ],
        [0.8, 2.15, 3.55],
        LIGHT_BLUE,
    )
)

story.append(p("2. Enlaces de entrega", "H1Custom"))
for label, url in [
    ("Repositorio en GitHub", "https://github.com/EmilianoSP1/portafolio-profesional"),
    ("Historial de commits", "https://github.com/EmilianoSP1/portafolio-profesional/commits/main"),
    ("Sitio en GitHub Pages", "https://emilianosp1.github.io/portafolio-profesional/"),
]:
    story.append(p(f"<b>{label}:</b> <font color='#0563C1'>{url}</font>"))
story.append(
    p(
        "Nota: se agrego un workflow de GitHub Pages. Si la URL publica aun muestra 404, debe habilitarse Pages en Settings > Pages "
        "y seleccionar GitHub Actions o la rama main como fuente de publicacion."
    )
)

story.append(p("3. Preguntas contestadas", "H1Custom"))
qa = [
    ("Que es el control de versiones?", "Es una practica y conjunto de herramientas que registra cambios de un proyecto a lo largo del tiempo. Permite recuperar versiones anteriores, comparar modificaciones, colaborar sin perder historial y auditar quien hizo cada cambio."),
    ("Cual es la diferencia entre Git y GitHub?", "Git es el sistema de control de versiones que funciona localmente. GitHub es una plataforma en la nube que aloja repositorios Git y facilita colaboracion, pull requests, issues, Actions y GitHub Pages."),
    ("Cuales son los estados principales de un archivo en Git?", "Working Directory: zona donde se editan archivos. Staging Area: zona de preparacion despues de git add. Repositorio local: historial permanente creado con git commit."),
    ("Para que sirve git init?", "Inicializa un repositorio Git en una carpeta y crea la configuracion interna necesaria para comenzar a rastrear archivos."),
    ("Para que sirve git status?", "Muestra el diagnostico del proyecto: rama actual, archivos sin rastrear, archivos modificados, cambios preparados y estado frente al remoto."),
    ("Que hacen git add y git commit?", "git add mueve cambios al Staging Area. git commit guarda una instantanea permanente en el historial local con un mensaje descriptivo."),
    ("Que hacen git remote, git push y git pull?", "git remote vincula el repositorio local con una direccion remota. git push envia commits al remoto. git pull trae cambios remotos y los integra en la rama local."),
    ("Por que se produjo el rechazo del push?", "Porque el repositorio remoto tenia un commit nuevo que el repositorio local todavia no conocia. Git evito sobrescribir ese historial y pidio traer primero los cambios."),
    ("Como se resolvio el conflicto?", "Se ejecuto git pull origin main --no-rebase, Git marco el conflicto en index.html, se eliminaron las marcas de conflicto, se eligio el titulo final, luego se ejecuto git add, git commit y git push."),
    ("Que flujo de trabajo conviene para este proyecto?", "GitHub Flow es el mas conveniente porque el portafolio es un proyecto web pequeno con entregas continuas: rama main estable, cambios pequenos y despliegue frecuente."),
]
for question, answer in qa:
    story.append(p(question, "Question"))
    story.append(p(answer))

story.append(p("4. Flujos de trabajo de versionamiento", "H1Custom"))
story.append(
    table(
        ["Flujo", "Ramas principales", "Ideal para", "Complejidad", "CI/CD"],
        [
            ("Git Flow", "master, develop, feature", "Proyectos grandes con versiones", "Alta", "Media"),
            ("GitHub Flow", "main, feature", "Entregas continuas y proyectos web", "Baja", "Alta"),
            ("GitLab Flow", "main + entornos/versiones", "DevOps y equipos con CI/CD", "Media/Alta", "Muy alta"),
            ("One Flow", "main, feature", "Equipos pequenos o medianos", "Baja", "Alta"),
        ],
        [0.8, 1.25, 2.2, 1.0, 1.25],
        colors.HexColor("#92D050"),
    )
)

story.append(p("5. Plataformas y herramientas", "H1Custom"))
story.append(
    table(
        ["Plataforma", "CI/CD integrado", "Autoalojable", "Integracion empresarial", "Mejor para"],
        [
            ("GitHub", "GitHub Actions", "No", "Media", "Proyectos colaborativos y open source"),
            ("GitLab", "GitLab CI/CD", "Si", "Alta", "DevOps completo e integrado"),
            ("Bitbucket", "Bitbucket Pipelines", "Si", "Alta", "Equipos que usan Atlassian"),
        ],
        [1.0, 1.25, 1.05, 1.45, 1.75],
        colors.HexColor("#4AAED8"),
    )
)

story.append(p("6. Conclusion", "H1Custom"))
story.append(
    p(
        "La practica demuestra el ciclo completo de versionamiento: crear un repositorio local, preparar cambios, confirmar commits, "
        "subir a GitHub, resolver divergencias entre repositorio local y remoto, y dejar el proyecto listo para despliegue en GitHub Pages."
    )
)

doc = SimpleDocTemplate(
    str(PDF),
    pagesize=letter,
    rightMargin=0.75 * inch,
    leftMargin=0.75 * inch,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
)
doc.build(story)
print(PDF)
