from pyppeteer import chromium_downloader
from pyppeteer.chromium_downloader import logger as pyppeteer_logger
from pyppeteer.chromium_downloader import DOWNLOADS_FOLDER, REVISION
import urllib3
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
)
from io import BytesIO


def download_chromium():
    url = chromium_downloader.get_url()
    filename = url.split('/')[-1]

    urllib3.disable_warnings()
    with urllib3.PoolManager() as http:
        # Get data from url.
        # set preload_content=False means using stream later.
        data = http.request('GET', url, preload_content=False)

        try:
            total_length = int(data.headers['content-length'])
        except (KeyError, ValueError, AttributeError):
            total_length = 0

        progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )

        task_id = progress.add_task('Chromium download', filename=filename, total=total_length, start=True)

        with progress:
            # 10 * 1024
            _data = BytesIO()
            for chunk in data.stream(32768):
                _data.write(chunk)
                progress.update(task_id, advance=len(chunk))

    pyppeteer_logger.disabled = True
    chromium_downloader.extract_zip(_data, DOWNLOADS_FOLDER / REVISION)
    pyppeteer_logger.disabled = False
