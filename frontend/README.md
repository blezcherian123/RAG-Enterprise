# Homeegram frontend

React and Vite dashboard for role-scoped company assistants.

## Local development

```bash
npm install
npm run dev
```

The API defaults to `http://localhost:8000`. Set `VITE_API_BASE_URL` to the deployed API origin when building the frontend, for example:

```dotenv
VITE_API_BASE_URL=https://api.example.com
```

All four assistant cards are currently available. The chat screen provides local role-aware demo replies; it is not connected to an AI or company retrieval service.
