import time
from queue import Queue
from datetime import datetime
from rich.console import Console, Group
from rich.live import Live
from .worker import Worker
from .display import clear_screen, create_progress, title_panel, print_summary
from tasktracker.logger import logger

def run(title: str, action, tasks, worker_count: int = 2):
    clear_screen()

    logger.info(f"TaskTracker started with {len(tasks)} tasks, {worker_count} workers.")

    task_q = Queue()
    stat_q = Queue()
    all_elapsed = []
    worker_stats = {}
    completed_flags = {}
    worker_start_times = {}
    console = Console()

    for task in tasks:
        task_q.put(task)

    progress = create_progress(console)
    start_time = time.time()
    start_dt = datetime.now()

    worker_count = min(worker_count, len(tasks))
    worker_names = [f"Worker-{i+1}" for i in range(worker_count)]
    task_ids = {}

    with Live(console=console, refresh_per_second=1) as live:
        for name in worker_names:
            task_id = progress.add_task("",
                total=None,
                worker=name,
                task_name="",
                task_desc="",
                elapsed_fmt="0.00"
            )
            task_ids[name] = task_id
            worker_stats[name] = []
            completed_flags[name] = False

        workers = [Worker(name, action, task_q, stat_q) for name in worker_names]
        for w in workers:
            w.start()

        completed = 0
        total_tasks = len(tasks)

        while completed < total_tasks:
            elapsed = time.time() - start_time

            for name in worker_names:
                task_id = task_ids[name]
                task = progress.tasks[task_id]

                if not completed_flags[name]:
                    current = time.time() - worker_start_times.get(name, time.time())
                    total = sum(worker_stats[name]) + current
                    progress.update(task_id, elapsed_fmt=f"{total:.2f}s")
            
            live.update(Group(
                title_panel(title, elapsed, completed, total_tasks),
                progress
            ))

            try:
                msg = stat_q.get(timeout=0.2)
            except:
                continue

            name = msg["worker"]
            status = msg["status"]
            dur = msg.get("duration", 0)
            desc = msg.get("desc", "")
            taskname = msg.get("name", "")

            task_id = task_ids[name]
            task = progress.tasks[task_id]

            if status == "started":
                worker_start_times[name] = time.time()
                progress.update(task_id,
                    task_name=taskname[:16],
                    task_desc=(desc[:37] + "...") if len(desc) > 40 else desc)

            if status in {"success", "failed", "exception"}:
                completed += 1
                worker_stats[name].append(dur)
                all_elapsed.append(dur)
                completed_flags[name] = True

                progress.update(task_id, advance=1)
                total = sum(worker_stats[name])
                progress.update(task_id, elapsed_fmt=f"{total:.2f}s")

        for w in workers:
            w.stop = True
            w.join()

        script_duration = time.time() - start_time

        logger.info(f"All tasks completed in {script_duration:.2f} seconds.")

        live.update(Group(
            title_panel(title, script_duration, completed, total_tasks),
            progress
        ))
        time.sleep(0.5)

    worker_total_time = sum(all_elapsed)
    per_worker_totals = [sum(worker_stats[w]) for w in worker_names if worker_stats[w]]
    min_time = min(per_worker_totals) if per_worker_totals else 0
    max_time = max(per_worker_totals) if per_worker_totals else 0

    print_summary(console,
        total_tasks=total_tasks,
        script_duration=script_duration,
        worker_total_time=worker_total_time,
        start_dt=start_dt,
        end_dt=datetime.now(),
        min_worker_time=min_time,
        max_worker_time=max_time,
        worker_count=len(worker_stats)
    )
