

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/MSG/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.MSG.Api")
