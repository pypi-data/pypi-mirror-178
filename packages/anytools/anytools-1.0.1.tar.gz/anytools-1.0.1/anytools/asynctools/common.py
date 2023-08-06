import asyncio
import logging
import signal

_protected = set()
_main_task = None


def create_task(coro, *, name=None, protect=False, catch_exceptions=False):
    task = asyncio.create_task(coro, name=name)
    if protect:
        task.add_done_callback(_protected.discard)
        _protected.add(task)
    if catch_exceptions:
        task.add_done_callback(_handle_task_result)
    return task


def _handle_task_result(task):
    try:
        task.result()

    except asyncio.CancelledError as error:
        pass

    except Exception as error:
        logging.error(f"{task._coro.__name__}: {repr(error)}", exc_info=True)


def cancel_weak_tasks():
    tasks = get_all_tasks()
    for task in tasks:
        if task not in _protected:
            task.cancel()
    return tasks


def get_all_tasks():
    tasks = []
    current_task = asyncio.current_task()
    for task in asyncio.all_tasks():
        if task is current_task:
            continue
        if task is _main_task:
            continue
        tasks.append(task)
    return tasks


def add_shutdown_signal_handler(signals=[signal.SIGINT]):
    global _main_task
    _main_task = asyncio.current_task()
    loop = asyncio.get_running_loop()
    for sig in signals:
        loop.add_signal_handler(
            sig,
            lambda signal=sig: asyncio.create_task(
                _shutdown_signal_handler(signal),
            ),
        )


def add_dummy_signal_handler(signals, reason=None):
    loop = asyncio.get_running_loop()
    for sig in signals:
        loop.add_signal_handler(
            sig,
            lambda signal=sig: asyncio.create_task(
                _dummy_signal_handler(signal, reason),
            ),
        )


async def _shutdown_signal_handler(sig):
    signal_name = sig.name
    logging.info(f"Received: {signal_name}, shutdowning...")
    add_dummy_signal_handler([sig], reason="shutdown")
    tasks = cancel_weak_tasks()
    await asyncio.gather(*tasks, return_exceptions=True)
    logging.info(f"Shotdown has been finished.")


async def _dummy_signal_handler(sig, reason=None):
    signal_name = sig.name
    logging.info(f"Received: {signal_name}, ignoring... [{reason}]")
