def test_unauthorised_user_generate_report(client, mocker):
    patch = mocker.patch("background_tasks.app_tasks.create_task_report_for_user.delay")
    res = client.get('/api/v1/reports')
    assert res.status_code == 401
    assert patch.call_count == 0


def test_user_generate_report(authorised_client, mocker):
    patch = mocker.patch("background_tasks.app_tasks.create_task_report_for_user.delay")
    res = authorised_client.get('/api/v1/reports')
    assert res.status_code == 200
    assert res.json() == 'Success'
    assert patch.call_count == 1

