import json
from pathlib import Path


def printTitle(title):
    print("")
    print("=" * len(title))
    print(title)
    print("=" * len(title))


def printInfo(message):
    print(f"[INFO] {message}")


def printWarning(message):
    print(f"[WARN] {message}")


def saveJson(data, outputPath):
    outputPath = Path(outputPath)
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    with outputPath.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)

    printInfo(f"Relatorio salvo em: {outputPath}")
