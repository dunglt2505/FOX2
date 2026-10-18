using System;
using System.ComponentModel;
using System.Windows;
using System.Windows.Threading;
using FOX2.Bridge.Desktop.Services;
using FOX2.Bridge.Desktop.ViewModels;
using Forms = System.Windows.Forms;

namespace FOX2.Bridge.Desktop;
public partial class MainWindow : Window
{
    readonly MainViewModel model = new(); readonly DispatcherTimer timer;
    readonly Forms.NotifyIcon tray; readonly Forms.ToolStripMenuItem pause, check;
    bool allowClose; bool initialized;
    public MainWindow() {
        InitializeComponent(); DataContext = model;
        MinimizedSetting.IsChecked = DesktopPreferences.Load().StartMinimized; initialized = true;
        var menu = new Forms.ContextMenuStrip();
        menu.Items.Add("Open Dashboard", null, (_, _) => OpenDashboard());
        pause = (Forms.ToolStripMenuItem)menu.Items.Add("Pause / Resume", null, (_, _) => model.PauseResume.Execute(null));
        check = (Forms.ToolStripMenuItem)menu.Items.Add("Check now", null, (_, _) => model.CheckNow.Execute(null));
        menu.Items.Add("Open Logs", null, (_, _) => model.OpenLogs.Execute(null));
        menu.Items.Add("Exit after current task", null, (_, _) => model.Exit.Execute(null));
        // Generic OS icon until an authorized FOX2 source asset is supplied.
        tray = new Forms.NotifyIcon { Text = "FOX2 Bridge RC1", Icon = System.Drawing.SystemIcons.Application, ContextMenuStrip = menu, Visible = true };
        tray.MouseClick += (_, e) => { if (e.Button == Forms.MouseButtons.Left) OpenDashboard(); };
        timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
        model.GracefulExitComplete += () => { allowClose = true; timer.Stop(); tray.Dispose(); Close(); Application.Current.Shutdown(); };
        timer.Tick += async (_, _) => { await model.Refresh(); check.Enabled = model.CheckNow.CanExecute(null); pause.Text = model.Paused ? "Resume Bridge" : "Pause Bridge"; };
        timer.Start(); _ = model.Refresh();
        Closing += OnClosing;
        StateChanged += (_, _) => { if (WindowState == WindowState.Minimized) Hide(); };
    }
    public void OpenDashboard() { Navigation.SelectedIndex = 0; Show(); WindowState = WindowState.Normal; Activate(); }
    void OnClosing(object? sender, CancelEventArgs e) { if (!allowClose) { e.Cancel = true; Hide(); } }
    async void SaveArtifact(object sender, RoutedEventArgs e) {
        var dialog = new Microsoft.Win32.OpenFileDialog { CheckFileExists = true, Multiselect = false, Title = "Save a local artifact" };
        if (dialog.ShowDialog(this) == true) await model.SaveArtifact(dialog.FileName);
    }
    void BrowseVault(object sender, RoutedEventArgs e) {
        try {
            var root = new ArtifactVaultService().Root;
            BridgeInstallationLocator.RejectLinks(root);
            System.IO.Directory.CreateDirectory(root);
            // Native read-only browsing; selection does not import or execute a file.
            var dialog = new Microsoft.Win32.OpenFileDialog { InitialDirectory = root, CheckFileExists = true,
                Multiselect = false, Title = "Artifact Vault - browse local objects", ShowReadOnly = true, ReadOnlyChecked = true };
            dialog.ShowDialog(this);
        } catch { MessageBox.Show("Local Artifact Vault is unavailable.", "FOX2 Bridge"); }
    }
    void CopyVaultPath(object sender, RoutedEventArgs e) {
        try { Clipboard.SetText(new ArtifactVaultService().Root); }
        catch { MessageBox.Show("Clipboard unavailable.", "FOX2 Bridge"); }
    }
    async void SaveSupport(object sender, RoutedEventArgs e) {
        var dialog = new Microsoft.Win32.SaveFileDialog { Filter = "Support ZIP|*.zip", FileName = "FOX2-Bridge-support.zip", AddExtension = true };
        if (dialog.ShowDialog(this) == true) await model.SaveSupport(dialog.FileName);
    }
    void CopySummary(object sender, RoutedEventArgs e) { try { Clipboard.SetText(model.Diagnostics); } catch { MessageBox.Show("Clipboard unavailable.", "FOX2 Bridge"); } }
    void MinimizedChanged(object sender, RoutedEventArgs e) {
        if (!initialized) return;
        try { new DesktopPreferences(MinimizedSetting.IsChecked == true).Save(); }
        catch { MessageBox.Show("Could not save Desktop preference.", "FOX2 Bridge"); }
    }
}
