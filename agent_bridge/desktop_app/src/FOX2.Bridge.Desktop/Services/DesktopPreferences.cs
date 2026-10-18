using System;
using System.IO;
using System.Text.Json;
namespace FOX2.Bridge.Desktop.Services;
public sealed record DesktopPreferences(bool StartMinimized = false)
{
    static string PathName => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "FOX2", "BridgeDesktop", "settings.json");
    public static DesktopPreferences Load() { try { BridgeInstallationLocator.RejectLinks(PathName); return JsonSerializer.Deserialize<DesktopPreferences>(File.ReadAllText(PathName)) ?? new(); } catch { return new(); } }
    public void Save() {
        BridgeInstallationLocator.RejectLinks(PathName); Directory.CreateDirectory(Path.GetDirectoryName(PathName)!);
        var pending = PathName + "." + Guid.NewGuid().ToString("N");
        try { File.WriteAllText(pending, JsonSerializer.Serialize(this)); File.Move(pending, PathName, true); }
        finally { if (File.Exists(pending)) File.Delete(pending); }
    }
}
