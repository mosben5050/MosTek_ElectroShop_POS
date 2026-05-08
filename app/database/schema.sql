-- ════════════════════════════════════════════════════════════════════
-- MosTek ElectroPOS — Database Schema
-- SQLite 3
-- ════════════════════════════════════════════════════════════════════

-- Enable foreign key enforcement (SQLite has it off by default)
PRAGMA foreign_keys = ON;


-- ────────────────────────────────────────────────────────────────────
-- Users — staff who log into the system
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    full_name       TEXT    NOT NULL,
    role            TEXT    NOT NULL CHECK (role IN ('admin', 'cashier', 'technician')),
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    last_login_at   TEXT
);


-- ────────────────────────────────────────────────────────────────────
-- Shop settings — one row only, holds tax + receipt info
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS shop_settings (
    id              INTEGER PRIMARY KEY CHECK (id = 1),  -- enforces single row
    shop_name       TEXT    NOT NULL DEFAULT 'My Shop',
    address         TEXT,
    phone           TEXT,
    email           TEXT,
    ghanapost_code  TEXT,
    tax_mode        TEXT    NOT NULL DEFAULT 'none'
                            CHECK (tax_mode IN ('none', 'flat_rate', 'vat_standard')),
    flat_rate_pct   REAL    NOT NULL DEFAULT 3.0,
    vat_pct         REAL    NOT NULL DEFAULT 15.0,
    nhil_pct        REAL    NOT NULL DEFAULT 2.5,
    getfund_pct     REAL    NOT NULL DEFAULT 2.5,
    covid_pct       REAL    NOT NULL DEFAULT 1.0,
    currency_symbol TEXT    NOT NULL DEFAULT 'GHS',
    receipt_footer  TEXT    DEFAULT 'Thank you for your business!'
);


-- ────────────────────────────────────────────────────────────────────
-- Categories — for grouping products (Phones, Cables, Batteries, etc.)
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);


-- ────────────────────────────────────────────────────────────────────
-- Products — items the shop sells (and parts used in repairs)
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sku             TEXT    NOT NULL UNIQUE,
    barcode         TEXT    UNIQUE,
    name            TEXT    NOT NULL,
    description     TEXT,
    category_id     INTEGER,
    cost_price      REAL    NOT NULL DEFAULT 0,
    selling_price   REAL    NOT NULL DEFAULT 0,
    stock_qty       INTEGER NOT NULL DEFAULT 0,
    reorder_level   INTEGER NOT NULL DEFAULT 0,
    is_service      INTEGER NOT NULL DEFAULT 0,  -- 1 = service (no stock), 0 = physical product
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_products_name     ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_barcode  ON products(barcode);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);


-- ────────────────────────────────────────────────────────────────────
-- Stock movements — audit trail of every stock change
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stock_movements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL,
    change_qty      INTEGER NOT NULL,  -- positive = in, negative = out
    reason          TEXT    NOT NULL CHECK (reason IN
                        ('purchase', 'sale', 'return', 'repair_use',
                         'damaged', 'stock_take', 'adjustment')),
    reference_id    INTEGER,           -- e.g. sale id or repair id
    notes           TEXT,
    user_id         INTEGER,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id)    REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id);


-- ────────────────────────────────────────────────────────────────────
-- Customers
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    phone       TEXT    UNIQUE,           -- main lookup key
    email       TEXT,
    address     TEXT,
    notes       TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_customers_name  ON customers(name);


-- ────────────────────────────────────────────────────────────────────
-- Sales — header record for each transaction
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sales (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_no      TEXT    NOT NULL UNIQUE,
    customer_id     INTEGER,
    user_id         INTEGER NOT NULL,
    subtotal        REAL    NOT NULL DEFAULT 0,
    discount        REAL    NOT NULL DEFAULT 0,
    tax_total       REAL    NOT NULL DEFAULT 0,
    total           REAL    NOT NULL DEFAULT 0,
    payment_method  TEXT    NOT NULL CHECK (payment_method IN
                        ('cash', 'momo', 'card', 'bank_transfer', 'mixed')),
    amount_paid     REAL    NOT NULL DEFAULT 0,
    change_given    REAL    NOT NULL DEFAULT 0,
    status          TEXT    NOT NULL DEFAULT 'completed'
                            CHECK (status IN ('completed', 'voided', 'refunded')),
    notes           TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (user_id)     REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_sales_created  ON sales(created_at);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id);


-- ────────────────────────────────────────────────────────────────────
-- Sale items — line items for each sale
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sale_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id         INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    product_name    TEXT    NOT NULL,  -- snapshot in case product is later renamed
    quantity        INTEGER NOT NULL,
    unit_price      REAL    NOT NULL,
    discount        REAL    NOT NULL DEFAULT 0,
    line_total      REAL    NOT NULL,
    FOREIGN KEY (sale_id)    REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX IF NOT EXISTS idx_sale_items_sale ON sale_items(sale_id);


-- ────────────────────────────────────────────────────────────────────
-- Repair tickets — devices brought in for repair
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS repair_tickets (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_no           TEXT    NOT NULL UNIQUE,
    customer_id         INTEGER NOT NULL,
    device_type         TEXT    NOT NULL,   -- e.g. Phone, Laptop, TV
    device_brand        TEXT,
    device_model        TEXT,
    serial_or_imei      TEXT,
    accessories         TEXT,                -- charger, cover, sim card, etc.
    condition_on_arrival TEXT,
    reported_fault      TEXT    NOT NULL,
    diagnosis           TEXT,
    work_done           TEXT,
    quoted_price        REAL    NOT NULL DEFAULT 0,
    deposit_paid        REAL    NOT NULL DEFAULT 0,
    final_price         REAL    NOT NULL DEFAULT 0,
    status              TEXT    NOT NULL DEFAULT 'received'
                                CHECK (status IN ('received', 'diagnosed',
                                                  'awaiting_parts', 'in_progress',
                                                  'repaired', 'collected',
                                                  'unrepairable', 'cancelled')),
    received_by         INTEGER NOT NULL,    -- user_id
    received_at         TEXT    NOT NULL DEFAULT (datetime('now')),
    completed_at        TEXT,
    collected_at        TEXT,
    sale_id             INTEGER,             -- linked when converted to sale on pickup
    notes               TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (received_by) REFERENCES users(id),
    FOREIGN KEY (sale_id)     REFERENCES sales(id)
);

CREATE INDEX IF NOT EXISTS idx_repairs_status   ON repair_tickets(status);
CREATE INDEX IF NOT EXISTS idx_repairs_customer ON repair_tickets(customer_id);


-- ────────────────────────────────────────────────────────────────────
-- Repair parts — parts consumed in a repair
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS repair_parts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    repair_id       INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    product_name    TEXT    NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      REAL    NOT NULL,
    line_total      REAL    NOT NULL,
    FOREIGN KEY (repair_id)  REFERENCES repair_tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);


-- ────────────────────────────────────────────────────────────────────
-- Audit log — track sensitive actions (voids, price changes, etc.)
-- ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    action      TEXT    NOT NULL,     -- e.g. 'void_sale', 'price_change'
    entity      TEXT,                  -- e.g. 'sale', 'product'
    entity_id   INTEGER,
    details     TEXT,                  -- free-form JSON or text
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);


-- ════════════════════════════════════════════════════════════════════
-- Seed data — one row in shop_settings (so we always have settings)
-- ════════════════════════════════════════════════════════════════════
INSERT OR IGNORE INTO shop_settings (id) VALUES (1);