import csv
import ftplib
import gzip
import os
import shutil
from datetime import datetime
from io import BytesIO
from pathlib import Path
from socket import gaierror
from tempfile import gettempdir
from hashlib import md5
from typing import Dict, List

import numpy as np
import pandas as pd
import rasterio


class _wpFTP:
    timeout = 10  # ftp timeout, in seconds

    def __init__(
        self, server: str = "ftp.worldpop.org.uk", username: str = "anonymous", password: str = ""
    ):
        self.server = server
        self.username = username
        self.password = password

        self.__connect()

    def __connect(self):
        try:
            self.ftp = ftplib.FTP(self.server, self.username, self.password, timeout=self.timeout)
        except ftplib.error_perm as err:
            raise err
        except gaierror as err:
            raise err

        self.ftp.sendcmd("TYPE i")  # switch to binary mode

    def __repr__(self):
        return type(self).__name__ + " <" + self.username + "@" + self.server + ">"

    def __del__(self):
        if hasattr(self, "ftp"):
            self.ftp.close()

    @property
    def csv_signature(self):
        bio = BytesIO()
        p = Path("/assets/wpgpDatasets.md5")
        self.ftp.retrbinary("RETR " + p.as_posix(), bio.write)
        bio.seek(0)
        result = bio.read().decode("utf-8")
        result = result.strip()
        result = result.split(" ")[0]
        return result

    def get_timestamp(self, ftp_absolute_path: str):
        p = Path(ftp_absolute_path)

        response_code, time = self.ftp.sendcmd("MDTM %s" + p.as_posix()).split(" ")

        if response_code != "213":
            raise ValueError(f"Could not get timestamp for {ftp_absolute_path}")

        return datetime.strptime(time, "%Y%m%d%H%M%S")

    def get_filesize(self, ftp_absolute_path):
        p = Path(ftp_absolute_path)

        try:
            filesize = self.ftp.size(p.as_posix())
        except ftplib.error_perm as _:
            raise ftplib.error_perm(f"FTP complained for file: '{p.as_posix()}'.")

        if not filesize is None and filesize >= 0:
            return filesize

        return None

    def download(self, from_ftp_absolute_path: str, to_local_absolute_path: str):
        p_ftp = Path(from_ftp_absolute_path)
        p_local = Path(to_local_absolute_path).joinpath(p_ftp.name)
        file_size = self.get_filesize(p_ftp.as_posix())

        if file_size is None:
            raise ValueError(f"Could not get filesize for {p_ftp.as_posix()}")

        if p_local.exists():
            os.remove(p_local.as_posix())

        with open(p_local.as_posix(), "wb") as f:
            self.ftp.retrbinary("RETR " + p_ftp.as_posix(), f.write, blocksize=8192, rest=None)

        return p_local.as_posix()


class WP:
    csv_signature = None
    csv_file = None
    csv_file_gzip = None
    options: List[str] = []
    data: Dict[str, Dict[str, Dict[str, str]]] = {}
    temp_dir = os.path.join(gettempdir(), "worldpop")

    def __init__(self) -> None:
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        self.ftp = _wpFTP()
        if self.ftp.csv_signature != self.csv_signature:
            self.__refresh_csv_signature()

        self.__load_recourses()

    def __refresh_csv_signature(self):
        self.csv_file = self.ftp.download("/assets/wpgpDatasets.csv", self.temp_dir)

        with open(self.csv_file, "rb") as f:
            self.csv_file_gzip = os.path.join(self.temp_dir, "wpgpDatasets.csv.gz")
            with gzip.open(self.csv_file_gzip, "wb") as f_out:
                shutil.copyfileobj(f, f_out)

        signature = md5()

        signature.update(gzip.open(self.csv_file_gzip, "rb").read())
        signature.digest().hex()

        self.csv_signature = signature

    def __load_recourses(self):
        if self.csv_file is None or self.csv_file_gzip is None:
            self.__refresh_csv_signature()

        if self.csv_file is None or self.csv_file_gzip is None:
            raise ValueError("Could not load csv files")

        with gzip.open(self.csv_file_gzip, "rt") as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                iso = row["ISO3"]
                option = row["Covariate"]
                description = row["Description"]
                path = row["PathToRaster"]

                if not iso in self.data:
                    self.data[iso] = {}

                if not option in self.data[iso]:
                    self.data[iso][option] = {}

                self.data[iso][option]["description"] = description
                self.data[iso][option]["path"] = path

                if not option in self.options:
                    self.options.append(option)

    def get_file(
        self,
        iso: str,
        option: str,
        to_local_absolute_path: str = os.path.join(gettempdir(), "worldpop"),
    ):
        if not iso in self.data:
            raise ValueError(f"ISO {iso} not found.")

        if not option in self.data[iso]:
            raise ValueError(f"Option {option} not found for ISO {iso}.")

        path = self.data[iso][option]["path"]
        return self.ftp.download(path, to_local_absolute_path)

    def to_pandas(self, iso: str, option: str):
        path = self.get_file(iso, option)
        dataset = rasterio.open(path)
        band1 = dataset.read(1)
        height, width = band1.shape
        cols, rows = np.meshgrid(np.arange(width), np.arange(height))
        xs, ys = rasterio.transform.xy(dataset.transform, rows, cols)  # type: ignore
        lons = np.array(xs)
        lats = np.array(ys)
        coordinates = np.dstack((lats, lons, band1))
        df = pd.DataFrame(coordinates.reshape(-1, 3), columns=["lat", "lon", "population"])

        return df
