import hashlib

def generate_query_hash(sql: str) -> str:
    normalized = sql.strip().encode()
    return hashlib.sha3_384(normalized).hexdigest()
