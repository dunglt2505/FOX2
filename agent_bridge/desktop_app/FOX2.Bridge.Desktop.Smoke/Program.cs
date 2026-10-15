using FOX2.Bridge.Desktop.Services;

static void Assert(bool condition, string message)
{
    if (!condition)
        throw new InvalidOperationException(message);
}

var statusJson = """
{
  "state": "PAUSED",
  "paused": true,
  "stop_requested": false,
  "heartbeat": "2026-10-15T14:30:00+00:00",
  "last_poll": "2026-10-15T14:29:30+00:00",
  "start_with_windows": true,
  "last_result": {"status": "NO_ELIGIBLE_DISPATCH"},
  "execution_display": {
    "requested": {
      "product": "CODEX",
      "model": "gpt-6.1-sol",
      "reasoning_effort": "medium",
      "permission_profile": "FULL_ACCESS"
    },
    "metadata": {
      "observed_model": "NOT_EXPOSED",
      "applied_permission": {"profile": "FULL_ACCESS"},
      "observed_permission_profile": "NOT_EXPOSED",
      "usage": null,
      "capacity": null
    }
  },
  "tools": [
    {
      "tool_name": "codex",
      "available": true,
      "auth_status": "AUTHENTICATED",
      "version": "codex-cli fixture",
      "error": null
    }
  ]
}
""";

var status = BridgeJsonParser.ParseWorkerStatus(statusJson);
Assert(status.RawState == "PAUSED", "state mapping failed");
Assert(status.Paused, "paused mapping failed");
Assert(status.StartWithWindows, "startup mapping failed");
Assert(status.Execution.RequestedProduct == "CODEX", "agent mapping failed");
Assert(status.Execution.RequestedModel == "gpt-6.1-sol", "model mapping failed");
Assert(status.Execution.RequestedPermission == "FULL_ACCESS", "permission mapping failed");
Assert(status.Tools.Count == 1 && status.Tools[0].AuthStatus == "AUTHENTICATED", "tool mapping failed");
Assert(status.Execution.Usage == "Not exposed by CLI", "usage fallback failed");

var temp = Path.Combine(Path.GetTempPath(), "fox2-desktop-smoke-" + Guid.NewGuid().ToString("N"));
try
{
    var bridge = Path.Combine(temp, "FOX2", "AgentBridge");
    var version = Path.Combine(bridge, "versions", "fixture", "runtime", "Scripts");
    Directory.CreateDirectory(version);
    File.WriteAllText(Path.Combine(bridge, "current.json"), "{\"package_sha256\":\"fixture\"}");
    File.WriteAllBytes(Path.Combine(version, "python.exe"), [0]);

    var locator = new BridgeRuntimeLocator(temp);
    var resolved = locator.ResolvePythonPath();

    Assert(
        resolved == Path.Combine(version, "python.exe"),
        "runtime locator did not resolve the immutable installed version");
}
finally
{
    try { Directory.Delete(temp, recursive: true); } catch { }
}

Console.WriteLine("FOX2_BRIDGE_DESKTOP_SMOKE=PASS");
