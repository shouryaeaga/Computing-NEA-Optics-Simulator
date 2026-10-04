import re
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
UML_DIR = PROJECT_ROOT / "uml"

UML_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# 1. Run Pyreverse
# ---------------------------------------------------------

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
# 2. Find the generated PlantUML file
# ---------------------------------------------------------

uml_file = UML_DIR / "classes_Optics.plantuml"

if not uml_file.exists():
    raise FileNotFoundError(f"Could not find generated UML file: {uml_file}")


# ---------------------------------------------------------
# 3. Convert Python naming conventions to UML visibility
#    __foo -> -foo (private), _foo -> #foo (protected),
#    foo -> +foo (public), __init__ -> +__init__ (public)
# ---------------------------------------------------------

lines = uml_file.read_text(encoding="utf-8").splitlines()

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
        member = stripped
        member = re.sub(r"\[.*?\]", "", member)

        if not member.startswith(("+", "-", "#", "~")):
            name = member.split("(", 1)[0].split(" ", 1)[0]

            if re.match(r"^__.*__$", name):
                member = "+" + member
            elif member.startswith("__"):
                member = "-" + member[2:]
            elif member.startswith("_"):
                member = "#" + member[1:]
            else:
                member = "+" + member

        line = indentation + member

    output.append(line)


# ---------------------------------------------------------
# 4. Write the modified UML
# ---------------------------------------------------------

extra_lines = """
' Light sources own their Rays
src.objects.light_sources.Base.LightSource "1" *-- "0..*" src.core.ray.Ray

' Renderer owns the Scene
src.GUI.renderer.Renderer *--> src.GUI.scene.Scene

' Scene is directed-associated with the light sources
src.GUI.scene.Scene "0..*" --> src.objects.light_sources.Base.LightSource
""".strip().splitlines()

end = max(i for i, l in enumerate(output) if l.strip().startswith("@enduml"))
output[end:end] = extra_lines

uml_file.write_text("\n".join(output) + "\n", encoding="utf-8")

print(f"UML generated successfully: {uml_file}")