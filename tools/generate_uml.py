import re
import subprocess
import sys
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
    raise FileNotFoundError(
        f"Could not find generated UML file: {uml_file}"
    )


# ---------------------------------------------------------
# 3. Convert Python naming conventions to UML visibility
#
#    __foo       -> -foo   private
#    _foo        -> #foo   protected
#    foo         -> +foo   public
#
#    __init__    -> +__init__()  public constructor
# ---------------------------------------------------------

lines = uml_file.read_text(encoding="utf-8").splitlines()

inside_class = False
output = []


for line in lines:

    stripped = line.strip()

    # Detect beginning/end of a class
    if stripped.startswith("class ") and stripped.endswith("{"):
        inside_class = True
        output.append(line)
        continue

    if inside_class and stripped == "}":
        inside_class = False
        output.append(line)
        continue

    # Only modify members inside classes
    if inside_class and stripped:

        indentation = line[:len(line) - len(line.lstrip())]
        member = stripped

        # Don't touch relationships or other PlantUML commands
        if not member.startswith(("+", "-", "#", "~")):

            # Python magic methods such as __init__
            if re.match(r"^__.*__$", member.split("(", 1)[0]):
                member = "+" + member

            # Private: __name
            elif member.startswith("__"):
                member = "-" + member[2:]

            # Protected: _name
            elif member.startswith("_"):
                member = "#" + member[1:]

            # Public
            else:
                member = "+" + member

            line = indentation + member

    output.append(line)


# ---------------------------------------------------------
# 4. Write the modified UML
# ---------------------------------------------------------

uml_file.write_text(
    "\n".join(output) + "\n",
    encoding="utf-8",
)

print(f"UML generated successfully: {uml_file}")