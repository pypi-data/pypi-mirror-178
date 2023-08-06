import os
import shutil
from pathlib import Path

import requests
from rich import print
from rich.markup import escape
from rich.panel import Panel
from tqdm import tqdm

# Google Drive links for the projects will be added here
PREBUILT_PROJECTS = {
    "[open-source][validation]-coco-2017-dataset": "https://storage.googleapis.com/encord-active-sandbox-data/%5Bopen-source%5D%5Bvalidation%5D-coco-2017-dataset.zip",
    "[open-source][test]-limuc-ulcerative-colitis-classification": "https://storage.googleapis.com/encord-active-sandbox-data/%5Bopen-source%5D%5Btest%5D-limuc-ulcerative-colitis-classification.zip",
    "[open-source]-covid-19-segmentations": "https://storage.googleapis.com/encord-active-sandbox-data/%5Bopen-source%5D-covid-19-segmentations.zip",
    "[open-source][validation]-bdd-dataset": "https://storage.googleapis.com/encord-active-sandbox-data/%5Bopen-source%5D%5Bvalidation%5D-bdd-dataset.zip",
}

PREBUILT_PROJECT_TO_STORAGE = {
    "[open-source][validation]-coco-2017-dataset": "1.1 GB",
    "[open-source][test]-limuc-ulcerative-colitis-classification": "301.3 MB",
    "[open-source]-covid-19-segmentations": "53.8 MB",
    "[open-source][validation]-bdd-dataset": "219 MB",
}


def fetch_metric(project_n: str, out_dir: Path):
    """
    Prebuilt metrics for publicly available datasets can be downloaded via this script.
    As long as we keep using Google Drive, we should keep zipped file names same for each project.
    Otherwise, Google Drive may update the links, which makes the below links obsolete.
    """
    url = PREBUILT_PROJECTS[project_n]
    output_file_name = "prebuilt_project.zip"
    output_file_path = out_dir / output_file_name
    print(f"Output destination: {escape(out_dir.as_posix())}")
    if not out_dir.is_dir():
        exit()

    r = requests.get(url, stream=True)
    total_length = int(str(r.headers.get("content-length")))
    with open(output_file_path.as_posix(), "wb") as f:
        with tqdm(total=total_length, unit="B", unit_scale=True, desc="Downloading sandbox project", ascii=True) as bar:
            for chunk in tqdm(r.iter_content(chunk_size=1024 * 1024)):
                f.write(chunk)
                bar.update(len(chunk))

    print("Unpacking zip file. May take a bit.")
    shutil.unpack_archive(output_file_path, out_dir)
    os.remove(output_file_path)

    print(
        Panel(
            f"""
Successfully downloaded sandbox dataset. To view the data, run:

[cyan blink]encord-active visualise "{escape(out_dir.as_posix())}"
        """,
            title="🌟 Success 🌟",
            style="green",
            expand=False,
        )
    )
