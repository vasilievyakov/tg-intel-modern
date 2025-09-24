import importlib, sys
mods=['apps.backend.app','apps.backend.api.channels','apps.backend.api.posts','apps.backend.api.summaries','apps.backend.services.telegram','apps.backend.services.fetcher','apps.backend.services.ai','apps.backend.core.db','apps.backend.core.config']
ok=True
for m in mods:
    try:
        importlib.import_module(m)
        print(f"IMPORTED:{m}")
    except Exception as e:
        print(f"IMPORT_ERROR:{m}:{e.__class__.__name__}:{e}")
        ok=False
sys.exit(0 if ok else 1)
