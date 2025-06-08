import os
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def title_panel(title, elapsed, completed, total):
    console = Console()
    width = console.width
    
    elapsed_text = f"[bold yellow1]⏱ {elapsed:.2f}s[/bold yellow1]"
    progress_text = f"[bold violet]{completed}/{total} Completed[/bold violet]"
    content = f"[bold orange1]{title}[/bold orange1]    {elapsed_text}    {progress_text}"
    return Align.center(
        Panel(content, border_style="blue1", width=width, expand=True, padding=(0, 0))
    )

def create_progress(console: Console) -> Progress:
    return Progress(
        TextColumn("[bold white]{task.fields[worker]:<15}"),
        TextColumn("[bold green]{task.completed:>5}✅", justify="right"),
        TextColumn("[bold yellow1]{task.fields[elapsed_fmt]:>10} ⏱", justify="right"),
        TextColumn("[bold cyan]🔄 {task.fields[task_desc]:<30}", justify="left"),
        console=console,
        refresh_per_second=2,
    )

def print_summary(console, total_tasks, script_duration, worker_total_time, start_dt, end_dt, min_worker_time, max_worker_time, worker_count):
    def ftime(dt): return dt.strftime("%d.%m.%Y %H:%M:%S")
    def fnum(n): return f"{n:,.2f}"

    console.print("\n")
    console.rule("[bold green]  Task Completion Report ")
    console.print("\n")

    summary = Table.grid(padding=(0, 2))
    summary.add_column("🗂", justify="left", min_width=1, no_wrap=True)
    summary.add_column(justify="left", style="bold", width=10, no_wrap=True)
    summary.add_column(justify="right", width=20)
    summary.add_column("🗂", justify="left", min_width=1, no_wrap=True)
    summary.add_column(justify="left", style="bold", width=15, no_wrap=True)
    summary.add_column(justify="right", width=10)

    summary.add_row("🕒", "Start:", ftime(start_dt),
                    "⚡", "Fastest:", f"{fnum(min_worker_time)}s")
    summary.add_row("🕓", "End:", ftime(end_dt),
                    "🐢", "Slowest:", f"{fnum(max_worker_time)}s")
    summary.add_row("⏳", "Duration:", f"{fnum(script_duration)}s",
                    "📦", "Worker Time:", f"{fnum(worker_total_time)}s")
    summary.add_row("✔", "Tasks:", str(total_tasks),
                    "👥", "Workers:", str(worker_count))
    summary.add_row("", "", "", "", "", "")

    console.print(summary)
    console.print("─" * console.width, style="bold green")
