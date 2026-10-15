using System.Collections.ObjectModel;
using System.Windows.Input;
using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;
using FOX2.Bridge.Desktop.Services;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class DiagnosticsViewModel : ObservableObject
{
    private readonly IBridgeControlClient _client;
    private string _statusMessage = "Ready";

    public DiagnosticsViewModel(IBridgeControlClient client)
    {
        _client = client;
        OpenLogsCommand = new AsyncRelayCommand(OpenLogsAsync);
        SaveSupportBundleCommand = new AsyncRelayCommand(SaveSupportBundleAsync);
    }

    public ObservableCollection<ToolStatus> Tools { get; } = [];

    public ICommand OpenLogsCommand { get; }
    public ICommand SaveSupportBundleCommand { get; }

    public string StatusMessage
    {
        get => _statusMessage;
        private set => SetProperty(ref _statusMessage, value);
    }

    public string BridgeRoot => _client.BridgeRoot;

    public void Update(BridgeStatusSnapshot snapshot)
    {
        Tools.Clear();
        foreach (var tool in snapshot.Tools)
            Tools.Add(tool);

        StatusMessage = snapshot.RawState is "DEGRADED" or "ERROR"
            ? snapshot.LastError ?? "Bridge needs attention."
            : "Bridge runtime is responding.";
    }

    private async Task OpenLogsAsync()
    {
        try
        {
            await _client.OpenLogsAsync();
            StatusMessage = "Logs opened.";
        }
        catch (Exception ex)
        {
            StatusMessage = ex.Message;
        }
    }

    private async Task SaveSupportBundleAsync()
    {
        var dialog = new Microsoft.Win32.SaveFileDialog
        {
            Filter = "ZIP archive (*.zip)|*.zip",
            FileName = $"FOX2-support-{DateTime.Now:yyyyMMdd-HHmmss}.zip"
        };

        if (dialog.ShowDialog() != true)
            return;

        try
        {
            await _client.SaveSupportBundleAsync(dialog.FileName);
            StatusMessage = "Sanitized support bundle saved.";
        }
        catch (Exception ex)
        {
            StatusMessage = ex.Message;
        }
    }
}
