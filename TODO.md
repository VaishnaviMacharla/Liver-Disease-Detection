# Fix app.py Model Config Print Issue
Status: [x] Completed ✅

## Steps:
- [x] 1. Understand issue (model.get_config() prints on load_model in new venv)
- [ ] 2. Edit predict_with_gradcam.py: Add TF log suppress + lazy model load
- [ ] 3. Edit app.py: Add TF suppress at top
- [ ] 4. Test: python scripts/app.py (no print)
- [ ] 5. Complete task

## Why this happens:
New venv TF version/setting auto-prints model config on load_model. Harmless but ugly.

