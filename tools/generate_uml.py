import re
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
UML_DIR = PROJECT_ROOT / "uml"

MODIFIER_RE = re.compile(r"^(\{(?:abstract|static)\})\s*")
GENERIC_RE = re.compile(r"\[[^\[\]]*\]")  # innermost [...] only

# Extra relationships that pyreverse can't infer on its own.
# Delete lines from here once pyreverse starts drawing them itself
# (e.g. after adding type annotations), otherwise you get duplicate arrows.
EXTRA_LINES = """
' Light sources own their Rays
src.objects.light_sources.Base.LightSource "1" *-- "0..*" src.core.ray.Ray

' Renderer owns its collaborators
src.GUI.renderer.Renderer *--> src.GUI.scene.Scene
src.GUI.renderer.Renderer *--> src.GUI.input_handler.InputHandler
src.GUI.renderer.Renderer *--> src.GUI.glass_shape_renderer.GlassShapeRenderer
src.GUI.renderer.Renderer *--> src.GUI.light_source_renderer.LightSourceRenderer

' Scene associations
src.GUI.scene.Scene --> "0..*" src.objects.light_sources.Base.LightSource
src.GUI.scene.Scene --> "0..*" src.objects.glass_shapes.Polygon.Polygon
src.GUI.scene.Scene --> "0..*" src.core.ray.Ray : refracted rays
src.GUI.input_handler.InputHandler --> src.GUI.scene.Scene

' Renderers depend on what they draw
src.GUI.glass_shape_renderer.GlassShapeRenderer ..> src.objects.glass_shapes.Polygon.Polygon
src.GUI.light_source_renderer.LightSourceRenderer ..> src.objects.light_sources.Base.LightSource
src.GUI.light_source_renderer.LightSourceRenderer ..> src.core.ray.Ray

' Only uncomment if Rectangle is declared as class Rectangle(Polygon)
' and pyreverse has not drawn the arrow itself:
' src.objects.glass_shapes.Rectangle.Rectangle --|> src.objects.glass_shapes.Polygon.Polygon
""".strip().splitlines()


# ---------------------------------------------------------
# 1. Run Pyreverse
# ---------------------------------------------------------

def run_pyreverse() -> None:
    subprocess.run(
        [
            "pyreverse",
            "-o", "plantuml",
            "-p", "Optics",
            "-d", str(UML_DIR),
            "-f", "ALL",
            str(SRC_DIR),
        ],
        check=True,
    )


# ---------------------------------------------------------
# 2. Convert Python naming conventions to UML visibility
#    __foo -> -foo (private), _foo -> #foo (protected),
#    foo -> +foo (public), __init__ -> +__init__ (public)
#    {abstract}/{static} modifiers are kept and placed after
#    the visibility symbol: +{abstract} foo()
# ---------------------------------------------------------

def add_visibility(member: str) -> str:
    if member.startswith(("+", "-", "#", "~")):
        return member

    modifier = ""
    match = MODIFIER_RE.match(member)
    if match:
        modifier = match.group(1) + " "
        member = member[match.end():]

    name = member.split("(", 1)[0].split(" ", 1)[0]

    if re.match(r"^__.*__$", name):  # dunder methods are public
        prefix = "+"
    elif member.startswith("__"):  # private
        prefix, member = "-", member[2:]
    elif member.startswith("_"):  # protected
        prefix, member = "#", member[1:]
    else:
        prefix = "+"

    return prefix + modifier + member


def strip_generics(member: str) -> str:
    """Remove [...] type parameters, innermost first, so nested ones
    like list[list[tuple]] are removed completely."""
    while True:
        new = GENERIC_RE.sub("", member)
        if new == member:
            return member
        member = new


def process_lines(lines: list[str]) -> list[str]:
    inside_class = False
    output = []

    for line in lines:
        stripped = line.strip()

        # Turn off PlantUML's coloured visibility icons so the
        # +, -, # characters are shown as text instead
        if stripped.startswith("@startuml"):
            output.append(line)
            output.append("skinparam classAttributeIconSize 0")
            continue

        if stripped.startswith("class ") and stripped.endswith("{"):
            inside_class = True
            output.append(line)
            continue

        if inside_class and stripped == "}":
            inside_class = False
            output.append(line)
            continue

        if inside_class and stripped:
            indentation = line[: len(line) - len(line.lstrip())]
            member = strip_generics(stripped)
            line = indentation + add_visibility(member)

        output.append(line)

    # Insert extra relationships just before @enduml
    end = max(i for i, l in enumerate(output) if l.strip().startswith("@enduml"))
    output[end:end] = EXTRA_LINES

    return output


def main() -> None:
    UML_DIR.mkdir(exist_ok=True)
    run_pyreverse()

    uml_file = UML_DIR / "classes_Optics.plantuml"
    if not uml_file.exists():
        raise FileNotFoundError(f"Could not find generated UML file: {uml_file}")

    lines = uml_file.read_text(encoding="utf-8").splitlines()
    output = process_lines(lines)
    uml_file.write_text("\n".join(output) + "\n", encoding="utf-8")

    print(f"UML generated successfully: {uml_file}")


if __name__ == "__main__":
    main()