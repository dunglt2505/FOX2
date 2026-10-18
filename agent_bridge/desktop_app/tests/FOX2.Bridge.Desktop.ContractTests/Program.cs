using System.Diagnostics;
using System.Security.Cryptography;
using System.Text.Json;
using FOX2.Bridge.Desktop.Services;
using FOX2.Bridge.Desktop.ViewModels;

int passed = 0;
void Check(bool condition, string label) { if (!condition) throw new Exception(label); passed++; Console.WriteLine("PASS " + label); }
void Reject(Action action, string label) { try { action(); } catch { Check(true, label); return; } throw new Exception(label); }
var root = Path.Combine(Path.GetTempPath(), "fox2-vault-test-" + Guid.NewGuid().ToString("N")); Directory.CreateDirectory(root);
try {
    var vault = new ArtifactVaultService(Path.Combine(root, "vault"));
    var source = Path.Combine(root, "résumé.txt"); var bytes = RandomNumberGenerator.GetBytes(32771); File.WriteAllBytes(source, bytes);
    var saved = vault.Save(source);
    Check(saved.Sha256 == Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant(), "source SHA256");
    Check(File.ReadAllBytes(Path.Combine(vault.Root, saved.VaultPath)).SequenceEqual(bytes), "verified content-addressed object");
    Check(vault.List().Single().State == "LOCAL_SAVED", "LOCAL_SAVED only");
    vault.Save(source); Check(vault.List().Count == 1, "duplicate content index idempotence");
    Check(!Directory.GetFiles(vault.Root, ".index-*").Any(), "atomic index temporary cleaned");
    Check(!Directory.GetFiles(Path.Combine(vault.Root, "objects", saved.Sha256), ".copy-*").Any(), "copy temporary cleaned");
    var before = File.ReadAllBytes(Path.Combine(vault.Root, "index.json"));
    File.WriteAllText(Path.Combine(vault.Root, saved.VaultPath), "corrupt");
    Reject(() => vault.Save(source), "corrupt existing object rejected");
    Check(before.SequenceEqual(File.ReadAllBytes(Path.Combine(vault.Root, "index.json"))), "failed verification preserves index");
    var huge = Path.Combine(root, "large"); using (var stream = File.Create(huge)) stream.SetLength(ArtifactVaultService.MaximumBytes + 1);
    Reject(() => vault.Save(huge), "size bound");
    Reject(() => vault.Save("relative.txt"), "relative selection rejected");
    Reject(() => vault.Save(@"\\server\file"), "network selection rejected");
    using (var gate = new FileStream(Path.Combine(vault.Root, ".vault.lock"), FileMode.Open, FileAccess.ReadWrite, FileShare.None))
        Reject(() => vault.Save(source), "concurrent index writer rejected");
    var broken = new ArtifactVaultService(Path.Combine(root, "broken")); Directory.CreateDirectory(broken.Root);
    File.WriteAllText(Path.Combine(broken.Root, "index.json"), "invalid");
    Reject(() => broken.Save(source), "malformed index preserved");
    File.WriteAllText(Path.Combine(broken.Root, "index.json"), JsonSerializer.Serialize(new[] { saved with { State = "RELEASED" } }));
    Reject(() => broken.List(), "release state rejected");
    foreach (var action in Enum.GetValues<ControlAction>()) {
        var commandArguments = BridgeControlClient.Arguments(action, true);
        Check(commandArguments.Take(4).SequenceEqual(new[] { "-I", "-m", "fox2_agent_bridge", "control" }), "fixed argument boundary " + action);
    }
    Reject(() => BridgeControlClient.Arguments((ControlAction)999), "unknown control rejected");
    Reject(() => BridgeControlClient.Arguments(ControlAction.SetStartWithWindows), "startup explicit choice");
    Check(MainViewModel.Label("PAUSED") == "Paused" && MainViewModel.Label("bogus") == "Unknown", "state mapping");
    using var unverified = JsonDocument.Parse("{\"tool_name\":\"copilot\",\"available\":true,\"auth_status\":\"UNVERIFIED\",\"version\":null}");
    Check(MainViewModel.ToolLabel(unverified.RootElement).Contains("Available / auth unverified"), "Copilot auth unverified");
    Check(MainViewModel.ToolLabel(unverified.RootElement).Contains("Not provided by CLI"), "no invented CLI version");
    var viewModel = new MainViewModel();
    using var pausedState = JsonDocument.Parse("{\"state\":\"PAUSED\",\"paused\":true}");
    typeof(MainViewModel).GetField("status", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)!.SetValue(viewModel, pausedState.RootElement.Clone());
    Check(viewModel.Polling == "Polling: Paused" && !viewModel.CheckNow.CanExecute(null), "paused UI never bypasses polling");
    var python = Environment.GetEnvironmentVariable("FOX2_TEST_PYTHON") ?? throw new Exception("test Python required");
    var pipe = await BridgeControlClient.RunProcessAsync(python, new[] { "-I", "-c", "import sys,json,os; sys.stderr.write('x'*200000); print(json.dumps({'ok':True,'clean':not any(k.upper() in ('PYTHONPATH','PYTHONHOME') for k in os.environ)}))" }, TimeSpan.FromSeconds(5));
    Check(pipe.GetProperty("ok").GetBoolean() && pipe.GetProperty("clean").GetBoolean(), "concurrent pipes and hermetic environment");
    var watch = Stopwatch.StartNew();
    try { await BridgeControlClient.RunProcessAsync(python, new[] { "-I", "-c", "import time; time.sleep(60)" }, TimeSpan.FromMilliseconds(300)); throw new Exception("timeout missing"); }
    catch (OperationCanceledException) { Check(watch.Elapsed.TotalSeconds < 5, "bounded process timeout"); }
    try { await BridgeControlClient.RunProcessAsync(python, new[] { "-I", "-c", "import sys; sys.stderr.write('private-value'); sys.exit(7)" }, TimeSpan.FromSeconds(5)); throw new Exception("failure missing"); }
    catch (IOException error) { Check(!error.Message.Contains("private-value"), "sanitized process failure"); }
    Console.WriteLine(JsonSerializer.Serialize(new { passed, failed = 0 }));
} finally { Directory.Delete(root, true); }
