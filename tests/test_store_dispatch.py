def test_store_dispatch_to_drain(runtime_model):
    runtime_model.run()
    assert runtime_model.drain.completed_count >= 1
    drain_events = [e for e in runtime_model.stats.event_log if e["object"] == "DRAIN_01" and e["event"] == "DRAIN"]
    assert len(drain_events) == runtime_model.drain.completed_count
