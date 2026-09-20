import pytest

from pathlib import Path

from sts2.sts_run_parser import StsRunParser

def test_sts_run_parser_init():
    test_path = Path('tests/samples/win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    assert sut
    assert isinstance(sut, StsRunParser)

def test_parse_players_win():
    test_path = Path('tests/samples/win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()

    assert len(sut.dfs) == 8

def test_parse_players_loss():
    test_path = Path('tests/samples/loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()

    assert len(sut.dfs) == 7

def test_parse_players_mp_win():
    test_path = Path('tests/samples/multiplayer_win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()

    assert len(sut.dfs) == 8

def test_parse_players_mp_loss():
    test_path = Path('tests/samples/multiplayer_loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()

    assert len(sut.dfs) == 8

def test_parse_map_point_history_win():
    test_path = Path('tests/samples/win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_map_point_history()

    assert len(sut.dfs) == 14

def test_parse_map_point_history_loss():
    test_path = Path('tests/samples/loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_map_point_history()

    assert len(sut.dfs) == 13

def test_parse_map_point_history_mp_win():
    test_path = Path('tests/samples/multiplayer_win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_map_point_history()

    assert len(sut.dfs) == 15

def test_parse_map_point_history_mp_loss():
    test_path = Path('tests/samples/multiplayer_loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_map_point_history()

    assert len(sut.dfs) == 15

def test_load_to_db_win():
    test_path = Path('tests/samples/win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)
    sut.parse_players()
    sut.parse_map_point_history()

    sut.load_to_db()

def test_load_to_db_loss():
    test_path = Path('tests/samples/loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()
    sut.parse_map_point_history()

    sut.load_to_db()

def test_load_to_db_mp_win():
    test_path = Path('tests/samples/multiplayer_win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()
    sut.parse_map_point_history()

    sut.load_to_db()

def test_load_to_db_mp_loss():
    test_path = Path('tests/samples/multiplayer_loss.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_players()
    sut.parse_map_point_history()

    sut.load_to_db()

def test_parse_run_metadata():
    test_path = Path('tests/samples/win.run')
    db_path = Path('instance/sts2_runs.db')
    sut = StsRunParser(test_path, db_path)

    sut.parse_run_metadata()

    assert 'runs' in sut.dfs
    assert len(sut.dfs['runs'].columns) == 13
    assert 'run_id' in sut.dfs['runs'].columns
    assert sut.dfs['runs'].iloc[0]['start_time'] == 1778022104