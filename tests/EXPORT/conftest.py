

def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/EXPORT/" in str(item.fspath).replace("\\", "/"):
            item.add_marker("EXPORT")
