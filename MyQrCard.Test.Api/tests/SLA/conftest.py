

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/SLA/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.SLA.Api")
