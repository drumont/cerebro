import os

import psutil
from mcp.server.fastmcp import FastMCP

port = os.getenv("CEREBRO_PORT", 8000)

mcp = FastMCP(
    name="cerebro",
    host="0.0.0.0",
    port=port)


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
def kill_process(pid: int) -> dict:
    """ This tool kills a process by its PID
    :param pid: Process ID
    :return: Dictionary with status and message
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return {"status": "success", "message": f"Process {pid} terminated."}
    except psutil.NoSuchProcess:
        return {"status": "failure", "message": f"Process {pid} does not exist."}
    except psutil.AccessDenied:
        return {"status": "failure", "message": f"Access denied to terminate process {pid}."}
    except psutil.TimeoutExpired:
        return {"status": "failure", "message": f"Timeout expired while terminating process {pid}."}

def run():
    mcp.run(
        transport="streamable-http"
    )

def main():
    run()

if __name__ == "__main__":
    main()