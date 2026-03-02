from engine.logger import log_result

entry_hash = log_result({
    "event": "manual_test",
    "status": "ok",
    "environment": "dev"
})

print("Entry hash gerado:", entry_hash)

