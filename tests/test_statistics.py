from services.report_builder import ReportBuilder


def test_kpi_computable(runtime_model):
    runtime_model.run()
    report = ReportBuilder.integrated_report(
        runtime_model.stats,
        runtime_model.config.simulation_time,
        runtime_model.drain.completed_count,
        runtime_model.worker_01.busy_time,
    )
    assert "throughput" in report
    assert "avg_wip" in report
    assert "worker_utilization" in report
