from services.statistics_collector import StatisticsCollector


class ReportBuilder:
    @staticmethod
    def object_report(stats: StatisticsCollector, horizon: float) -> dict:
        out: dict[str, dict] = {}
        for obj, metric in stats.content_metrics.items():
            metric.observe(horizon, metric.last_value)
            out[obj] = {
                "avg_content": metric.avg(horizon),
                "max_content": metric.max_value,
                "blocked_time": stats.blocked_time.get(obj, 0.0),
            }
        return out

    @staticmethod
    def integrated_report(stats: StatisticsCollector, horizon: float, completed: int, worker_busy: float) -> dict:
        stats.wip_metric.observe(horizon, stats.wip_metric.last_value)
        return {
            "throughput": completed,
            "avg_lead_time": (sum(stats.lead_times) / len(stats.lead_times)) if stats.lead_times else 0.0,
            "avg_wip": stats.wip_metric.avg(horizon),
            "max_wip": stats.wip_metric.max_value,
            "total_blocked_time": sum(stats.blocked_time.values()),
            "worker_utilization": (worker_busy / horizon) if horizon > 0 else 0.0,
        }
