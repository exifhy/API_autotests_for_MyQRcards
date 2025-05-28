

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/ADM/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("ADM")
