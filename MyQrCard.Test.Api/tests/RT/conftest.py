

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/RT/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.RT.Api")
