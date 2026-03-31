def test_worker_transports_and_updates_state(runtime_model):
    runtime_model.run()
    assert runtime_model.worker_01.task_count > 0
    states = [s for _, s in runtime_model.worker_01.state_history]
    assert "PICKING" in states
    assert "WALKING" in states
    assert "DROPPING" in states


def test_worker_move_time(runtime_model):
    t = runtime_model.worker_01.move_time(3.0)
    assert t == 3.0 / runtime_model.worker_01.speed_mps
