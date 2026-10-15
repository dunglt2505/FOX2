using System.Diagnostics;
using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.Services;

public sealed class BridgeControlClient(BridgeRuntimeLocator locator) : IBridgeControlClient
{
    private static readonly TimeSpan DefaultTimeout = TimeSpan.FromSeconds(12);

    public string BridgeRoot => locator.BridgeRoot;

    public async Task<BridgeStatusSnapshot> GetStatusAsync(CancellationToken cancellationToken = default)
    {
        var json = await InvokeJsonAsync(
            ["-m", "fox2_agent_bridge", "control", "status"],
            DefaultTimeout,
            cancellationToken);

        return BridgeJsonParser.ParseWorkerStatus(json);
    }

    public Task PauseAsync(CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(["-m", "fox2_agent_bridge", "control", "pause"], cancellationToken);

    public Task ResumeAsync(CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(["-m", "fox2_agent_bridge", "control", "resume"], cancellationToken);

    public Task CheckNowAsync(CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(["-m", "fox2_agent_bridge", "control", "check-now"], cancellationToken);

    public Task RequestExitAsync(CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(["-m", "fox2_agent_bridge", "control", "request-exit"], cancellationToken);

    public Task OpenLogsAsync(CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(["-m", "fox2_agent_bridge", "control", "open-logs"], cancellationToken);

    public Task SetStartWithWindowsAsync(bool enabled, CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(
            [
                "-m", "fox2_agent_bridge", "control", "set-start-with-windows",
                "--enabled", enabled ? "true" : "false"
            ],
            cancellationToken);

    public Task SaveSupportBundleAsync(string destination, CancellationToken cancellationToken = default) =>
        InvokeDiscardAsync(
            ["-m", "fox2_agent_bridge", "diagnostics", "--output", destination],
            cancellationToken,
            TimeSpan.FromSeconds(45));

    private async Task InvokeDiscardAsync(
        IReadOnlyList<string> arguments,
        CancellationToken cancellationToken,
        TimeSpan? timeout = null)
    {
        _ = await InvokeJsonAsync(arguments, timeout ?? DefaultTimeout, cancellationToken);
    }

    private async Task<string> InvokeJsonAsync(
        IReadOnlyList<string> arguments,
        TimeSpan timeout,
        CancellationToken cancellationToken)
    {
        var python = locator.ResolvePythonPath();
        var startInfo = new ProcessStartInfo(python)
        {
            UseShellExecute = false,
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            WorkingDirectory = locator.BridgeRoot
        };

        foreach (var argument in arguments)
            startInfo.ArgumentList.Add(argument);

        using var process = new Process { StartInfo = startInfo };
        if (!process.Start())
            throw new InvalidOperationException("FOX2 Bridge control process could not start.");

        var stdoutTask = process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderrTask = process.StandardError.ReadToEndAsync(cancellationToken);

        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeoutCts.CancelAfter(timeout);

        try
        {
            await process.WaitForExitAsync(timeoutCts.Token);
        }
        catch (OperationCanceledException) when (!cancellationToken.IsCancellationRequested)
        {
            try { process.Kill(entireProcessTree: true); } catch { }
            throw new TimeoutException("FOX2 Bridge control timed out.");
        }

        var stdout = await stdoutTask;
        var stderr = await stderrTask;

        if (process.ExitCode != 0)
            throw new InvalidOperationException(
                string.IsNullOrWhiteSpace(stderr)
                    ? "FOX2 Bridge control failed."
                    : $"FOX2 Bridge control failed: {Bound(stderr)}");

        return stdout;
    }

    private static string Bound(string value)
    {
        var text = value.ReplaceLineEndings(" ").Trim();
        return text.Length <= 300 ? text : text[..300];
    }
}
