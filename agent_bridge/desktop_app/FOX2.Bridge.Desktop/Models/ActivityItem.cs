namespace FOX2.Bridge.Desktop.Models;

public sealed record ActivityItem(
    DateTimeOffset Timestamp,
    string Type,
    string Message,
    string Status);
