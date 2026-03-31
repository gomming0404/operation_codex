from services.report_builder import ReportBuilder


def test_object_and_integrated_report(runtime_model):
    runtime_model.run()
    obj = ReportBuilder.object_report(runtime_model.stats, runtime_model.config.simulation_time)
    integ = ReportBuilder.integrated_report(runtime_model.stats, runtime_model.config.simulation_time, runtime_model.drain.completed_count, runtime_model.worker_01.busy_time)
    assert "BUF_01" in obj
    assert "throughput" in integ
    assert integ["throughput"] == runtime_model.drain.completed_count
