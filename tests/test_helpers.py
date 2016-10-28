def test_make_external_id():
    from digital_logic.helpers import make_external_id

    worker_id = 'debug7SDIPD'
    assignment_id = 'debugSSDIP8'
    hit_id = 'debug7SDPIS'

    external_id = make_external_id(worker_id, assignment_id, hit_id)

    assert external_id == '97cdf37dfa7e75280ecf22ef98867dfe'
