def test_create_db(runner, mocker):
    mock_create_all = mocker.patch('app.cli.db.create_all')
    result = runner.invoke(args=['setup', 'init-db'])
    assert result.exit_code == 0
    assert 'Initialized the database.' in result.output
    mock_create_all.assert_called_once()

def test_drop_db(runner, mocker):
    mock_drop_all = mocker.patch('app.cli.db.drop_all')
    result = runner.invoke(args=['setup', 'drop-db'])
    assert result.exit_code == 0
    assert 'Dropped the database.' in result.output
    mock_drop_all.assert_called_once()
