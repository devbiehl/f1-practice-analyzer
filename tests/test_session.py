from event_pipeline.session import Session

def test_session_init():
    s = Session("spielberg", "practice 2", '2025')
    assert s.track_name == "spielberg"
    assert s.session_name == "practice 2"
    assert s.year == '2025'

def test_session_run(mocker):
    # Mock dependecies
    mock_session = mocker.patch('event_pipeline.session.SessionFetcher')
    mock_session_instance = mock_session.return_value
    mock_session_instance.get_session_key.return_value = "valid_session_key"

    mock_dataingestor = mocker.patch('event_pipeline.session.DataIngestor')
    mock_dataingestor_instance = mock_dataingestor.return_value
    mock_dataingestor_instance.load_data.return_value = ({"driver1": "data"}, {"team1": "data"})

    mock_lapanalyzer = mocker.patch('event_pipeline.session.LapAnalyzer')
    mock_lapanalyzer_instance = mock_lapanalyzer.return_value
    mock_lapanalyzer_instance.summary.return_value = None

    mock_dbhandler = mocker.patch('event_pipeline.session.DBHandler')
    mock_dbhandler_instance = mock_dbhandler.return_value
    mock_dbhandler_instance.save_to_db.return_value = None

    mock_logger = mocker.patch('event_pipeline.session.setup_logger')
    mock_logger.return_value = mocker.Mock()

    # create session and run
    s = Session("spielberg", "practice 2", '2025')
    s.run()

    # assert expected calls
    mock_session_instance.get_session_key.assert_called_once()
    mock_dataingestor_instance.load_data.assert_called_once()
    mock_lapanalyzer_instance.summary.assert_called_once()
    mock_dbhandler_instance.save_to_db.assert_called_once()