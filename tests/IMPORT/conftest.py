

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/IMPORT/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.IMPORT.Api")
