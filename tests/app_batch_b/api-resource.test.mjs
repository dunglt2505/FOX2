import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

// Resolve TypeScript from the frontend's installed dependencies.
const requireFrontend = createRequire(new URL("../../frontend/package.json", import.meta.url));
const ts = requireFrontend("typescript");

function loadModule(path, fetchImpl = () => { throw new Error("Unexpected network request"); }) {
  const source = readFileSync(new URL(path, import.meta.url), "utf8");
  const compiled = ts.transpileModule(source, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS },
    reportDiagnostics: true
  });
  assert.deepEqual(compiled.diagnostics?.filter((d) => d.category === ts.DiagnosticCategory.Error), []);
  const exports = {};
  vm.runInNewContext(compiled.outputText, { exports, fetch: fetchImpl, Headers, URLSearchParams, Date }, { filename: path });
  return exports;
}

const ok = (body = {}) => new Response(JSON.stringify(body), {
  status: 200, headers: { "content-type": "application/json" }
});

test("investor API uses same-origin backend endpoints only, with CAS payload", async () => {
  const calls = [];
  const { api } = loadModule("../../frontend/src/api.ts", async (path, options) => {
    calls.push({ path, options });
    return ok({ items: [] });
  });
  await api.health();
  await api.sourceHealth();
  await api.overview();
  await api.watchlist();
  await api.replaceWatchlist(7, ["instrument-17"]);
  await api.searchStocks(" HPG & more ");
  await api.stock("  hpg ");
  await api.bars(" hpg ");

  assert.equal(calls.length, 8);
  for (const { path, options } of calls) {
    assert.match(path, /^\/api\//);
    assert.equal(path.startsWith("//"), false);
    assert.equal(options.headers.get("Accept"), "application/json");
  }
  const mutation = calls[4];
  assert.equal(mutation.path, "/api/watchlist");
  assert.equal(mutation.options.method, "PUT");
  assert.equal(mutation.options.headers.get("Content-Type"), "application/json");
  assert.deepEqual(JSON.parse(mutation.options.body), { expected_version: 7, items: ["instrument-17"] });
  assert.equal(calls[5].path, "/api/stocks?query=HPG%20%26%20more&limit=20");
  assert.equal(calls[6].path, "/api/stocks/HPG");
  assert.match(calls[7].path, /^\/api\/stocks\/HPG\/bars\?/);
});

test("API error text never reflects backend secrets, including 409 CAS", async () => {
  for (const status of [400, 401, 403, 404, 409, 422, 429, 500, 503]) {
    const { api } = loadModule("../../frontend/src/api.ts", async () =>
      new Response(JSON.stringify({ detail: "SECRET_TOKEN_DO_NOT_SHOW" }), { status })
    );
    await assert.rejects(api.watchlist(), (error) => {
      assert.equal(error.status, status);
      assert.equal(error.message.includes("SECRET_TOKEN_DO_NOT_SHOW"), false);
      assert.ok(error.message.length > 0);
      if (status === 409) assert.match(error.message, /version conflict/i);
      return true;
    });
  }
});

test("old Stock360 or refresh snapshots are never visible under a new request key", () => {
  const { visibleResource } = loadModule("../../frontend/src/resourceVisibility.ts");
  const prior = { key: "stock-AAA-0", data: { symbol: "AAA", last_price: 12 }, error: null, loading: false };
  const stale = visibleResource(prior, "stock-BBB-0");
  assert.equal(stale.data, null);
  assert.equal(stale.error, null);
  assert.equal(stale.loading, true);
  const refreshed = visibleResource(prior, "stock-AAA-1");
  assert.equal(refreshed.data, null);
  assert.equal(refreshed.loading, true);
  const current = visibleResource(prior, "stock-AAA-0");
  assert.equal(current.data.symbol, "AAA");
  assert.equal(current.loading, false);
});

test("healthy local backend must not masquerade as LIVE market data", () => {
  const { healthBadge, providerModeLabel } = loadModule("../../frontend/src/healthTruth.ts");
  const offline = { status: "OK", provider_enabled: false };
  assert.equal(healthBadge(offline), "OK");
  assert.notEqual(healthBadge(offline), "LIVE");
  assert.equal(providerModeLabel(offline), "Disabled / offline-safe");
  assert.equal(healthBadge({ status: "UNHEALTHY", provider_enabled: true }), "UNHEALTHY");
  assert.equal(providerModeLabel(null), "Unknown");
  assert.equal(healthBadge(null), "UNAVAILABLE");
});
