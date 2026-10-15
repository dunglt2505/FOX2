using System.Text.Json;
using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.Services;

public static class BridgeJsonParser
{
    public static BridgeStatusSnapshot ParseWorkerStatus(string json)
    {
        using var document = JsonDocument.Parse(json);
        var root = document.RootElement;

        var state = Text(root, "state", "STOPPED");
        var paused = Bool(root, "paused");
        var stopRequested = Bool(root, "stop_requested");
        var currentDispatch = OptionalText(root, "current_dispatch");
        var heartbeat = Date(root, "heartbeat");
        var lastPoll = Date(root, "last_poll");
        var lastError = OptionalText(root, "last_error");
        var startWithWindows = Bool(root, "start_with_windows");

        var lastResultStatus = "none";
        if (root.TryGetProperty("last_result", out var lastResult) &&
            lastResult.ValueKind == JsonValueKind.Object)
        {
            lastResultStatus = Text(lastResult, "status", "none");
        }

        var execution = ParseExecution(root);
        var tools = ParseTools(root);

        return new BridgeStatusSnapshot(
            state,
            paused,
            stopRequested,
            currentDispatch,
            heartbeat,
            lastPoll,
            lastError,
            startWithWindows,
            lastResultStatus,
            execution,
            tools);
    }

    private static ExecutionSummary ParseExecution(JsonElement root)
    {
        if (!root.TryGetProperty("execution_display", out var execution) ||
            execution.ValueKind != JsonValueKind.Object)
        {
            return EmptyExecution();
        }

        var requested = execution.TryGetProperty("requested", out var requestedElement) &&
                        requestedElement.ValueKind == JsonValueKind.Object
            ? requestedElement
            : default;

        var metadata = execution.TryGetProperty("metadata", out var metadataElement) &&
                       metadataElement.ValueKind == JsonValueKind.Object
            ? metadataElement
            : default;

        var appliedPermission = "";
        if (metadata.ValueKind == JsonValueKind.Object &&
            metadata.TryGetProperty("applied_permission", out var applied) &&
            applied.ValueKind == JsonValueKind.Object)
        {
            appliedPermission = Text(applied, "profile", "");
        }

        return new ExecutionSummary(
            requested.ValueKind == JsonValueKind.Object ? Text(requested, "product", "") : "",
            requested.ValueKind == JsonValueKind.Object ? Text(requested, "model", "") : "",
            requested.ValueKind == JsonValueKind.Object ? Text(requested, "reasoning_effort", "") : "",
            requested.ValueKind == JsonValueKind.Object ? Text(requested, "permission_profile", "") : "",
            metadata.ValueKind == JsonValueKind.Object ? Text(metadata, "observed_model", "NOT_EXPOSED") : "NOT_EXPOSED",
            appliedPermission,
            metadata.ValueKind == JsonValueKind.Object ? Text(metadata, "observed_permission_profile", "NOT_EXPOSED") : "NOT_EXPOSED",
            metadata.ValueKind == JsonValueKind.Object ? JsonOrFallback(metadata, "usage", "Not exposed by CLI") : "Not exposed by CLI",
            metadata.ValueKind == JsonValueKind.Object ? JsonOrFallback(metadata, "capacity", "Not exposed by CLI") : "Not exposed by CLI");
    }

    private static IReadOnlyList<ToolStatus> ParseTools(JsonElement root)
    {
        if (!root.TryGetProperty("tools", out var tools) ||
            tools.ValueKind != JsonValueKind.Array)
            return Array.Empty<ToolStatus>();

        var result = new List<ToolStatus>();
        foreach (var item in tools.EnumerateArray())
        {
            result.Add(new ToolStatus(
                Text(item, "tool_name", "unknown"),
                Bool(item, "available"),
                Text(item, "auth_status", "UNVERIFIED"),
                Text(item, "version", "Not exposed"),
                OptionalText(item, "error")));
        }

        return result;
    }

    private static ExecutionSummary EmptyExecution() =>
        new("", "", "", "", "NOT_EXPOSED", "", "NOT_EXPOSED", "Not exposed by CLI", "Not exposed by CLI");

    private static string Text(JsonElement element, string property, string fallback)
    {
        if (element.ValueKind == JsonValueKind.Object &&
            element.TryGetProperty(property, out var value) &&
            value.ValueKind == JsonValueKind.String)
        {
            return value.GetString() ?? fallback;
        }

        return fallback;
    }

    private static string? OptionalText(JsonElement element, string property)
    {
        if (element.ValueKind == JsonValueKind.Object &&
            element.TryGetProperty(property, out var value) &&
            value.ValueKind == JsonValueKind.String)
        {
            return value.GetString();
        }

        return null;
    }

    private static bool Bool(JsonElement element, string property)
    {
        return element.ValueKind == JsonValueKind.Object &&
               element.TryGetProperty(property, out var value) &&
               value.ValueKind is JsonValueKind.True or JsonValueKind.False &&
               value.GetBoolean();
    }

    private static DateTimeOffset? Date(JsonElement element, string property)
    {
        var value = OptionalText(element, property);
        return DateTimeOffset.TryParse(value, out var parsed) ? parsed : null;
    }

    private static string JsonOrFallback(JsonElement element, string property, string fallback)
    {
        if (!element.TryGetProperty(property, out var value) ||
            value.ValueKind is JsonValueKind.Null or JsonValueKind.Undefined)
            return fallback;

        return value.ValueKind == JsonValueKind.String
            ? value.GetString() ?? fallback
            : value.GetRawText();
    }
}
