def test_source_stops_after_simulation_time(runtime_model):
    runtime_model.run()
    assert runtime_model.env.now == runtime_model.config.simulation_time
    assert runtime_model.source.generated_count <= int(runtime_model.config.simulation_time / 7.0) + 2


def test_source_generates_expected_range(runtime_model):
    runtime_model.run()
    assert runtime_model.source.generated_count >= 15
    assert runtime_model.source.generated_count <= 18
