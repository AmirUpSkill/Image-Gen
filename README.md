# Image-Gen

A starter repository for an image generation project with separate backend and frontend.

## Features
- Separate `backend/` and `frontend/`
- Standard `.gitignore` for Node and Python
- Ready to extend with your preferred stack

## Structure
```
Image-Gen/
├─ backend/
└─ frontend/
```

## Getting started
- Frontend (example with Vite):
  1. `cd frontend`
  2. Initialize: `npm create vite@latest . -- --template react-ts`
  3. Install & run: `npm install && npm run dev`

- Backend (Python example):
  1. `cd backend`
  2. `python -m venv .venv`
  3. Activate: Linux/macOS `source .venv/bin/activate`, Windows PowerShell `.venv\\Scripts\\Activate.ps1`
  4. `pip install -U pip`

## Environment
- Do not commit secrets. Use `.env`, and commit an `.env.example` with placeholders.

## Contributing
- Fork, branch, open PRs. Keep commits focused.

## License
MIT
