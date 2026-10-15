using System.Text.Json;

namespace FOX2.Bridge.Desktop.Services;

public sealed class BridgeRuntimeLocator
{
    private readonly string _localAppData;

    public BridgeRuntimeLocator(string? localAppData = null)
    {
        _localAppData = localAppData
            ?? Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
    }

    public string BridgeRoot =>
        Path.Combine(_localAppData, "FOX2", "AgentBridge");

    public string ResolvePythonPath()
    {
        var current = Path.Combine(BridgeRoot, "current.json");
        if (!File.Exists(current))
            throw new FileNotFoundException("FOX2 Bridge current.json is missing.", current);

        using var document = JsonDocument.Parse(File.ReadAllText(current));
        if (!document.RootElement.TryGetProperty("package_sha256", out var packageElement))
            throw new InvalidDataException("FOX2 Bridge current.json has no package_sha256.");

        var packageSha = packageElement.GetString();
        if (string.IsNullOrWhiteSpace(packageSha))
            throw new InvalidDataException("FOX2 Bridge package_sha256 is empty.");

        var python = Path.Combine(
            BridgeRoot,
            "versions",
            packageSha,
            "runtime",
            "Scripts",
            "python.exe");

        if (!File.Exists(python))
            throw new FileNotFoundException("Installed FOX2 Bridge Python is missing.", python);

        return python;
    }
}
