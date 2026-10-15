namespace FOX2.Bridge.Desktop.Models;

public sealed record ToolStatus(
    string Name,
    bool Available,
    string AuthStatus,
    string Version,
    string? Error);
