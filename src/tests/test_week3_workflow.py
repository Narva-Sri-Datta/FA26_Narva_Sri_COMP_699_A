from database import connect

def login(client,email): return client.post('/login',data={'email':email,'password':'password123'},follow_redirects=True)
def test_user_submit_predict_store_and_match(app,client):
    login(client,'user@example.com')
    response=client.post('/requests/new',data={'description':'The kitchen sink pipe is leaking water','category':'','item_details':'Kitchen sink','service_area':'Test City'},follow_redirects=True)
    assert response.status_code==200
    assert b'Predicted category' in response.data
    with connect(app.config['DATABASE']) as db:
        row=db.execute('SELECT * FROM service_requests').fetchone()
        assert row['predicted_category']=='Plumbing'
        assert row['final_category']=='Plumbing'
        assert row['user_id']==app.config['TEST_IDS']['user']
    assert b'Test Plumbing' in response.data

def test_invalid_short_problem_is_rejected(client):
    login(client,'user@example.com')
    response=client.post('/requests/new',data={'description':'leak'},follow_redirects=True)
    assert response.status_code==400
    assert b'Enter a problem description' in response.data

def test_provider_accept_and_complete_then_user_feedback(app,client):
    login(client,'user@example.com')
    client.post('/requests/new',data={'description':'The sink pipe is leaking badly','service_area':'Test City'},follow_redirects=True)
    with connect(app.config['DATABASE']) as db: rid=db.execute('SELECT id FROM service_requests').fetchone()[0]
    client.post('/logout')
    login(client,'provider@example.com')
    response=client.post(f'/provider/requests/{rid}/decision',data={'action':'accept'},follow_redirects=True)
    assert response.status_code==200
    client.post(f'/provider/requests/{rid}/status',data={'status':'Completed','provider_notes':'Repaired the pipe'},follow_redirects=True)
    client.post('/logout')
    login(client,'user@example.com')
    response=client.post(f'/requests/{rid}/feedback',data={'rating':'5','comment':'Good service'},follow_redirects=True)
    assert response.status_code==200
    with connect(app.config['DATABASE']) as db:
        assert db.execute('SELECT status FROM service_requests WHERE id=?',(rid,)).fetchone()[0]=='Completed'
        assert db.execute('SELECT rating FROM feedback WHERE request_id=?',(rid,)).fetchone()[0]==5

def test_admin_approves_provider(app,client):
    login(client,'admin@example.com')
    response=client.get('/admin')
    assert response.status_code==200
    response=client.post(f"/admin/providers/{app.config['TEST_IDS']['provider']}/approval",data={'approved':'0'},follow_redirects=True)
    assert response.status_code==200
