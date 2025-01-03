from pathlib import Path
from typing import Literal

from modules import Logger
from modules.request import Api
from modules.filesystem import download, Directory

from ..deployment_info import Deployment


def download_missing_files(deployment: Deployment, mode: Literal["Player", "Studio"], missing_file_hashes: list[str]) -> None:
    for item in deployment.package_manifest:
        if item["hash"] not in missing_file_hashes:
            continue
        
        file: str = item["file"]
        hash: str = item["hash"]
        size: int = item["size"]

        size_mb: float = round(size / 1048576, 2)
        Logger.info(f"Downloading file: {file} (hash: {hash}, size: {size_mb} MB)")
        download_target: Path = Directory.DOWNLOADS / mode / hash
        
        download(Api.Roblox.Deployment.download(deployment.version, file), download_target)














# Downloading each file simulatneously
# from pathlib import Path
# from typing import Literal
# from queue import Queue
# from threading import Thread

# from modules import Logger
# from modules.request import Api
# from modules.filesystem import download, Directory

# from ..deployment_info import Deployment


# def download_missing_files(deployment: Deployment, mode: Literal["Player", "Studio"], missing_file_hashes: list[str]) -> None:
#     exception_queue: Queue = Queue()
#     threads: list[Thread] = []

#     for item in deployment.package_manifest:
#         if item["hash"] not in missing_file_hashes:
#             continue
        
#         file: str = item["file"]
#         thread = Thread(name=f"file-download-thread_{file}", target=worker, args=(deployment, mode, item, exception_queue), daemon=True)
#         threads.append(thread)
#         thread.start()
    
#     for thread in threads:
#         thread.join()
    
#     if not exception_queue.empty():
#         raise exception_queue.get()


# # Download each file simultaneously
# def worker(deployment: Deployment, mode: Literal["Player", "Studio"], item: dict, exception_queue: Queue) -> None:
#     try:
#         file: str = item["file"]
#         hash: str = item["hash"]
#         size: int = item["size"]

#         size_mb: float = round(size / 1048576, 2)
#         Logger.info(f"Downloading file: {file} (hash: {hash}, size: {size_mb} MB)")
#         download_target: Path = Directory.DOWNLOADS / mode / hash
        
#         download(Api.Roblox.Deployment.download(deployment.version, file), download_target)

#     except Exception as e:
#         Logger.error(f"Failed to download file: {file}! {type(e).__name__}: {e}")
#         exception_queue.put(e)