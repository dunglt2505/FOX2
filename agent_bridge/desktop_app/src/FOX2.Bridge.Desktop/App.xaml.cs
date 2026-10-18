using System;
using System.Security.Principal;
using System.Threading;
using System.Windows;
using System.IO;

namespace FOX2.Bridge.Desktop;
public partial class App : Application
{
    Mutex? singleton; EventWaitHandle? showEvent; RegisteredWaitHandle? listener; FileStream? presentationLock;
    protected override void OnStartup(StartupEventArgs e) {
        base.OnStartup(e);
        var sid = WindowsIdentity.GetCurrent().User!.Value;
        singleton = new Mutex(true, @"Local\FOX2BridgeDesktop-" + sid, out var first);
        showEvent = new EventWaitHandle(false, EventResetMode.AutoReset, @"Local\FOX2BridgeDesktopShow-" + sid);
        if (!first) { showEvent.Set(); Shutdown(); return; }
        var lockPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "FOX2", "BridgeDesktop", "desktop.lock");
        try {
            Services.BridgeInstallationLocator.RejectLinks(lockPath);
            Directory.CreateDirectory(Path.GetDirectoryName(lockPath)!);
            presentationLock = new FileStream(lockPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None);
        } catch { MessageBox.Show("Desktop is unavailable during installation maintenance. The Worker continues independently.", "FOX2 Bridge"); Shutdown(); return; }
        var window = new MainWindow(); MainWindow = window;
        listener = ThreadPool.RegisterWaitForSingleObject(showEvent, (_, _) => Dispatcher.BeginInvoke(window.OpenDashboard), null, -1, false);
        DispatcherUnhandledException += (_, args) => { args.Handled = true; MessageBox.Show("Desktop needs attention. The Worker continues independently.", "FOX2 Bridge"); };
        if (Array.IndexOf(e.Args, "--minimized") < 0 && !Services.DesktopPreferences.Load().StartMinimized) window.Show();
    }
    protected override void OnExit(ExitEventArgs e) { listener?.Unregister(null); presentationLock?.Dispose(); showEvent?.Dispose(); singleton?.Dispose(); base.OnExit(e); }
}
