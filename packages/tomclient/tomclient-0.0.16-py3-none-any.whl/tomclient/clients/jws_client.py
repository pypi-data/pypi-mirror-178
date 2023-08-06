import asyncio
import traceback
from jsonrpc_websocket import Server
from loguru import logger


class JWSClient:
    def __init__(self, host_url) -> None:
        self.server = Server(f"ws://{host_url}/api/v1/ws")

    def _run(self, func, kwargs, timeout=5):
        try:
            return asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(func(**kwargs), timeout)
            )
        except asyncio.TimeoutError:
            logger.error(f"timeout error... {func.__name__}")
            return None

    async def _send_status(self, current_time, metric, value, worker_id):
        try:
            if not self.server.connected:
                print("reconnecting...")
                await self.server.ws_connect()
            status = await self.server.worker_update(
                current_time, metric, value, worker_id
            )
            if status == 1:
                await self.server.worker_rejoin(
                    self.worker_id,
                    self.ip_addr,
                    self.gpu_spec,
                    self.gpu_memory,
                    self.servable,
                )
        except Exception as e:
            # in most cases we need to re-initialize nvidia-smi
            logger.error(f"failed to update... {e}")

    async def _join_worker(self, ip_addr, gpu_spec, gpu_memory, servable):
        logger.info("joining...")
        logger.info(ip_addr)
        logger.info(gpu_spec)
        logger.info(gpu_memory)
        logger.info(servable)
        try:
            if not self.server.connected:
                await self.server.ws_connect()
            self.worker_id = await self.server.worker_join(
                ip_addr, gpu_spec, gpu_memory, servable
            )
        except Exception as e:
            traceback.print_exc()
            logger.error(f"failed to join... {e}")

    async def _update_serving(self, worker_id, workload):
        try:
            if not self.server.connected:
                await self.server.ws_connect()
            await self.server.worker_updateServingStatus(worker_id, workload)
        except Exception as e:
            logger.error(f"failed to update serving status... {e}")

    async def _get_new_workload(self, worker_id):
        try:
            if not self.server.connected:
                await self.server.ws_connect()
            return await self.server.worker_getDesiredWorkload(worker_id)
        except Exception as e:
            logger.error(f"failed to get new workload... {e}")
