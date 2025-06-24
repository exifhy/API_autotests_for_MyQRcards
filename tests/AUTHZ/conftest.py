

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/AUTHZ/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.AUTHZ.Api")
