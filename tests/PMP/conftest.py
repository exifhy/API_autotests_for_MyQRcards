

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/PMP/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.PMP.Api")
