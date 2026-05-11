# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import Optional, Tuple

from src.models.TargetEmisi import TargetEmisi


class TargetEmisiController:
    def __init__(self):
        self._targetEmisi: Optional[TargetEmisi] = None

    @property
    def targetEmisi(self) -> Optional[TargetEmisi]:
        return self._targetEmisi

    @targetEmisi.setter
    def targetEmisi(self, value: TargetEmisi):
        self._targetEmisi = value

    # ------------------------------------------------------------------ #
    # Public operations                                                    #
    # ------------------------------------------------------------------ #

    def dapatkanTarget(self) -> Optional[TargetEmisi]:
        """Fetch the current global emission target from the database.

        Returns the TargetEmisi object, or None when no target has been set.
        Also caches the result in self._targetEmisi for convenience.
        """
        target = TargetEmisi.get()
        self._targetEmisi = target
        return target

    def tambahTarget(self, data: TargetEmisi) -> Tuple[bool, str]:
        """Create and persist a brand-new emission target (UC06).

        Parameters
        ----------
        data:
            A TargetEmisi instance populated with the desired values.
            ``id`` must be *None* (i.e. the record does not yet exist).

        Returns
        -------
        (True, "")           on success
        (False, error_msg)   on validation failure
        """
        if not data.validasiInput():
            return False, "Nilai target tidak valid. Pastikan nilainya lebih dari 0."

        saved = TargetEmisi.insert(data)
        self._targetEmisi = saved
        return True, ""

    def ubahTarget(self, data: TargetEmisi) -> Tuple[bool, str]:
        """Update an existing emission target record (UC07).

        The ``data`` object must carry a valid ``id`` that already exists in
        the database.  The method validates the new value before persisting.

        Parameters
        ----------
        data:
            TargetEmisi instance with updated values.  Must have a non-None
            ``id`` to identify which row to overwrite.

        Returns
        -------
        (True, "")           on success
        (False, error_msg)   on validation failure or missing id
        """
        if data.id is None:
            return False, "ID target tidak ditemukan."
        if not data.validasiInput():
            return False, "Nilai target tidak valid. Pastikan nilainya lebih dari 0."

        existing = TargetEmisi.get()
        if existing is None:
            return False, "Target emisi belum ditetapkan."

        existing.ubah(data)
        TargetEmisi.update(existing)
        self._targetEmisi = existing
        return True, ""

    def simpanTarget(self, data: TargetEmisi) -> Tuple[bool, str]:
        """Upsert: insert if no target exists yet, otherwise update (UC06/UC07).

        This is the primary save entry-point called by FormTargetView.

        Returns
        -------
        (True, "")           on success
        (False, error_msg)   on failure
        """
        if not data.validasiInput():
            return False, "Nilai target tidak valid. Pastikan nilainya lebih dari 0."

        existing = TargetEmisi.get()
        if existing is None:
            # UC06 – first-time target creation
            data.tahun = data.tahun or datetime.now().year
            saved = TargetEmisi.insert(data)
            self._targetEmisi = saved
        else:
            # UC07 – update existing global target
            existing.ubah(data)
            TargetEmisi.update(existing)
            self._targetEmisi = existing

        return True, ""

    def simpanLog(self, data: TargetEmisi) -> Tuple[bool, str]:
        """Alias for simpanTarget (retained for interface compatibility)."""
        return self.simpanTarget(data)