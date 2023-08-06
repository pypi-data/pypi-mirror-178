import os
import traceback
from time import time

from jsonrpc_websocket import Server
from loguru import logger
from psutil import STATUS_ZOMBIE
from tomclient.clients.jws_client import JWSClient
from tomclient.pods.manager import podmanager
from tomclient.utility import (
    list_servable_workload,
    parse_servable_config,
    safe_get_cuda_visible_devices,
)


class TOMClient(JWSClient):
    def __init__(self, host_url):
        self.server = Server(f"ws://{host_url}/api/v1/ws")
        self.worker_id: str = ""
        self.ip_addr: str = ""
        self.gpu_spec: str = ""
        self.gpu_memory: str = ""
        self.current_workload: str = {"workload": "", "mode": ""}
        self.working_dir = ""
        self.cuda_visible_devices = None

    def update_status(self, metric: str, value: str):
        current_time = int(time())
        self._run(
            self._send_status,
            kwargs={
                "current_time": current_time,
                "metric": metric,
                "value": value,
                "worker_id": self.worker_id,
            },
        )

    def join(
        self,
        ip_addr: str,
        gpu_id: int,
        gpu_spec: str,
        gpu_memory: str,
        working_dir: str = ".",
        total_gpus: int = 1,
    ):
        self.ip_addr = ip_addr
        self.gpu_spec = gpu_spec
        self.gpu_memory = gpu_memory
        self.servable = list_servable_workload(working_dir)
        self.working_dir = working_dir
        self.gpu_id = gpu_id
        self.total_gpus = total_gpus
        self._run(
            self._join_worker,
            kwargs={
                "ip_addr": ip_addr,
                "gpu_spec": gpu_spec,
                "gpu_memory": gpu_memory,
                "servable": self.servable,
            },
        )

    def update_serving_status(self):
        workload = (
            f"{self.current_workload['workload']}:{self.current_workload['mode']}"
        )
        self._run(
            self._update_serving,
            kwargs={"worker_id": self.worker_id, "workload": workload},
        )

    def bootstrap_workload(self):
        # read tom.yaml file
        # check if workload is changed
        # if changed, bootstrap the workload
        new_workload = self._run(self._get_new_workload, {"worker_id": self.worker_id})
        if new_workload:
            if new_workload["workload"] != "":
                if new_workload != self.current_workload:
                    logger.info(f"New Workload: {new_workload}")
                    logger.debug(f"current workload {self.current_workload}")
                    self.start_worker_pod(
                        new_workload=new_workload,
                        bootstrap_payload=new_workload["bootstrap_config"],
                    )
                else:
                    new_workload = None
            else:
                new_workload = None
        return new_workload

    def start_worker_pod(self, new_workload, bootstrap_payload=None):
        working_dir = os.path.join(self.working_dir, new_workload["workload"])
        try:
            tom_config = parse_servable_config(working_dir)
        except Exception as e:
            logger.error(f"Failed to parse TOM configuration file: {e}")
            return
        pod_name = (
            tom_config["workload"] + ":" + new_workload["mode"] + ":" + self.worker_id
        )
        # prepare environment variables
        envs = {env["name"]: env["value"] for env in tom_config["spec"]["env"]}
        pod = podmanager.get_pod(pod_name)
        if pod is not None:
            logger.error(f"Pod {pod_name} already exists")
            return
        mode_found = False
        for mode_entry in tom_config["mode"]:
            if mode_entry["name"] == new_workload["mode"]:
                mode_found = True
                # prepare environment variables

                # process CUDA_VISIBLE_DEVICES
                try:
                    cuda_visible_devices = safe_get_cuda_visible_devices(
                        tom_config,
                        bootstrap_payload,
                        mode_entry,
                        self.gpu_id,
                        self.total_gpus,
                    )
                    print(cuda_visible_devices)
                    envs["CUDA_VISIBLE_DEVICES"] = cuda_visible_devices
                    self.cuda_visible_devices = cuda_visible_devices
                except Exception as e:
                    logger.error(f"Failed to pre-allocate CUDA_VISIBLE_DEVICES: {e}")
                    return
                entrypoint_script = mode_entry["entrypoint"]
                # kill old pod
                existing_pods = podmanager.get_pods()
                existing_pods_on_gpu = [
                    pod for pod in existing_pods if pod.name.endswith(self.worker_id)
                ]
                podmanager.kill(existing_pods_on_gpu)
                logger.info(f"envs: {envs}")
                podmanager.run(
                    f"cd {working_dir} && /bin/bash {entrypoint_script}",
                    name=pod_name,
                    check=True,
                    additional_env=envs,
                )

                return cuda_visible_devices
        if not mode_found:
            logger.error(
                f"Mode {new_workload['mode']} not found in TOM configuration file"
            )
            return

    def check_pods(self):
        emptied_cards = []
        pods = podmanager.get_pods()
        for pod in pods:
            if pod.proc is None:
                logger.info("cleaning pod: " + pod.name)
                # pod from last run
                podmanager.clean_pod(pod)
            if pod.proc.status() == STATUS_ZOMBIE:
                logger.info("releasing pod: " + pod.name)
                # try to get envs - if failed - skip it
                try:
                    occupied_cards = pod.env["CUDA_VISIBLE_DEVICES"].split(",")
                    emptied_cards.extend(occupied_cards)
                    logger.info(f"releasing cards: {emptied_cards}")
                    # podmanager.clean_pod(pod)
                except Exception as e:
                    traceback.print_exc()
                    logger.error(f"failed to clean pod: {e}")
        return emptied_cards
