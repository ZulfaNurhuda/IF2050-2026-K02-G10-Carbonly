import pytest

from src.controllers.TargetEmisiController import TargetEmisiController
from src.models.TargetEmisi import TargetEmisi
from src.services.DBContext import DBContext


@pytest.fixture(autouse=True)
def temp_db(monkeypatch, tmp_path):
    db_file = tmp_path / "test_carbonly.db"
    monkeypatch.setattr(DBContext, "_DB_PATH", str(db_file))
    TargetEmisi.create_table()


def test_create_table():
    TargetEmisi.create_table()


def test_validasi_input_fail():
    assert TargetEmisi(nilaiTarget=0, satuan="kg", tahun=2026).validasiInput() is False
    assert TargetEmisi(nilaiTarget=-1, satuan="kg", tahun=2026).validasiInput() is False
    assert TargetEmisi(nilaiTarget=10, satuan="", tahun=2026).validasiInput() is False
    assert TargetEmisi(
        nilaiTarget=10, satuan="   ", tahun=2026
    ).validasiInput() is False


def test_validasi_input_pass():
    assert TargetEmisi(
        nilaiTarget=10, satuan="kg CO2e", tahun=2026
    ).validasiInput() is True


def test_insert_and_get():
    inserted = TargetEmisi.insert(
        TargetEmisi(nilaiTarget=100.5, satuan="kg CO2e", tahun=2026)
    )

    target = TargetEmisi.get()

    assert target is not None
    assert target.id == inserted.id
    assert target.nilaiTarget == 100.5
    assert target.satuan == "kg CO2e"
    assert target.tahun == 2026


def test_update():
    inserted = TargetEmisi.insert(
        TargetEmisi(nilaiTarget=100, satuan="kg CO2e", tahun=2026)
    )

    TargetEmisi.update(
        TargetEmisi(id=inserted.id, nilaiTarget=250, satuan="ton CO2e", tahun=2027)
    )
    target = TargetEmisi.get()

    assert target is not None
    assert target.id == inserted.id
    assert target.nilaiTarget == 250
    assert target.satuan == "ton CO2e"
    assert target.tahun == 2027


def test_save_insert():
    saved = TargetEmisi.save(TargetEmisi(nilaiTarget=75, satuan="kg CO2e", tahun=2026))

    assert saved.id is not None
    target = TargetEmisi.get()
    assert target is not None
    assert target.id == saved.id
    assert target.nilaiTarget == 75
    assert target.satuan == "kg CO2e"
    assert target.tahun == 2026


def test_save_update():
    inserted = TargetEmisi.save(
        TargetEmisi(nilaiTarget=75, satuan="kg CO2e", tahun=2026)
    )

    saved = TargetEmisi.save(
        TargetEmisi(id=inserted.id, nilaiTarget=125, satuan="ton CO2e", tahun=2027)
    )
    target = TargetEmisi.get()

    assert saved.id == inserted.id
    assert target is not None
    assert target.id == inserted.id
    assert target.nilaiTarget == 125
    assert target.satuan == "ton CO2e"
    assert target.tahun == 2027


def test_controller_dapatkan_target():
    inserted = TargetEmisi.insert(
        TargetEmisi(nilaiTarget=50, satuan="kg CO2e", tahun=2026)
    )
    controller = TargetEmisiController()

    target = controller.dapatkanTarget()

    assert target is not None
    assert target.id == inserted.id
    assert target.nilaiTarget == 50
    assert target.satuan == "kg CO2e"
    assert target.tahun == 2026
    assert controller.targetEmisi is target


def test_controller_simpan_target_insert():
    controller = TargetEmisiController()

    success, message = controller.simpanTarget(
        TargetEmisi(nilaiTarget=90, satuan="kg CO2e", tahun=2026)
    )

    assert success is True
    assert message == ""
    target = TargetEmisi.get()
    assert target is not None
    assert target.id is not None
    assert target.nilaiTarget == 90
    assert target.satuan == "kg CO2e"
    assert target.tahun == 2026
    assert controller.targetEmisi is not None
    assert controller.targetEmisi.id == target.id


def test_controller_simpan_target_update():
    inserted = TargetEmisi.insert(
        TargetEmisi(nilaiTarget=90, satuan="kg CO2e", tahun=2026)
    )
    controller = TargetEmisiController()

    success, message = controller.simpanTarget(
        TargetEmisi(nilaiTarget=120, satuan="ton CO2e", tahun=2027)
    )

    assert success is True
    assert message == ""
    target = TargetEmisi.get()
    assert target is not None
    assert target.id == inserted.id
    assert target.nilaiTarget == 120
    assert target.satuan == "ton CO2e"
    assert target.tahun == 2027
    assert controller.targetEmisi is not None
    assert controller.targetEmisi.id == inserted.id


def test_controller_simpan_target_invalid():
    controller = TargetEmisiController()

    success, message = controller.simpanTarget(
        TargetEmisi(nilaiTarget=0, satuan="", tahun=2026)
    )

    assert success is False
    assert message
    assert TargetEmisi.get() is None
