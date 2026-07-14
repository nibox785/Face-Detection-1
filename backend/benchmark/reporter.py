import csv
import json
from pathlib import Path

REPORT_ROOT = Path(__file__).resolve().parents[2] / "reports" / "benchmark"
REPORT_ROOT.mkdir(parents=True, exist_ok=True)


class BenchmarkReporter:
    @staticmethod
    def save_json(summary: dict, file_name: str = "summary.json"):
        path = REPORT_ROOT / file_name
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        return path

    @staticmethod
    def save_csv(summary: dict, file_name: str = "summary.csv"):
        path = REPORT_ROOT / file_name
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "value"])
            writer.writerow(["total_runs", summary.get("total_runs", 0)])
            writer.writerow(["avg_face_count", summary.get("avg_face_count", 0.0)])
            writer.writerow(["avg_latency", summary.get("latency", {}).get("avg", 0.0)])
            writer.writerow(["p50_latency", summary.get("latency", {}).get("p50", 0.0)])
            writer.writerow(["p95_latency", summary.get("latency", {}).get("p95", 0.0)])
            writer.writerow(["p99_latency", summary.get("latency", {}).get("p99", 0.0)])
            for model, values in summary.get("models", {}).items():
                writer.writerow([f"model_{model}_avg_latency", values.get("avg", 0.0)])
                writer.writerow([f"model_{model}_p50", values.get("p50", 0.0)])
                writer.writerow([f"model_{model}_p95", values.get("p95", 0.0)])
                writer.writerow([f"model_{model}_p99", values.get("p99", 0.0)])
        return path

    @staticmethod
    def save_markdown(summary: dict, file_name: str = "summary.md"):
        path = REPORT_ROOT / file_name
        lines = ["# Benchmark Summary", "", "## Overview", ""]
        lines.append(f"- Total runs: {summary.get('total_runs', 0)}")
        lines.append(f"- Average face count: {summary.get('avg_face_count', 0.0):.2f}")
        latency = summary.get("latency", {})
        lines.append(f"- Average latency (ms): {latency.get('avg', 0.0):.2f}")
        lines.append(f"- p50 latency (ms): {latency.get('p50', 0.0):.2f}")
        lines.append(f"- p95 latency (ms): {latency.get('p95', 0.0):.2f}")
        lines.append(f"- p99 latency (ms): {latency.get('p99', 0.0):.2f}")
        lines.append("")
        lines.append("## Model Breakdown")
        for model, values in summary.get("models", {}).items():
            lines.append(f"### {model}")
            lines.append(f"- avg latency (ms): {values.get('avg', 0.0):.2f}")
            lines.append(f"- p50 latency (ms): {values.get('p50', 0.0):.2f}")
            lines.append(f"- p95 latency (ms): {values.get('p95', 0.0):.2f}")
            lines.append(f"- p99 latency (ms): {values.get('p99', 0.0):.2f}")
            lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return path
