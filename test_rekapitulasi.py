# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
import sys
from datetime import datetime, timedelta

from PyQt6.QtWidgets import QApplication

sys.path.insert(0, "/home/ark/Project/IF2050-2026-K02-G10-Carbonly")

from src.views.RekapitulasiView import RekapitulasiView


class FakeRekapitulasiController:
    def dapatkanRekapitulasi(self, tanggalMulai: datetime, tanggalAkhir: datetime):
        emisi_per_hari = []
        delta = (tanggalAkhir - tanggalMulai).days
        for i in range(delta + 1):
            day = tanggalMulai + timedelta(days=i)
            val = (i % 5 + 1) * 1.5
            emisi_per_hari.append((day, val))
        total = sum(v for _, v in emisi_per_hari)
        return {
            "total_emisi": total,
            "target_emisi": 10.0,
            "log": [],
            "emisi_per_hari": emisi_per_hari,
        }


def test_rekapitulasi_view():
    app = QApplication(sys.argv)
    fake = FakeRekapitulasiController()
    view = RekapitulasiView(controller=fake)

    assert view.current_mode == "Harian"
    assert view.chart.title() == "Grafik Emisi Harian"

    view.onModeChanged("Mingguan")
    assert view.current_mode == "Mingguan"
    assert view.chart.title() == "Grafik Emisi Mingguan"

    view.onModeChanged("Harian")
    assert view.current_mode == "Harian"
    assert view.chart.title() == "Grafik Emisi Harian"

    print("PASS: All assertions passed")


if __name__ == "__main__":
    test_rekapitulasi_view()
