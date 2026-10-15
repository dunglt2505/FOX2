using System.Windows.Input;
using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;
using FOX2.Bridge.Desktop.Services;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class MainViewModel : ObservableObject, IDisposable
{
    private readonly IBridgeControlClient _client;
    private readonly TrayService _tray;
    private readonly CancellationTokenSource _stop = new();
    private object _currentPage;
    private string? _lastState;
    private string? _lastDispatch;
    private bool _started;

    public MainViewModel(
        IBridgeControlClient client,
        AppSettingsService settings,
        TrayService tray)
    {
        _client = client;
        _tray = tray;

        Dashboard = new DashboardViewModel(client);
        Activity = new ActivityViewModel();
        Agents = new AgentsViewModel();
        Diagnostics = new DiagnosticsViewModel(client);
        Settings = new SettingsViewModel(client, settings);

        Dashboard.RefreshRequested = RefreshOnceAsync;
        _currentPage = Dashboard;

        NavigateDashboardCommand = new RelayCommand(() => CurrentPage = Dashboard);
        NavigateActivityCommand = new RelayCommand(() => CurrentPage = Activity);
        NavigateAgentsCommand = new RelayCommand(() => CurrentPage = Agents);
        NavigateDiagnosticsCommand = new RelayCommand(() => CurrentPage = Diagnostics);
        NavigateSettingsCommand = new RelayCommand(() => CurrentPage = Settings);
    }

    public DashboardViewModel Dashboard { get; }
    public ActivityViewModel Activity { get; }
    public AgentsViewModel Agents { get; }
    public DiagnosticsViewModel Diagnostics { get; }
    public SettingsViewModel Settings { get; }

    public ICommand NavigateDashboardCommand { get; }
    public ICommand NavigateActivityCommand { get; }
    public ICommand NavigateAgentsCommand { get; }
    public ICommand NavigateDiagnosticsCommand { get; }
    public ICommand NavigateSettingsCommand { get; }

    public object CurrentPage
    {
        get => _currentPage;
        private set => SetProperty(ref _currentPage, value);
    }

    public async Task StartAsync()
    {
        if (_started)
            return;

        _started = true;
        await RefreshOnceAsync();
        _ = RefreshLoopAsync(_stop.Token);
    }

    public async Task RequestExitAsync()
    {
        try
        {
            await _client.RequestExitAsync();
            Activity.Add("Worker", "Exit after current task requested", "INFO");
        }
        catch (Exception ex)
        {
            Activity.Add("System", ex.Message, "ERROR");
        }
    }

    public async Task RefreshOnceAsync()
    {
        BridgeStatusSnapshot snapshot;
        try
        {
            snapshot = await _client.GetStatusAsync(_stop.Token);
        }
        catch (Exception ex)
        {
            snapshot = BridgeStatusSnapshot.Offline(ex.Message);
        }

        Dashboard.Update(snapshot);
        Agents.Update(snapshot);
        Diagnostics.Update(snapshot);
        Settings.Update(snapshot);
        _tray.Update(snapshot);

        if (_lastState != snapshot.RawState)
        {
            Activity.Add("Worker", $"Worker state: {snapshot.RawState}", StatusFor(snapshot.RawState));

            if (_lastState is not null &&
                snapshot.RawState is "DEGRADED" or "ERROR" &&
                Settings.Notifications)
            {
                _tray.Notify(
                    "FOX2 Bridge needs attention",
                    snapshot.LastError ?? $"Worker state is {snapshot.RawState}.",
                    System.Windows.Forms.ToolTipIcon.Warning);
            }

            _lastState = snapshot.RawState;
        }

        if (_lastDispatch != snapshot.CurrentDispatch)
        {
            if (!string.IsNullOrWhiteSpace(snapshot.CurrentDispatch))
                Activity.Add("Task", $"Active dispatch: {snapshot.CurrentDispatch}", "INFO");
            else if (!string.IsNullOrWhiteSpace(_lastDispatch))
                Activity.Add("Task", $"Dispatch finished or released: {_lastDispatch}", "PASS");

            _lastDispatch = snapshot.CurrentDispatch;
        }
    }

    private async Task RefreshLoopAsync(CancellationToken cancellationToken)
    {
        try
        {
            using var timer = new PeriodicTimer(TimeSpan.FromSeconds(2));
            while (await timer.WaitForNextTickAsync(cancellationToken))
                await RefreshOnceAsync();
        }
        catch (OperationCanceledException)
        {
        }
    }

    private static string StatusFor(string state) => state switch
    {
        "DEGRADED" or "ERROR" or "STOPPED" => "WARN",
        "PAUSED" => "INFO",
        _ => "PASS"
    };

    public void Dispose()
    {
        _stop.Cancel();
        _stop.Dispose();
    }
}
