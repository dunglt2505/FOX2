using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace FOX2.Bridge.Desktop.Services;

public sealed class BridgeInstallationLocator
{
    public static string Root => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "FOX2", "AgentBridge");
    public static void RejectLinks(string path)
    {
        for (var item = new DirectoryInfo(Path.GetFullPath(path)); item != null; item = item.Parent)
            if (item.Exists && (item.Attributes & FileAttributes.ReparsePoint) != 0)
                throw new IOException("Linked paths are not supported.");
        if (File.Exists(path) && (File.GetAttributes(path) & FileAttributes.ReparsePoint) != 0)
            throw new IOException("Linked files are not supported.");
    }
    public (string Python, string Package, string Source) Locate()
    {
        var pointer = Path.Combine(Root, "current.json");
        RejectLinks(pointer);
        using var document = JsonDocument.Parse(File.ReadAllText(pointer));
        var hash = document.RootElement.GetProperty("package_sha256").GetString() ?? "";
        if (!Regex.IsMatch(hash, "^[0-9a-f]{64}$")) throw new IOException("Invalid installed package pointer.");
        var python = Path.Combine(Root, "versions", hash, "runtime", "Scripts", "python.exe");
        RejectLinks(python);
        if (!File.Exists(python)) throw new IOException("Installed runtime is unavailable.");
        return (python, hash, document.RootElement.TryGetProperty("source_sha256", out var source) ? source.GetString() ?? "Not provided" : "Not provided");
    }
}

public enum ControlAction { Status, Pause, Resume, CheckNow, RequestExit, OpenLogs, SetStartWithWindows }

public sealed class BridgeControlClient
{
    readonly BridgeInstallationLocator locator = new();
    public static string[] Arguments(ControlAction action, bool? enabled = null)
    {
        var command = action switch {
            ControlAction.Status => "status", ControlAction.Pause => "pause", ControlAction.Resume => "resume",
            ControlAction.CheckNow => "check-now", ControlAction.RequestExit => "request-exit",
            ControlAction.OpenLogs => "open-logs", ControlAction.SetStartWithWindows => "set-start-with-windows",
            _ => throw new ArgumentOutOfRangeException(nameof(action)) };
        if (action == ControlAction.SetStartWithWindows && enabled == null) throw new ArgumentException("Explicit startup choice required.");
        return new[] { "-I", "-m", "fox2_agent_bridge", "control", command }.Concat(
            action == ControlAction.SetStartWithWindows ? new[] { "--enabled", enabled == true ? "true" : "false" } : Array.Empty<string>()).ToArray();
    }
    public Task<JsonElement> InvokeAsync(ControlAction action, bool? enabled = null) => RunAsync(Arguments(action, enabled));
    public Task<JsonElement> DiagnosticsAsync(string output)
    {
        if (!Path.IsPathFullyQualified(output) || Path.GetExtension(output) != ".zip" || output.StartsWith(@"\\"))
            throw new ArgumentException("Choose a local support ZIP file.");
        var full = Path.GetFullPath(output);
        BridgeInstallationLocator.RejectLinks(full);
        var local = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        foreach (var protectedRoot in new[] { BridgeInstallationLocator.Root, Path.Combine(local, "FOX2", "BridgeDesktop", "Artifacts") })
            if (full.StartsWith(protectedRoot + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
                throw new ArgumentException("Choose a support destination outside product data.");
        return RunAsync(new[] { "-I", "-m", "fox2_agent_bridge", "diagnostics", "--output", full });
    }
    async Task<JsonElement> RunAsync(string[] arguments)
    {
        try { return await RunProcessAsync(locator.Locate().Python, arguments, TimeSpan.FromSeconds(15)); }
        catch { throw new IOException("Bridge control unavailable. Check the installed runtime and Diagnostics."); }
    }
    // Shared bounded runner; the UI's only caller supplies fixed arguments above.
    internal static async Task<JsonElement> RunProcessAsync(string executable, string[] arguments, TimeSpan timeout)
    {
        var info = new ProcessStartInfo(executable) { UseShellExecute = false, CreateNoWindow = true,
            RedirectStandardOutput = true, RedirectStandardError = true, WorkingDirectory = BridgeInstallationLocator.Root };
        foreach (var argument in arguments) info.ArgumentList.Add(argument);
        foreach (var key in info.Environment.Keys.ToArray())
            if (key.Equals("PYTHONPATH", StringComparison.OrdinalIgnoreCase) || key.Equals("PYTHONHOME", StringComparison.OrdinalIgnoreCase)) info.Environment.Remove(key);
        using var process = Process.Start(info) ?? throw new IOException("Control unavailable.");
        using var bound = new CancellationTokenSource(timeout);
        var stdout = DrainAsync(process.StandardOutput, bound.Token);
        var stderr = DrainAsync(process.StandardError, bound.Token);
        try {
            await Task.WhenAll(process.WaitForExitAsync(bound.Token), stdout, stderr);
            if (process.ExitCode != 0) throw new IOException("Control failed.");
            using var document = JsonDocument.Parse(await stdout);
            return document.RootElement.Clone();
        } catch {
            if (!process.HasExited) { process.Kill(entireProcessTree: true); await process.WaitForExitAsync(); }
            try { await Task.WhenAll(stdout, stderr); } catch { }
            throw;
        }
    }
    static async Task<string> DrainAsync(StreamReader stream, CancellationToken token)
    {
        var buffer = new char[4096]; var text = new System.Text.StringBuilder();
        int count;
        while ((count = await stream.ReadAsync(buffer.AsMemory(), token)) != 0) {
            if (text.Length + count > 1_048_576) throw new IOException("Control response exceeds bound.");
            text.Append(buffer, 0, count);
        }
        return text.ToString();
    }
}
