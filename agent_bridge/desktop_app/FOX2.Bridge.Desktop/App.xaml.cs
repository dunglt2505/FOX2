using System.Security.Principal;
using System.Windows;
using FOX2.Bridge.Desktop.Services;
using FOX2.Bridge.Desktop.ViewModels;

namespace FOX2.Bridge.Desktop;

public partial class App : Application
{
    private Mutex? _mutex;
    private TrayService? _tray;
    private MainWindow? _window;
    private MainViewModel? _viewModel;

    protected override async void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        var sid = WindowsIdentity.GetCurrent().User?.Value ?? Environment.UserName;
        _mutex = new Mutex(false, $"Local\\FOX2BridgeDesktop-{sid}");
        try
        {
            if (!_mutex.WaitOne(0))
            {
                Shutdown();
                return;
            }
        }
        catch (AbandonedMutexException)
        {
        }

        var settings = new AppSettingsService();
        var client = new BridgeControlClient(new BridgeRuntimeLocator());
        _tray = new TrayService();
        _viewModel = new MainViewModel(client, settings, _tray);

        _window = new MainWindow { DataContext = _viewModel };

        _tray.OpenRequested += ShowMainWindow;
        _tray.ExitRequested += async () =>
        {
            await _viewModel.RequestExitAsync();
            _window.AllowRealClose = true;
            _window.Close();
            Shutdown();
        };
        _tray.PauseRequested += () => _viewModel.Dashboard.PauseCommand.Execute(null);
        _tray.ResumeRequested += () => _viewModel.Dashboard.ResumeCommand.Execute(null);
        _tray.CheckNowRequested += () => _viewModel.Dashboard.CheckNowCommand.Execute(null);
        _tray.OpenLogsRequested += () => _viewModel.Diagnostics.OpenLogsCommand.Execute(null);

        _window.Show();
        await _viewModel.StartAsync();
    }

    private void ShowMainWindow()
    {
        if (_window is null)
            return;

        if (!_window.IsVisible)
            _window.Show();

        if (_window.WindowState == WindowState.Minimized)
            _window.WindowState = WindowState.Normal;

        _window.Activate();
        _window.Topmost = true;
        _window.Topmost = false;
        _window.Focus();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _viewModel?.Dispose();
        _tray?.Dispose();

        if (_mutex is not null)
        {
            try { _mutex.ReleaseMutex(); } catch (ApplicationException) { }
            _mutex.Dispose();
        }

        base.OnExit(e);
    }
}
