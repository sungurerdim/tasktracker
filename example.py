from tasktracker.task import Task
from tasktracker.runner import run
from tasktracker.logger import logger
import time, random

def my_action(file_path):
    logger.info(f"Processing file: {file_path}")
    time.sleep(random.uniform(3.70, 5.65))
    return True

if __name__ == "__main__":
    tasks = [
        Task(data="input/first_file_to_process.txt", name="File A", desc="Convert A to X"),
        Task("input/second_file_to_process.txt"),
        Task("input/third_file_to_process.txt", "File C", "Convert C to Z", ),
    ]

    run(
        title="Demo Process",
        action=my_action,
        tasks=tasks,
        worker_count=2
    )