import os

import yaml


def parse_servable_config(working_dir: str):
    tom_config_file = os.path.join(working_dir, "tom.yaml")
    if not os.path.exists(tom_config_file):
        raise Exception(f"tom.yaml file not found in {working_dir}")
    try:
        with open(tom_config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        raise Exception(f"Failed to load TOM configuration file {tom_config_file}: {e}")
    # fill default values
    if "mode" not in config:
        config["mode"] = []
    for idx, mode_entry in enumerate(config["mode"]):
        if "gpu" not in mode_entry:
            config["mode"][idx]["gpu"] = 1
    return config


def list_servable_workload(working_dir: str):
    """
    reads the directories in working_dir
    and returns a dictionary between: workload_name: [mode1, mode2, ...]
    """
    # list all directories in working_dir
    servables = [
        x
        for x in os.listdir(working_dir)
        if os.path.isdir(os.path.join(working_dir, x))
    ]
    servable_workloads = []
    for servable in servables:
        try:
            servable_config = parse_servable_config(os.path.join(working_dir, servable))
            servable_workloads.append(
                {
                    "name": servable_config["workload"],
                    "modes": [mode["name"] for mode in servable_config["mode"]],
                }
            )
        except Exception:
            pass
    return servable_workloads


def safe_get_cuda_visible_devices(
    tom_config, bootstrap_payload, mode_entry, current_gpu_id, total_gpu_count
):

    """
    We manage the CUDA device by properly set the CUDA_VISIBLE_DEVICES, with the following principles:
    - If CUDA_VISIBLE_DEVICES is already set in the system - this is usually the case when the tomclient daemon is started by the cluster manager (slurm, etc.) - then we don't violate existing settings.
    - If this model only requires one GPU, we will assign the GPU with the corresponding ID.
    - else, If the user specifies the CUDA_VISIBLE_DEVICES, we use it.
        - If the user-specified CUDA_VISIBLE_DEVICES is not valid, we need to process.
        - Invalid GPU ids:
            * Not enough for the required GPU number - raise an error;
            * GPU id is not available. - unsure how to check this?
    - else, If the user does not specify the CUDA_VISIBLE_DEVICES, we use the GPU ID corresponding to the current worker, and several other GPUs.
    """
    if os.environ.get("CUDA_VISIBLE_DEVICES") is not None:
        return os.environ.get("CUDA_VISIBLE_DEVICES")
    if mode_entry["gpu"] == 1:
        return f"{current_gpu_id}"
    if "CUDA_VISIBLE_DEVICES" in bootstrap_payload:
        # check if the user-specified CUDA_VISIBLE_DEVICES is valid
        user_specified_gpu_ids = bootstrap_payload["CUDA_VISIBLE_DEVICES"].split(",")
        if len(user_specified_gpu_ids) < mode_entry["gpu"]:
            raise Exception(
                f"Invalid CUDA_VISIBLE_DEVICES: {bootstrap_payload['CUDA_VISIBLE_DEVICES']}, not enough GPUs for the workload."
            )
    return bootstrap_payload["CUDA_VISIBLE_DEVICES"]
