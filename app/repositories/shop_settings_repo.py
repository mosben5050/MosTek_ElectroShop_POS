"""Shop settings repository — read/write the single-row shop_settings table.

The schema enforces that only one row exists (id = 1). This repo wraps
that constraint so the rest of the app can think of settings as a single
object, not a table.
"""
from typing import Optional, Dict, Any

from app.database.connection import get_connection


class ShopSettingsRepository:
    """Data access for the singleton shop_settings table."""

    # ────────────────────────────────────────────────────────────
    # Read
    # ────────────────────────────────────────────────────────────
    def get(self) -> Dict[str, Any]:
        """Return the current shop settings as a dict.

        The schema seeds row id=1 on first run, so this should never
        return None in practice.
        """
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM shop_settings WHERE id = 1"
            ).fetchone()
        if row is None:
            # Defensive — should not happen, but if it does, seed and retry
            self._ensure_row_exists()
            return self.get()
        return dict(row)

    def is_configured(self) -> bool:
        """Return True if the shop has been set up at least once.

        We treat the shop as 'configured' once shop_name has been changed
        from the default 'My Shop'. This drives the first-run wizard.
        """
        settings = self.get()
        return (settings.get("shop_name") or "").strip().lower() not in (
            "", "my shop"
        )

    # ────────────────────────────────────────────────────────────
    # Write
    # ────────────────────────────────────────────────────────────
    def update(self, **fields) -> None:
        """Update one or more shop_settings columns.

        Pass keyword arguments matching column names, e.g.:
            update(shop_name="Albedida Electronics", phone="0244111222")

        Unknown columns are silently ignored (no SQL injection risk because
        we whitelist column names).
        """
        if not fields:
            return

        # Whitelist of columns we allow updating from this method
        allowed = {
            "shop_name", "address", "phone", "email", "ghanapost_code",
            "tax_mode", "flat_rate_pct", "vat_pct", "nhil_pct",
            "getfund_pct", "covid_pct", "currency_symbol", "receipt_footer",
        }

        safe_fields = {k: v for k, v in fields.items() if k in allowed}
        if not safe_fields:
            return

        set_clause = ", ".join(f"{col} = ?" for col in safe_fields.keys())
        values = list(safe_fields.values())

        with get_connection() as conn:
            conn.execute(
                f"UPDATE shop_settings SET {set_clause} WHERE id = 1",
                values,
            )
            conn.commit()

    # ────────────────────────────────────────────────────────────
    # Internal
    # ────────────────────────────────────────────────────────────
    @staticmethod
    def _ensure_row_exists() -> None:
        """Insert the singleton row if for some reason it's missing."""
        with get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO shop_settings (id) VALUES (1)")
            conn.commit()