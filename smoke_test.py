import ast
from pathlib import Path

main_source = Path("main.py").read_text(encoding="utf-8")
storage_source = Path("storage.py").read_text(encoding="utf-8")
main_tree = ast.parse(main_source)
storage_tree = ast.parse(storage_source)
main_defs = {node.name for node in ast.walk(main_tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
storage_defs = {node.name for node in ast.walk(storage_tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
required_main = {"valid_url", "extract_supported_url", "preview_media", "download_media", "receive_url", "format_selected", "music_page", "music_selected", "privacy_callback", "admin_stats"}
required_storage = {"init_db", "upsert_user", "has_consent", "log_link", "recent_links", "stats"}
missing_main = required_main - main_defs
missing_storage = required_storage - storage_defs
assert not missing_main, f"missing main definitions: {missing_main}"
assert not missing_storage, f"missing storage definitions: {missing_storage}"
assert 'CallbackQueryHandler(privacy_callback' in main_source
assert 'CallbackQueryHandler(music_page' in main_source
assert 'send_photo' in main_source
assert 'storage.init_db()' in main_source
print("smoke test passed")
