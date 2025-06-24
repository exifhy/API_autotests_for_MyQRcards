

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/NEWS/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("HubEx.Service.NEWS.Api")
