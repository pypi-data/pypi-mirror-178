from tomclient.client import TOMClient
from tomclient.gpuml.gpu_profiler import gpu_measure
from tomclient.states.globals import shared_states


def clock_update_status(tom_client, gpu_id):
    global shared_states
    shared_states["gpu_stats"] = gpu_measure()
    if shared_states["gpu_stats"] is not None and "gpu" in shared_states["gpu_stats"]:
        stat = shared_states["gpu_stats"]["gpu"][int(gpu_id)]
        gpu_util = stat["utilization"]
        power_usage = stat["power_readings"]["power_draw"]
        available_memory = stat["fb_memory_usage"]["free"]
        used_memory = stat["fb_memory_usage"]["used"]
        tom_client.update_status(metric="Available Memory", value=available_memory)
        tom_client.update_status(metric="Used Memory", value=used_memory)
        tom_client.update_status(metric="GPU Utilization", value=gpu_util)
        tom_client.update_status(metric="Power Usage", value=power_usage)


def clock_watch(sc, tom_client: TOMClient, ip_addr: str, gpu_id: str):
    global shared_states

    # check if there's card emptied in last round
    if len(shared_states["empty_cards"]) > 0:
        tom_client.cuda_visible_devices = None
        tom_client.current_workload = {"workload": "", "mode": ""}
        if gpu_id in shared_states["serving_workload_pool"]:
            shared_states["serving_workload_pool"].pop(gpu_id)
        try:
            shared_states["empty_cards"].remove(gpu_id)
        except Exception as e:
            pass
    else:
        # bootstrap new workload
        # bootstrap will reset the cuda_visible_devices within the tom_client
        new_workload = tom_client.bootstrap_workload()
        if new_workload is not None:
            # propagate occupied cards
            all_cards = tom_client.cuda_visible_devices
            if all_cards is not None:
                all_cards = all_cards.split(",")
                for card in all_cards:
                    # this should be propagated to other tomclient
                    shared_states["serving_workload_pool"][card] = new_workload

        # if gpu_id is set in workload, then update the tom_client current_workload

        if gpu_id in shared_states["serving_workload_pool"]:
            tom_client.current_workload = shared_states["serving_workload_pool"][gpu_id]
        else:
            tom_client.current_workload = {"workload": "", "mode": ""}
        shared_states["empty_cards"].extend(tom_client.check_pods())
        for card in shared_states["empty_cards"]:
            shared_states["serving_workload_pool"].pop(card, None)
        tom_client.update_serving_status()

    clock_update_status(tom_client, gpu_id)
    sc.enter(10, 1, clock_watch, (sc, tom_client, ip_addr, gpu_id))
