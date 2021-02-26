import pytest
from pathlib import Path
from google.cloud import storage
import shutil
from google.api_core.exceptions import NotFound
from basedosdados import Storage

DATASET_ID = "pytest"
TABLE_ID = "pytest"

TABLE_FILES = ["publish.sql", "table_config.yaml"]


@pytest.fixture
def metadatadir(tmpdir_factory):
    return "tests/tmp_bases/"


@pytest.fixture
def storage(metadatadir):
    return Storage(dataset_id=DATASET_ID, table_id=TABLE_ID, metadata_path=metadatadir)


def test_upload(storage):

    storage.delete_file("municipios.csv", "staging", not_found_ok=True)

    storage.upload("tests/tmp_bases/municipios.csv", mode="staging")

    with pytest.raises(Exception):
        storage.upload("tests/tmp_bases/municipios.csv", mode="staging")

    storage.upload(
        "tests/tmp_bases/municipios.csv", mode="staging", if_exists="replace"
    )

    storage.upload(
        "tests/tmp_bases/municipios.csv",
        mode="staging",
        if_exists="replace",
        partitions="key1=value1/key2=value2",
    )

    storage.upload(
        "tests/tmp_bases/municipios.csv",
        mode="staging",
        if_exists="replace",
        partitions={"key1": "value1", "key2": "value1"},
    )

    with pytest.raises(Exception):
        storage.upload(
            "tests/tmp_bases/municipios.csv",
            mode="staging",
            if_exists="replace",
            partitions=["key1", "value1", "key2", "value1"],
        )


def test_delete_file(storage):

    storage.delete_file("municipios.csv", "staging")

    with pytest.raises(NotFound):
        storage.delete_file("municipios.csv", "staging")

    storage.delete_file("municipios.csv", "staging", not_found_ok=True)


def test_copy_table(storage):

    Storage("br_ibge_pib", "municipios").copy_table()

    with pytest.raises(ValueError):
        Storage("br_ibge_pib2", "municipios2").copy_table()

    Storage("br_ibge_pib", "municipios").copy_table(
        destination_bucket_name="basedosdados-dev",
    )


def test_delete_table(storage):

    Storage("br_ibge_pib", "municipios").delete_table(bucket_name="basedosdados-dev")

    with pytest.raises(ValueError):
        Storage("br_ibge_pib", "municipios").delete_table()
