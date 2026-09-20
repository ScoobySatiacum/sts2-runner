def test_core_package_imports():
    from sts2.parse.loader import RunFileLoader
    from sts2.storage.sqlite_repository import SqliteRunRepository
    from sts2.queries.run_queries import RunQueries

    assert RunFileLoader is not None
    assert SqliteRunRepository is not None
    assert RunQueries is not None


def test_cli_and_gui_are_separate_layers():
    import sts2.cli as cli
    import sts2.gui as gui

    assert hasattr(cli, "ingest")
    assert hasattr(gui, "app")