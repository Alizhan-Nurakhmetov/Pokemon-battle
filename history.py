from pathlib import Path
def save(value, result):
    """Append players input and result"""
    path = Path(__file__).with_name("battles.txt")
    with path.open("a", encoding = "utf-8") as file:
        file.write(f"{value} -> {result}\n")

def read_history():
    "Read the saved turns for history"""
    path = Path(__file__).with_name("battles.txt")
    try:
        return path.read_text(encoding = "utf-8")
    except FileNotFoundError :
        return "Play a battle first"
    except OSError:
        return "Could not read the batlle log"

