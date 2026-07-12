import numpy as np


def compute_latency_metrics(latencies_ms):
    if not latencies_ms:
        return {"count": 0, "avg": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0}
    values = np.array(latencies_ms, dtype=np.float32)
    return {
        "count": int(values.size),
        "avg": float(np.mean(values)),
        "p50": float(np.percentile(values, 50)),
        "p95": float(np.percentile(values, 95)),
        "p99": float(np.percentile(values, 99)),
    }


def compute_fps(latency_ms):
    return float(1000.0 / max(latency_ms, 1.0))


def compute_quality_histogram(face_ratings):
    bins = {"Excellent": 0, "Good": 0, "Acceptable": 0, "Poor": 0, "Unusable": 0}
    for r in face_ratings:
        if r in bins:
            bins[r] += 1
        else:
            bins["Unusable"] += 1
    return bins


def compute_summary_metrics(results):
    metrics = {
        "total_runs": len(results),
        "total_faces": sum(r.get("face_count", 0) for r in results),
        "avg_face_count": float(np.mean([r.get("face_count", 0) for r in results])) if results else 0.0,
        "latency": compute_latency_metrics([r.get("latency_ms", 0.0) for r in results]),
        "models": {},
    }
    models = {}
    for r in results:
        model = r.get("model", "unknown")
        models.setdefault(model, []).append(r.get("latency_ms", 0.0))
    for model, latencies in models.items():
        metrics["models"][model] = compute_latency_metrics(latencies)
    return metrics
