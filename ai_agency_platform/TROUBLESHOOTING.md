# Docker Compose Build Troubleshooting

This document addresses two common failures seen during `docker compose up --build`.

## 1) Frontend error: `/app/.next/standalone: not found`

### Why it happens
Your frontend Dockerfile copies `.next/standalone`, but Next.js only generates that folder when **standalone output** is enabled.

### Fix
1. In your frontend `next.config.js` (or `next.config.mjs`), enable standalone output:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
};

module.exports = nextConfig;
```

2. Rebuild the frontend image without cache:

```bash
docker compose build --no-cache frontend
```

3. If you intentionally do **not** want standalone mode, update your frontend Dockerfile to copy the regular build output instead of `/app/.next/standalone`.

## 2) Pipeline build pulls huge CUDA/NVIDIA packages from `sentence-transformers`

### Why it happens
`sentence-transformers` pulls `torch`, and your resolver may select CUDA-enabled wheels, which are very large and slow.

### Fix (CPU-only)
Install CPU torch first, then install the rest:

```dockerfile
# In pipeline-service Dockerfile
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install --no-cache-dir chromadb pypdf python-docx sentence-transformers
```

Optional: pin versions to avoid unexpected resolver changes.

## 3) Recommended quick verification

```bash
docker compose build --no-cache frontend pipeline-service
docker compose up
```

If frontend still fails, run inside the frontend builder stage:

```bash
npm run build && ls -la .next && ls -la .next/standalone
```

That confirms whether standalone artifacts are actually produced.
