namespace FOX2.Bridge.Desktop.Models;

public sealed record ExecutionSummary(
    string RequestedProduct,
    string RequestedModel,
    string RequestedReasoning,
    string RequestedPermission,
    string ObservedModel,
    string AppliedPermission,
    string ObservedPermission,
    string Usage,
    string Capacity);

public sealed record BridgeStatusSnapshot(
    string RawState,
    bool Paused,
    bool StopRequested,
    string? CurrentDispatch,
    DateTimeOffset? Heartbeat,
    DateTimeOffset? LastPoll,
    string? LastError,
    bool StartWithWindows,
    string LastResultStatus,
    ExecutionSummary Execution,
    IReadOnlyList<ToolStatus> Tools)
{
    public static BridgeStatusSnapshot Offline(string error) =>
        new(
            "STOPPED",
            true,
            false,
            null,
            null,
            null,
            error,
            false,
            "none",
            new ExecutionSummary(
                "",
                "",
                "",
                "",
                "NOT_EXPOSED",
                "",
                "NOT_EXPOSED",
                "Not exposed by CLI",
                "Not exposed by CLI"),
            Array.Empty<ToolStatus>());
}
