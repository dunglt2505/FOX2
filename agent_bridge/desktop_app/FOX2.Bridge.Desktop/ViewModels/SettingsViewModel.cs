using System.Windows.Input;
using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;
using FOX2.Bridge.Desktop.Services;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class SettingsViewModel : ObservableObject
{
    private readonly IBridgeControlClient _client;
    private readonly AppSettingsService _settingsService;
    private bool _startWithWindows;
    private bool _notifications;
    private bool _closeToTray;
    private string _status = "";

    public SettingsViewModel(IBridgeControlClient client, AppSettingsService settingsService)
    {
        _client = client;
        _settingsService = settingsService;

        var ui = settingsService.Load();
        _notifications = ui.Notifications;
        _closeToTray = ui.CloseToTray;

        ToggleStartupCommand = new AsyncRelayCommand(ToggleStartupAsync);
    }

    public ICommand ToggleStartupCommand { get; }

    public bool StartWithWindows
    {
        get => _startWithWindows;
        set => SetProperty(ref _startWithWindows, value);
    }

    public bool Notifications
    {
        get => _notifications;
        set
        {
            if (SetProperty(ref _notifications, value))
                SaveUiSettings();
        }
    }

    public bool CloseToTray
    {
        get => _closeToTray;
        set
        {
            if (SetProperty(ref _closeToTray, value))
                SaveUiSettings();
        }
    }

    public string Status
    {
        get => _status;
        private set => SetProperty(ref _status, value);
    }

    public void Update(BridgeStatusSnapshot snapshot) =>
        StartWithWindows = snapshot.StartWithWindows;

    private async Task ToggleStartupAsync()
    {
        try
        {
            await _client.SetStartWithWindowsAsync(StartWithWindows);
            Status = StartWithWindows
                ? "Bridge will start with Windows."
                : "Bridge startup registration disabled.";
        }
        catch (Exception ex)
        {
            StartWithWindows = !StartWithWindows;
            Status = ex.Message;
        }
    }

    private void SaveUiSettings() =>
        _settingsService.Save(new UiSettings(CloseToTray, Notifications));
}
