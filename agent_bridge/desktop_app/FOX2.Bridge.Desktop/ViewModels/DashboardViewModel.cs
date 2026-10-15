using System.Windows.Input;
using System.Windows.Media;
using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;
using FOX2.Bridge.Desktop.Services;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class DashboardViewModel : ObservableObject
{
    private readonly IBridgeControlClient _client;
    private BridgeStatusSnapshot _snapshot = BridgeStatusSnapshot.Offline("Not connected yet.");
    private string? _actionError;

    public DashboardViewModel(IBridgeControlClient client)
    {
        _client = client;
        PauseCommand = new AsyncRelayCommand(PauseAsync, CanPause);
        ResumeCommand = new AsyncRelayCommand(ResumeAsync, CanResume);
        CheckNowCommand = new AsyncRelayCommand(CheckNowAsync, CanControl);
    }

    public Func<Task>? RefreshRequested { get; set; }

    public ICommand PauseCommand { get; }
    public ICommand ResumeCommand { get; }
    public ICommand CheckNowCommand { get; }

    private bool HeartbeatStale =>
        _snapshot.Heartbeat is null ||
        DateTimeOffset.UtcNow - _snapshot.Heartbeat.Value > TimeSpan.FromSeconds(60);

    private bool CanControl() =>
        !HeartbeatStale &&
        _snapshot.RawState is not "STOPPED" and not "STOPPING";

    private bool CanPause() => CanControl() && !_snapshot.Paused;
    private bool CanResume() => CanControl() && _snapshot.Paused;

    public string StateDisplay
    {
        get
        {
            if (HeartbeatStale && _snapshot.RawState is not "STARTING" and not "RECONCILING")
                return "OFFLINE";

            return _snapshot.RawState switch
            {
                "IDLE" => "READY",
                "POLLING" => "CHECKING",
                "EXECUTING" => "AGENT RUNNING",
                "PUBLISHING" => "PUBLISHING",
                "PAUSED" => "PAUSED",
                "DEGRADED" => "NEEDS ATTENTION",
                "ERROR" => "ACTION REQUIRED",
                "STARTING" => "STARTING",
                "RECONCILING" => "RECOVERING",
                "STOPPING" => "STOPPING",
                "STOPPED" => "OFFLINE",
                _ => _snapshot.RawState
            };
        }
    }

    public string HeaderSubtext =>
        HeartbeatStale
            ? "Heartbeat stale"
            : _snapshot.RawState == "PAUSED"
                ? "Worker alive"
                : _snapshot.RawState is "DEGRADED" or "ERROR"
                    ? "Review diagnostics"
                    : string.IsNullOrWhiteSpace(_snapshot.CurrentDispatch)
                        ? "Worker healthy"
                        : "Task active";

    public string HeroGlyph => StateDisplay switch
    {
        "PAUSED" => "Ⅱ",
        "AGENT RUNNING" => "▶",
        "PUBLISHING" => "↑",
        "READY" => "✓",
        "OFFLINE" => "!",
        "NEEDS ATTENTION" or "ACTION REQUIRED" => "!",
        _ => "•"
    };

    public string HeroTitle
    {
        get
        {
            if (StateDisplay == "OFFLINE")
                return "Bridge Worker is Offline";

            return _snapshot.RawState switch
            {
                "PAUSED" => "Bridge is Paused",
                "DEGRADED" => "Bridge Needs Attention",
                "ERROR" => "Bridge Requires Action",
                "EXECUTING" => "Agent is Running",
                "PUBLISHING" => "Publishing Result",
                "IDLE" => "Bridge is Ready",
                _ => "FOX2 Bridge"
            };
        }
    }

    public string HeroMessage
    {
        get
        {
            if (StateDisplay == "OFFLINE")
                return "The persisted status is readable, but the Worker heartbeat is not live.";

            return _snapshot.RawState switch
            {
                "PAUSED" => "Worker is healthy, but will not claim new tasks.",
                "DEGRADED" => _snapshot.LastError ?? "The last operation did not complete normally.",
                "ERROR" => _snapshot.LastError ?? "Bridge reported an error.",
                "EXECUTING" => "The current Agent task is being supervised by Bridge.",
                "PUBLISHING" => "Bridge is finalizing the authorized result.",
                "IDLE" => "Worker is healthy and ready for eligible work.",
                _ => "Worker status is being monitored."
            };
        }
    }

    public Brush HealthBrush =>
        HeartbeatStale || _snapshot.RawState is "DEGRADED" or "ERROR" or "STOPPED"
            ? new SolidColorBrush(Color.FromRgb(239, 68, 68))
            : _snapshot.RawState == "PAUSED"
                ? new SolidColorBrush(Color.FromRgb(245, 158, 11))
                : new SolidColorBrush(Color.FromRgb(34, 197, 94));

    public string WorkerFooterText =>
        HeartbeatStale || _snapshot.RawState == "STOPPED"
            ? "Worker Offline"
            : "Worker Running";

    public string CurrentTask =>
        string.IsNullOrWhiteSpace(_snapshot.CurrentDispatch) ? "No active task" : _snapshot.CurrentDispatch!;

    public string CurrentTaskSubtext =>
        string.IsNullOrWhiteSpace(_snapshot.CurrentDispatch)
            ? (_snapshot.Paused ? "Waiting for Resume…" : "Waiting for eligible work…")
            : _snapshot.RawState;

    public string LastPollText => Relative(_snapshot.LastPoll);
    public string HeartbeatText => Relative(_snapshot.Heartbeat);
    public string LastResult => _snapshot.LastResultStatus;
    public string AgentProduct => EmptyAs(_snapshot.Execution.RequestedProduct, "No active Agent");
    public string AgentModel => EmptyAs(_snapshot.Execution.RequestedModel, "Dispatch controlled");
    public string AgentReasoning => EmptyAs(_snapshot.Execution.RequestedReasoning, "Not active");
    public string AgentPermission => EmptyAs(_snapshot.Execution.RequestedPermission, "Not active");
    public string Usage => _snapshot.Execution.Usage;
    public string Capacity => _snapshot.Execution.Capacity;
    public string BridgeRoot => _client.BridgeRoot;
    public string? ActionError => _actionError;

    public void Update(BridgeStatusSnapshot snapshot)
    {
        _snapshot = snapshot;
        _actionError = null;

        foreach (var property in new[]
        {
            nameof(StateDisplay), nameof(HeaderSubtext), nameof(HeroGlyph), nameof(HeroTitle), nameof(HeroMessage),
            nameof(HealthBrush), nameof(WorkerFooterText), nameof(CurrentTask), nameof(CurrentTaskSubtext),
            nameof(LastPollText), nameof(HeartbeatText), nameof(LastResult), nameof(AgentProduct),
            nameof(AgentModel), nameof(AgentReasoning), nameof(AgentPermission), nameof(Usage),
            nameof(Capacity), nameof(BridgeRoot), nameof(ActionError)
        })
        {
            Raise(property);
        }

        (PauseCommand as AsyncRelayCommand)?.RaiseCanExecuteChanged();
        (ResumeCommand as AsyncRelayCommand)?.RaiseCanExecuteChanged();
        (CheckNowCommand as AsyncRelayCommand)?.RaiseCanExecuteChanged();
    }

    private async Task PauseAsync() => await RunControlAsync(_client.PauseAsync);
    private async Task ResumeAsync() => await RunControlAsync(_client.ResumeAsync);
    private async Task CheckNowAsync() => await RunControlAsync(_client.CheckNowAsync);

    private async Task RunControlAsync(Func<CancellationToken, Task> action)
    {
        try
        {
            await action(CancellationToken.None);
            if (RefreshRequested is not null)
                await RefreshRequested();
        }
        catch (Exception ex)
        {
            _actionError = ex.Message;
            Raise(nameof(ActionError));
        }
    }

    private static string Relative(DateTimeOffset? value)
    {
        if (value is null)
            return "Not available";

        var age = DateTimeOffset.UtcNow - value.Value;
        if (age.TotalSeconds < 5)
            return "just now";
        if (age.TotalMinutes < 1)
            return $"{Math.Max(1, (int)age.TotalSeconds)} sec ago";
        if (age.TotalHours < 1)
            return $"{Math.Max(1, (int)age.TotalMinutes)} min ago";

        return value.Value.ToLocalTime().ToString("HH:mm:ss");
    }

    private static string EmptyAs(string value, string fallback) =>
        string.IsNullOrWhiteSpace(value) ? fallback : value;
}
