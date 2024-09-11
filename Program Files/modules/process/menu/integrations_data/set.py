import json

from modules.other.paths import FilePath


def set(integration: str, value: bool) -> None:
    path: str = FilePath.INTEGRATIONS
    with open(path, 'r') as file:
        integrations: dict = json.load(file)
        file.close()

    for key, data in integrations.items():
        if data.get('name', None) == integration:
            integration = key
            break
    
    integrations[integration]['value'] = value

    dependants: list[str]|None = integrations[integration].get('dependants', None)
    if dependants is not None:
        for dependant in dependants:
            integrations[dependant]['value'] = value
            
    dependencies: list[dict]|None = integrations[integration].get('dependencies', None)
    if dependencies is not None:
        for dependency in dependencies:
            item = dependency.get('setting', None)
            value = dependency.get('value', None)
            if item is not None and value is not None:
                integrations[item]['value'] = value

    with open(path, 'w') as file:
        json.dump(integrations, file, indent=4)
        file.close()