using System.IO;
using System.Text.Json;

namespace FOX2.Bridge.Desktop.Services;

public sealed record UiSettings(bool CloseToTray = true, bool Notifications = true);

public sealed class AppSettingsService
{
    private readonly string _path;

    public AppSettingsService(string? localAppData = null)
    {
        var root = Path.Combine(
            localAppData ?? Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "FOX2",
            "BridgeDesktop");

        _path = Path.Combine(root, "settings.json");
    }

    public UiSettings Load()
    {
        try
        {
            if (!File.Exists(_path))
                return new UiSettings();

            return JsonSerializer.Deserialize<UiSettings>(File.ReadAllText(_path))
                   ?? new UiSettings();
        }
        catch
        {
            return new UiSettings();
        }
    }

    public void Save(UiSettings settings)
    {
        var directory = Path.GetDirectoryName(_path)!;
        Directory.CreateDirectory(directory);

        var json = JsonSerializer.Serialize(
            settings,
            new JsonSerializerOptions { WriteIndented = true });

        File.WriteAllText(_path, json + Environment.NewLine);
    }
}
