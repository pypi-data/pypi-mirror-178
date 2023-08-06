import traceback
from typing import Union

import pynvml


def gpu_measure() -> Union[dict, None]:
    try:
        pynvml.nvmlInit()
        metrics = {"gpu": []}
        deviceCount = pynvml.nvmlDeviceGetCount()
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            power = pynvml.nvmlDeviceGetPowerUsage(handle)
            utilitization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            try:
                name = name.decode("utf-8")
            except Exception as e:
                pass
            metrics["gpu"].append(
                {
                    "product_name": name,
                    "fb_memory_usage": {
                        "total": mem.total / 1024 / 1024,
                        "used": mem.used / 1024 / 1024,
                        "free": mem.free / 1024 / 1024,
                    },
                    "utilization": utilitization.gpu,
                    "power_readings": {"power_draw": power / 1000},
                }
            )
    except pynvml.NVMLError as error:
        traceback.print_exc()
        print(error)
        metrics = None
    finally:
        pynvml.nvmlShutdown()
        return metrics
