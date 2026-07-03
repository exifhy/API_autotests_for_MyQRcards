

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/PROXY/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.PROXY.Api")
