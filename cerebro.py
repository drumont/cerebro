
import psutil
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("cerebro")


@mcp.tool()
def get_all_processes() -> list[dict]:
    """ This tool gets all processes running on the host
    :return:
        list of dictionaries containing all processes running on the host
        dictionary keys: pid, name, username, status, memory_info, cpu_times
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'memory_info', 'cpu_times']):
        try:
            proc_info = proc.info
            proc_info['memory_info'] = proc.memory_percent() * 100
            proc_info['cpu_times'] = proc.cpu_percent() * 100
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

@mcp.tool()
def kill_process(pid: int) -> str:
    """ This tool kills a process by its PID
    :param pid: Process ID
    :return: Success or failure message
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return f"Process {pid} terminated successfully."
    except psutil.NoSuchProcess:
        return f"Process {pid} does not exist."
    except psutil.AccessDenied:
        return f"Access denied to terminate process {pid}."
    except psutil.TimeoutExpired:
        return f"Timeout expired while terminating process {pid}."


if __name__ == "__main__":
    mcp.run(transport="stdio")