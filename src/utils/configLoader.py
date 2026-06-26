from copy import deepcopy
from pathlib import Path


def loadConfig(configPath):
    yaml = _loadYaml()
    configPath = Path(configPath)

    if not configPath.exists():
        raise FileNotFoundError(f"Arquivo de config nao encontrado: {configPath}")

    with configPath.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    basePath = config.pop("baseConfig", None)
    if not basePath:
        return config

    basePath = Path(basePath)
    if not basePath.is_absolute():
        basePath = configPath.parent / basePath

    baseConfig = loadConfig(basePath)
    return mergeConfig(baseConfig, config)


def saveConfig(config, outputPath):
    yaml = _loadYaml()
    outputPath = Path(outputPath)
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    with outputPath.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config, file, sort_keys=False, allow_unicode=False)


def mergeConfig(baseConfig, overrideConfig):
    result = deepcopy(baseConfig) if baseConfig else {}

    for key, value in (overrideConfig or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = mergeConfig(result[key], value)
        else:
            result[key] = deepcopy(value)

    return result


def getValue(config, keyPath, default=None):
    current = config

    for key in keyPath.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current


def setValue(config, keyPath, value):
    keys = keyPath.split(".")
    current = config

    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return config


def applyOverrides(config, overrides):
    result = deepcopy(config)

    for keyPath, value in overrides.items():
        if value is not None:
            setValue(result, keyPath, value)

    return result


def _loadYaml():
    try:
        import yaml
    except ImportError as error:
        raise ImportError(
            "PyYAML nao esta instalado. Instale com: pip install pyyaml"
        ) from error

    return yaml
