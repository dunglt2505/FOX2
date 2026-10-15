using System.Collections.ObjectModel;
using FOX2.Bridge.Desktop.Infrastructure;
using FOX2.Bridge.Desktop.Models;

namespace FOX2.Bridge.Desktop.ViewModels;

public sealed class ActivityViewModel : ObservableObject
{
    public ObservableCollection<ActivityItem> Items { get; } = [];

    public void Add(string type, string message, string status)
    {
        Items.Insert(0, new ActivityItem(DateTimeOffset.Now, type, message, status));
        while (Items.Count > 100)
            Items.RemoveAt(Items.Count - 1);
    }
}
