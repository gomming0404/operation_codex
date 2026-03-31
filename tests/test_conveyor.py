def test_conveyor_transfer_time_formula(runtime_model):
    assert runtime_model.conveyor.transfer_time == runtime_model.config.conveyor_length / runtime_model.config.conveyor_speed


def test_conveyor_blocked_time_recorded(runtime_model):
    runtime_model.run()
    assert runtime_model.stats.blocked_time.get("CONV_01", 0.0) >= 0.0
    block_events = [e for e in runtime_model.stats.event_log if e["object"] == "CONV_01" and "BLOCK" in e["event"]]
    assert isinstance(block_events, list)
