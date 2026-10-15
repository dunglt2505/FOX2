using System.Drawing;
using System.Windows.Forms;
using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.Services;

public sealed class TrayService : IDisposable
{
    private readonly NotifyIcon _icon;
    private readonly ToolStripMenuItem _pause;
    private readonly ToolStripMenuItem _resume;

    public event Action? OpenRequested;
    public event Action? PauseRequested;
    public event Action? ResumeRequested;
    public event Action? CheckNowRequested;
    public event Action? OpenLogsRequested;
    public event Action? ExitRequested;

    public TrayService()
    {
        var menu = new ContextMenuStrip();

        var open = new ToolStripMenuItem("Open Dashboard");
        open.Click += (_, _) => OpenRequested?.Invoke();

        _pause = new ToolStripMenuItem("Pause Bridge");
        _pause.Click += (_, _) => PauseRequested?.Invoke();

        _resume = new ToolStripMenuItem("Resume Bridge");
        _resume.Click += (_, _) => ResumeRequested?.Invoke();

        var check = new ToolStripMenuItem("Check now");
        check.Click += (_, _) => CheckNowRequested?.Invoke();

        var logs = new ToolStripMenuItem("Open logs");
        logs.Click += (_, _) => OpenLogsRequested?.Invoke();

        var exit = new ToolStripMenuItem("Exit after current task");
        exit.Click += (_, _) => ExitRequested?.Invoke();

        menu.Items.Add(open);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(_pause);
        menu.Items.Add(_resume);
        menu.Items.Add(check);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(logs);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(exit);

        _icon = new NotifyIcon
        {
            Visible = true,
            Icon = SystemIcons.Application,
            Text = "FOX2 Bridge",
            ContextMenuStrip = menu
        };

        _icon.DoubleClick += (_, _) => OpenRequested?.Invoke();
        _icon.Click += (_, args) =>
        {
            if (args is MouseEventArgs mouse && mouse.Button == MouseButtons.Left)
                OpenRequested?.Invoke();
        };
    }

    public void Update(BridgeStatusSnapshot snapshot)
    {
        var display = StateDisplay(snapshot.RawState);
        var task = string.IsNullOrWhiteSpace(snapshot.CurrentDispatch)
            ? string.Empty
            : " · " + snapshot.CurrentDispatch;

        var text = $"FOX2 Bridge · {display}{task}";
        _icon.Text = text.Length <= 63 ? text : text[..63];

        _pause.Enabled = !snapshot.Paused && snapshot.RawState is not "STOPPED" and not "STOPPING";
        _resume.Enabled = snapshot.Paused && snapshot.RawState is not "STOPPED" and not "STOPPING";
    }

    public void Notify(string title, string message, ToolTipIcon icon = ToolTipIcon.Info)
    {
        _icon.BalloonTipTitle = title;
        _icon.BalloonTipText = message;
        _icon.BalloonTipIcon = icon;
        _icon.ShowBalloonTip(4000);
    }

    private static string StateDisplay(string state) => state switch
    {
        "IDLE" => "Ready",
        "POLLING" => "Checking",
        "EXECUTING" => "Agent running",
        "PUBLISHING" => "Publishing",
        "PAUSED" => "Paused",
        "DEGRADED" => "Needs attention",
        "ERROR" => "Action required",
        "STARTING" => "Starting",
        "RECONCILING" => "Recovering",
        "STOPPING" => "Stopping",
        "STOPPED" => "Offline",
        _ => state
    };

    public void Dispose()
    {
        _icon.Visible = false;
        _icon.Dispose();
    }
}
