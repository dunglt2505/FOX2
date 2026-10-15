using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.Services;

public interface IBridgeControlClient
{
    string BridgeRoot { get; }

    Task<BridgeStatusSnapshot> GetStatusAsync(CancellationToken cancellationToken = default);
    Task PauseAsync(CancellationToken cancellationToken = default);
    Task ResumeAsync(CancellationToken cancellationToken = default);
    Task CheckNowAsync(CancellationToken cancellationToken = default);
    Task RequestExitAsync(CancellationToken cancellationToken = default);
    Task OpenLogsAsync(CancellationToken cancellationToken = default);
    Task SetStartWithWindowsAsync(bool enabled, CancellationToken cancellationToken = default);
    Task SaveSupportBundleAsync(string destination, CancellationToken cancellationToken = default);
}
