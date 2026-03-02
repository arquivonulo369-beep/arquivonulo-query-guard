from google.cloud import bigquery
from datetime import datetime

from .config import PROJECT_ID, THRESHOLD_GB, DEFAULT_ENVIRONMENT
from .crypto import generate_query_hash
from .policy import PolicyEngine


client = bigquery.Client(project=PROJECT_ID)


def estimate_query_cost(sql: str) -> float:
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    query_job = client.query(sql, job_config=job_config)
    bytes_processed = query_job.total_bytes_processed
    return bytes_processed / (1024 ** 3)


def execute_query(sql: str):
    job_config = bigquery.QueryJobConfig(dry_run=False, use_query_cache=False)
    job = client.query(sql, job_config=job_config)
    job.result()


def resolve_threshold(cli_threshold):
    return cli_threshold if cli_threshold is not None else THRESHOLD_GB


def run_guard(
    sql: str,
    query_name: str,
    environment: str = DEFAULT_ENVIRONMENT,
    cli_threshold: float | None = None,
    simulate: bool = False
) -> dict:

    threshold_gb = resolve_threshold(cli_threshold)
    query_hash = generate_query_hash(sql)

    policy = PolicyEngine(threshold_gb)

    # 1️⃣ Validação sintática antes de qualquer chamada externa
    pre_blocked, pre_reason = policy.evaluate(sql, 0.0, environment)

    if pre_blocked:
        return {
            "query_name": query_name,
            "query_hash": query_hash,
            "estimated_gb": 0.0,
            "threshold_gb": threshold_gb,
            "blocked": True,
            "block_reason": pre_reason,
            "environment": environment,
            "mode": "simulate" if simulate else "execute",
            "timestamp": datetime.utcnow().isoformat()
        }

    # 2️⃣ Agora sim estimamos custo
    try:
        estimated_gb = estimate_query_cost(sql)
    except Exception as e:
        return {
            "query_name": query_name,
            "query_hash": query_hash,
            "estimated_gb": 0.0,
            "threshold_gb": threshold_gb,
            "blocked": True,
            "block_reason": f"Engine error: {str(e)}",
            "environment": environment,
            "mode": "simulate" if simulate else "execute",
            "timestamp": datetime.utcnow().isoformat()
        }

    # 3️⃣ Avaliação final com custo real
    blocked, block_reason = policy.evaluate(sql, estimated_gb, environment)

    if not blocked and not simulate:
        execute_query(sql)

    return {
        "query_name": query_name,
        "query_hash": query_hash,
        "estimated_gb": round(estimated_gb, 6),
        "threshold_gb": threshold_gb,
        "blocked": blocked,
        "block_reason": block_reason,
        "environment": environment,
        "mode": "simulate" if simulate else "execute",
        "timestamp": datetime.utcnow().isoformat()
    }

