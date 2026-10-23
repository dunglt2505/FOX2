import { defineConfig, type Plugin } from "vite";
import type { IncomingMessage } from "node:http";
import react from "@vitejs/plugin-react";

const frontendAuthority = "127.0.0.1:5173";
const frontendOrigin = "http://" + frontendAuthority;
const backendOrigin = "http://127.0.0.1:8000";
const validatedRequests = new WeakSet<IncomingMessage>();

function localOriginGuard(): Plugin {
  return {
    name: "fox2-local-origin-guard",
    configureServer(server) {
      // Register directly here, before Vite installs its internal proxy.
      // rawHeaders preserves duplicates which req.headers may join/discard.
      server.middlewares.use((req, res, next) => {
        const values = (name: string) => {
          const result: string[] = [];
          for (let i = 0; i < req.rawHeaders.length; i += 2) {
            if (req.rawHeaders[i].toLowerCase() === name) result.push(req.rawHeaders[i + 1]);
          }
          return result;
        };
        const hosts = values("host");
        const origins = values("origin");
        const contentTypes = values("content-type");
        const reject = (status: number) => {
          res.statusCode = status;
          res.setHeader("Content-Type", "application/json");
          res.setHeader("Cache-Control", "no-store");
          res.end(JSON.stringify({ detail: status === 403 ? "Origin denied" : "Invalid request" }));
        };
        if (hosts.length !== 1 || hosts[0] !== frontendAuthority ||
            origins.length > 1 || contentTypes.length > 1) {
          reject(400);
          return;
        }
        const readOnly = ["GET", "HEAD", "OPTIONS"].includes(req.method || "");
        if ((origins.length === 1 && origins[0] !== frontendOrigin) ||
            (!readOnly && origins.length !== 1)) {
          reject(403);
          return;
        }
        validatedRequests.add(req);
        next();
      });
    }
  };
}

export default defineConfig({
  plugins: [localOriginGuard(), react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: {
      "/api": {
        target: backendOrigin,
        changeOrigin: true,
        configure(proxy) {
          proxy.on("proxyReq", (proxyReq, req) => {
            if (!validatedRequests.has(req)) {
              proxyReq.destroy(new Error("Unvalidated local API request"));
              return;
            }
            // Translate only an exact, prevalidated frontend Origin. Read-only
            // requests without Origin remain without Origin on the backend.
            if (req.headers.origin === frontendOrigin) {
              proxyReq.setHeader("origin", backendOrigin);
            }
          });
        }
      }
    }
  },
  build: {
    target: "es2022",
    sourcemap: true
  }
});
