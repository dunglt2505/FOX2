using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace FOX2.Bridge.Desktop.Services;

public sealed record ArtifactRecord(string ArtifactId, string FileName, string Sha256, long SizeBytes,
    DateTimeOffset SavedAtUtc, string State, string VaultPath);

public sealed class ArtifactVaultService
{
    public const long MaximumBytes = 100 * 1024 * 1024;
    public string Root { get; }
    public ArtifactVaultService() : this(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "FOX2", "BridgeDesktop", "Artifacts")) { }
    internal ArtifactVaultService(string root) { Root = Path.GetFullPath(root); }
    static void Guard(string path) => BridgeInstallationLocator.RejectLinks(path);
    public IReadOnlyList<ArtifactRecord> List()
    {
        Guard(Root);
        var index = Path.Combine(Root, "index.json"); Guard(index);
        if (!File.Exists(index)) return Array.Empty<ArtifactRecord>();
        if (new FileInfo(index).Length > 5_000_000) throw new IOException("Artifact index exceeds bound.");
        var rows = JsonSerializer.Deserialize<List<ArtifactRecord>>(File.ReadAllText(index)) ?? new();
        if (rows.Any(row => row.State != "LOCAL_SAVED" || !Regex.IsMatch(row.Sha256, "^[0-9a-f]{64}$") ||
            row.ArtifactId != "sha256:" + row.Sha256 || row.SizeBytes < 0 || row.SizeBytes > MaximumBytes ||
            Path.GetFileName(row.FileName) != row.FileName || row.VaultPath != Path.Combine("objects", row.Sha256, row.FileName)))
            throw new IOException("Invalid artifact index.");
        return rows;
    }
    public ArtifactRecord Save(string selectedFile)
    {
        if (!Path.IsPathFullyQualified(selectedFile) || selectedFile.StartsWith(@"\\")) throw new IOException("Choose a local file.");
        var source = Path.GetFullPath(selectedFile); Guard(source); Guard(Root);
        using var input = new FileStream(source, FileMode.Open, FileAccess.Read, FileShare.Read);
        if (input.Length > MaximumBytes) throw new IOException("File exceeds 100 MiB.");
        var size = input.Length;
        var sha = Convert.ToHexString(SHA256.HashData(input)).ToLowerInvariant(); input.Position = 0;
        var name = Regex.Replace(Path.GetFileName(source), "[^A-Za-z0-9._-]", "_");
        if (string.IsNullOrWhiteSpace(name) || name.Trim('.') == "") name = "artifact";
        name = "file_" + name[..Math.Min(name.Length, 160)];
        Directory.CreateDirectory(Root); Guard(Root);
        var lockPath = Path.Combine(Root, ".vault.lock"); Guard(lockPath);
        using var gate = new FileStream(lockPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None);
        var rows = List().ToList();
        var directory = Path.Combine(Root, "objects", sha); Guard(directory); Directory.CreateDirectory(directory); Guard(directory);
        var destination = Path.Combine(directory, name); Guard(destination);
        var temporary = Path.Combine(directory, ".copy-" + Guid.NewGuid().ToString("N"));
        try {
            using (var copy = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None)) { input.CopyTo(copy); copy.Flush(true); }
            using (var copy = File.OpenRead(temporary))
                if (copy.Length != size || Convert.ToHexString(SHA256.HashData(copy)).ToLowerInvariant() != sha) throw new IOException("Artifact verification failed.");
            if (File.Exists(destination)) {
                using var existing = File.OpenRead(destination);
                if (Convert.ToHexString(SHA256.HashData(existing)).ToLowerInvariant() != sha) throw new IOException("Existing object failed verification.");
            } else File.Move(temporary, destination);
            var record = new ArtifactRecord("sha256:" + sha, name, sha, size, DateTimeOffset.UtcNow, "LOCAL_SAVED", Path.Combine("objects", sha, name));
            rows.RemoveAll(row => row.ArtifactId == record.ArtifactId); rows.Add(record);
            if (rows.Count > 10000) throw new IOException("Artifact count exceeds bound.");
            var index = Path.Combine(Root, "index.json"); Guard(index);
            var pending = Path.Combine(Root, ".index-" + Guid.NewGuid().ToString("N"));
            try {
                var raw = JsonSerializer.SerializeToUtf8Bytes(rows, new JsonSerializerOptions { WriteIndented = true });
                if (raw.Length > 5_000_000) throw new IOException("Artifact index exceeds bound.");
                using (var stream = new FileStream(pending, FileMode.CreateNew, FileAccess.Write, FileShare.None)) { stream.Write(raw); stream.Flush(true); }
                File.Move(pending, index, overwrite: true);
            } finally { if (File.Exists(pending)) File.Delete(pending); }
            return record;
        } finally { if (File.Exists(temporary)) File.Delete(temporary); }
    }
}
