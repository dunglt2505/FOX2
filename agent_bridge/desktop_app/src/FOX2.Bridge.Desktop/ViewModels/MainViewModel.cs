using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Input;
using FOX2.Bridge.Desktop.Services;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class AsyncCommand : ICommand
{
    readonly Func<Task> execute; readonly Func<bool> allowed; bool running;
    public AsyncCommand(Func<Task> execute, Func<bool>? allowed = null) { this.execute = execute; this.allowed = allowed ?? (() => true); }
    public bool CanExecute(object? parameter) => !running && allowed();
    public async void Execute(object? parameter) {
        if (!CanExecute(parameter)) return;
        running = true; Changed();
        try { await execute(); } finally { running = false; Changed(); }
    }
    public event EventHandler? CanExecuteChanged;
    public void Changed() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}

public sealed class MainViewModel : INotifyPropertyChanged
{
    readonly BridgeControlClient client = new(); readonly ArtifactVaultService vault = new();
    JsonElement status; bool refreshing; string error = ""; string? previous; bool exiting;
    public event PropertyChangedEventHandler? PropertyChanged;
    public event Action? GracefulExitComplete;
    public ObservableCollection<string> Activity { get; } = new();
    public ObservableCollection<ArtifactRecord> Artifacts { get; } = new();
    public string State => Text(status, "state");
    public bool Paused => Flag(status, "paused") || State == "PAUSED";
    public string StatusLabel => Label(State);
    public string Polling => Paused ? "Polling: Paused" : "Polling: Worker schedule";
    public string CurrentTask => Text(status, "current_dispatch", "No active task");
    public string Heartbeat => Text(status, "heartbeat", "No heartbeat yet");
    public string WorkerHealth {
        get {
            if (!DateTimeOffset.TryParse(Text(status, "heartbeat"), out var heartbeat)) return "Worker heartbeat unavailable";
            return DateTimeOffset.UtcNow - heartbeat > TimeSpan.FromSeconds(30) ? "Worker heartbeat stale — check Diagnostics" : "Worker heartbeat current";
        }
    }
    public string LastResult => status.ValueKind == JsonValueKind.Object && status.TryGetProperty("last_result", out var result)
        ? Text(result, "status", "Result recorded") : "No result provided";
    public string AgentSummary {
        get {
            if (status.ValueKind != JsonValueKind.Object || !status.TryGetProperty("last_result", out var last) ||
                last.ValueKind != JsonValueKind.Object || !last.TryGetProperty("execution", out var execution) ||
                execution.ValueKind != JsonValueKind.Object || !execution.TryGetProperty("agent_metadata", out var metadata) ||
                metadata.ValueKind != JsonValueKind.Object) return "Last execution: Agent, model, permission and usage not provided by Worker";
            var requested = metadata.TryGetProperty("requested", out var request) ? request : default;
            return "Last Agent: " + Text(execution, "agent_product") + "\nRequested model: " + Text(requested, "model") +
                "\nRequested permission: " + Text(requested, "permission_profile") +
                "\nObserved model: " + Text(metadata, "observed_model") + "\nObserved permission: " + Text(metadata, "observed_permission_profile") +
                "\nQuota: " + Text(metadata, "quota");
        }
    }
    public string Agents => status.ValueKind == JsonValueKind.Object && status.TryGetProperty("tools", out var tools) && tools.ValueKind == JsonValueKind.Array
        ? string.Join("\n\n", tools.EnumerateArray().Where(t => Text(t, "tool_name") is "codex" or "copilot").Select(ToolLabel)) : "Agent readiness not yet provided by Worker";
    public string Diagnostics {
        get {
            string installation;
            try { var located = new BridgeInstallationLocator().Locate(); installation = "Package SHA-256: " + located.Package + "\nSource SHA-256: " + located.Source; }
            catch { installation = "Installed pointer unavailable"; }
            var tools = status.ValueKind == JsonValueKind.Object && status.TryGetProperty("tools", out var list) && list.ValueKind == JsonValueKind.Array
                ? string.Join("\n", list.EnumerateArray().Select(ToolLabel)) : "Tool versions not provided";
            return installation + "\n\nWorker: " + StatusLabel + "\nHeartbeat: " + Heartbeat + "\n" + WorkerHealth + "\nLast sanitized error: " + Text(status, "last_error", "None") + "\n\n" + tools + "\n\n" + error;
        }
    }
    public string Message => error;
    public bool StartWithWindows => Flag(status, "start_with_windows");
    public bool BusyExit => exiting;
    public string ExitLabel => exiting ? "Waiting for current task to finish…" : "Exit after current task";
    public AsyncCommand PauseResume { get; }
    public AsyncCommand CheckNow { get; }
    public AsyncCommand OpenLogs { get; }
    public AsyncCommand Exit { get; }
    public AsyncCommand EnableStartup { get; }
    public AsyncCommand DisableStartup { get; }
    public MainViewModel() {
        PauseResume = new(() => Control(Paused ? ControlAction.Resume : ControlAction.Pause), () => !exiting);
        CheckNow = new(() => Control(ControlAction.CheckNow), () => !Paused && !exiting &&
            status.ValueKind == JsonValueKind.Object && State is not ("STOPPED" or "STOPPING" or "STARTING" or "RECONCILING"));
        OpenLogs = new(() => Control(ControlAction.OpenLogs));
        Exit = new(async () => { await Control(ControlAction.RequestExit); if (error == "") { exiting = true; Notify(); } }, () => !exiting);
        EnableStartup = new(() => Control(ControlAction.SetStartWithWindows, true));
        DisableStartup = new(() => Control(ControlAction.SetStartWithWindows, false));
        ReloadArtifacts();
    }
    public async Task Refresh() {
        if (refreshing) return; refreshing = true;
        try {
            status = await client.InvokeAsync(ControlAction.Status); error = "";
            var transition = State + " / " + CurrentTask;
            if (transition != previous) { Activity.Insert(0, DateTimeOffset.Now.ToString("T") + " · " + StatusLabel + " · " + CurrentTask); previous = transition; }
            while (Activity.Count > 100) Activity.RemoveAt(Activity.Count - 1);
            if (exiting && State == "STOPPED") GracefulExitComplete?.Invoke();
        } catch { error = "Bridge control unavailable. Check installation and Worker status."; }
        finally { refreshing = false; Notify(); }
    }
    async Task Control(ControlAction action, bool? enabled = null) {
        try { await client.InvokeAsync(action, enabled); error = ""; await Refresh(); }
        catch { error = "Control failed. Open Diagnostics for installation details."; Notify(); }
    }
    public async Task SaveSupport(string path) {
        try { await client.DiagnosticsAsync(path); error = "Support bundle saved."; }
        catch { error = "Support export failed. Choose a local ZIP outside product data."; }
        Notify();
    }
    public async Task SaveArtifact(string path) {
        try { await Task.Run(() => vault.Save(path)); error = "Artifact verified and LOCAL_SAVED."; ReloadArtifacts(); }
        catch { error = "Artifact save failed. Choose an accessible local file up to 100 MiB."; }
        Notify();
    }
    void ReloadArtifacts() { try { Artifacts.Clear(); foreach (var record in vault.List()) Artifacts.Add(record); } catch { error = "Artifact index needs attention."; } }
    void Notify() {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(null));
        foreach (var command in new[] { PauseResume, CheckNow, Exit, OpenLogs, EnableStartup, DisableStartup }) command.Changed();
    }
    public static string Label(string state) => state switch {
        "STARTING" => "Starting", "RECONCILING" => "Recovering State", "IDLE" => "Ready", "POLLING" => "Checking",
        "EXECUTING" => "Agent Running", "PUBLISHING" => "Publishing", "PAUSED" => "Paused", "DEGRADED" => "Needs Attention",
        "ERROR" => "Action Required", "STOPPING" => "Stopping Safely", "STOPPED" => "Offline", _ => "Unknown" };
    public static string ToolLabel(JsonElement tool) {
        var available = Flag(tool, "available"); var auth = Text(tool, "auth_status");
        var readiness = !available ? "Unavailable" : auth == "AUTHENTICATED" ? "Available / authenticated" : auth == "NOT_AUTHENTICATED" ? "Available / sign-in required" : "Available / auth unverified";
        return Text(tool, "tool_name") + ": " + readiness + " · version " + Text(tool, "version", "Not provided by CLI");
    }
    static bool Flag(JsonElement element, string key) => element.ValueKind == JsonValueKind.Object && element.TryGetProperty(key, out var value) && value.ValueKind == JsonValueKind.True;
    static string Text(JsonElement element, string key, string fallback = "Not provided") {
        if (element.ValueKind != JsonValueKind.Object || !element.TryGetProperty(key, out var value) || value.ValueKind == JsonValueKind.Null) return fallback;
        var text = value.ToString();
        if (text == "NOT_EXPOSED") return "Not provided by CLI";
        text = Regex.Replace(text, @"(?i)(https?://)[^\s/]+@", "$1[redacted]@");
        text = Regex.Replace(text, @"(?i)(token|password|secret|authorization)\s*[:=]\s*\S+", "$1=[redacted]");
        text = Regex.Replace(text, @"(?i)(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})", "[redacted]");
        return text.Length > 1000 ? text[..1000] : text;
    }
}
