using System.ComponentModel;
using System.Windows;
using System.Windows.Input;
using FOX2.Bridge.Desktop.ViewModels;

namespace FOX2.Bridge.Desktop;

public partial class MainWindow : Window
{
    public bool AllowRealClose { get; set; }

    public MainWindow()
    {
        InitializeComponent();
    }

    private void Header_OnMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        if (e.ClickCount == 2)
        {
            ToggleMaximize();
            return;
        }

        if (e.ButtonState == MouseButtonState.Pressed)
            DragMove();
    }

    private void Minimize_OnClick(object sender, RoutedEventArgs e) =>
        WindowState = WindowState.Minimized;

    private void Maximize_OnClick(object sender, RoutedEventArgs e) =>
        ToggleMaximize();

    private void ToggleMaximize() =>
        WindowState = WindowState == WindowState.Maximized
            ? WindowState.Normal
            : WindowState.Maximized;

    private void Close_OnClick(object sender, RoutedEventArgs e) => Close();

    protected override void OnClosing(CancelEventArgs e)
    {
        if (!AllowRealClose &&
            DataContext is MainViewModel viewModel &&
            viewModel.Settings.CloseToTray)
        {
            e.Cancel = true;
            Hide();
            return;
        }

        base.OnClosing(e);
    }
}
