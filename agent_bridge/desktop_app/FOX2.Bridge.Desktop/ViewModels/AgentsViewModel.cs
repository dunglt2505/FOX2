using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class AgentsViewModel : ObservableObject
{
    private BridgeStatusSnapshot _snapshot = BridgeStatusSnapshot.Offline("Not connected.");

    public string CodexStatus => AgentStatus("codex");
    public string CopilotStatus => AgentStatus("copilot");
    public string CodexVersion => AgentVersion("codex");
    public string CopilotVersion => AgentVersion("copilot");
    public string RequestedModel => EmptyAs(_snapshot.Execution.RequestedModel, "Dispatch controlled");
    public string RequestedReasoning => EmptyAs(_snapshot.Execution.RequestedReasoning, "Not active");
    public string RequestedPermission => EmptyAs(_snapshot.Execution.RequestedPermission, "Not active");
    public string ObservedModel => EmptyAs(_snapshot.Execution.ObservedModel, "NOT_EXPOSED");
    public string Usage => _snapshot.Execution.Usage;
    public string Capacity => _snapshot.Execution.Capacity;

    public void Update(BridgeStatusSnapshot snapshot)
    {
        _snapshot = snapshot;
        foreach (var property in new[]
        {
            nameof(CodexStatus), nameof(CopilotStatus), nameof(CodexVersion), nameof(CopilotVersion),
            nameof(RequestedModel), nameof(RequestedReasoning), nameof(RequestedPermission),
            nameof(ObservedModel), nameof(Usage), nameof(Capacity)
        })
        {
            Raise(property);
        }
    }

    private string AgentStatus(string name)
    {
        var tool = _snapshot.Tools.FirstOrDefault(
            item => string.Equals(item.Name, name, StringComparison.OrdinalIgnoreCase));

        if (tool is null || !tool.Available)
            return "Not available";

        return tool.AuthStatus switch
        {
            "AUTHENTICATED" => "Authenticated",
            "UNVERIFIED" => "Authentication not verified",
            _ => tool.AuthStatus.Replace('_', ' ').ToLowerInvariant()
        };
    }

    private string AgentVersion(string name) =>
        _snapshot.Tools.FirstOrDefault(
            item => string.Equals(item.Name, name, StringComparison.OrdinalIgnoreCase))?.Version
        ?? "Not exposed";

    private static string EmptyAs(string value, string fallback) =>
        string.IsNullOrWhiteSpace(value) ? fallback : value;
}
