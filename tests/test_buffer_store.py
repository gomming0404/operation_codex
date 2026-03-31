def test_buffer_capacity_not_exceeded(runtime_model):
    runtime_model.run()
    assert runtime_model.buffer.current_content <= runtime_model.buffer.capacity


def test_buffer_store_content_metrics_exist(runtime_model):
    runtime_model.run()
    assert "BUF_01" in runtime_model.stats.content_metrics
    assert "STORE_01" in runtime_model.stats.content_metrics
