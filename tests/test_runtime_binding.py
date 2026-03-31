def test_runtime_binding_smoke(anchor_repo, minimal_scenario, deterministic_distribution):
    from services.runtime_model_builder import RuntimeModelBuilder

    model = RuntimeModelBuilder(anchor_repo).build(minimal_scenario, distribution=deterministic_distribution)
    assert model.source.anchor_set.object_id == "SRC_01"
    assert model.buffer.anchor_set.get("worker_pickup")
    assert model.worker_pool.get_single_worker().worker_id == "WORKER_01"
    model.run(until=30)
    assert model.env.now == 30
