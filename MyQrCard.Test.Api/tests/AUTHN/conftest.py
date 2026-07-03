

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/AUTHN/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.AUTHN.Api")
