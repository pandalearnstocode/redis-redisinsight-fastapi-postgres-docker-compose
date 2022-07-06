import time

def optimization(iteration: int, run_time:str) -> dict:
    dummy_result = {"iteration": iteration, "run_time": run_time}
    return dummy_result

def _optimization_result(payload: dict) -> dict:
    """This is a dummy function which will call optimization from ml library.

    Args:
        payload (dict): optimization arguments.

    Returns:
        dict: optimization result.
    """
    time.sleep(10)
    return optimization(**payload)