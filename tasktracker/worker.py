import threading
import time
from tasktracker.logger import logger

class Worker(threading.Thread):
    def __init__(self, name, action_func, task_q, stat_q):
        super().__init__(daemon=True)
        self.name = name
        self.action = action_func
        self.task_q = task_q
        self.stat_q = stat_q
        self.stop = False

    def run(self):
        logger.info(f"[{self.name}] started.")
        while not self.stop:
            try:
                task = self.task_q.get(timeout=0.5)
            except:
                continue

            logger.info(f"[{self.name}] picked task '{task.name}'")
            start = time.time()
            self.stat_q.put({
                "worker": self.name,
                "status": "started",
                "name": task.name,
                "desc": task.desc,
            })

            logger.info(f"[{self.name}] started task '{task.name}'")

            try:
                result = self.action(task.data)
                status = "success" if result else "failed"
            except Exception as e:
                status = "exception"
                logger.exception(f"[{self.name}] exception on task '{task.name}': {e}")

            duration = round(time.time() - start, 2)
            self.stat_q.put({
                "worker": self.name,
                "status": status,
                "duration": duration
            })

            if status == "success":
                logger.info(f"[{self.name}] completed task '{task.name}' in {duration:.2f}s")
            elif status == "failed":
                logger.warning(f"[{self.name}] failed task '{task.name}' in {duration:.2f}s")

            self.task_q.task_done()
