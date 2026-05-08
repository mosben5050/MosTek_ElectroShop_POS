# Responsive Design Checklist

Every new screen, page, dialog, or widget in MosTek ElectroPOS must
pass this checklist before being merged to main. The goal: avoid the
"works on my screen, breaks on theirs" trap.

## Why this matters

Our customers run this app on machines ranging from:
- Modern 24" desktop monitors (1920×1080)
- Mid-range office laptops (1600×900)
- Budget Windows laptops (1366×768) — **THE COMMON CASE**
- Older POS terminals (1280×720 and below)

A screen that "works fine on the dev machine" but breaks on a 1366×768
laptop is broken in production.

---

## Test at three sizes before declaring a screen done

### 1. Maximised (1920×1080 or whatever your monitor is)
- Content uses available space sensibly
- Nothing stretches absurdly wide
- White space looks intentional, not empty

### 2. Standard laptop (1366×768)
- Nothing is clipped horizontally
- Nothing is clipped vertically (if it could be, the page should scroll)
- All buttons and inputs are clickable / readable
- Text doesn't overlap with other elements

### 3. Minimum supported size (1024×600)
- The page is still usable, even if tighter
- Critical actions (save, cancel, primary CTA) remain visible without scrolling
- Vertical scrollbars appear where needed instead of clipping

**How to test:** un-maximise the window and drag the corner inward
to each size. Quick visual scan at each.

---

## Layout rules (apply to every screen)

### NEVER do these
- ❌ `widget.setFixedSize(width, height)` — use min/max instead
- ❌ `widget.setFixedWidth(N)` on content that holds text or forms
- ❌ Hard-coded pixel widths in QSS for content widgets
- ❌ Absolute positioning with manual coordinates
- ❌ Trust that a window will be a specific size

### ALWAYS do these
- ✅ Use `QHBoxLayout` / `QVBoxLayout` / `QGridLayout` for everything
- ✅ Set `setSizePolicy(Expanding, ...)` on widgets that should grow
- ✅ Use `setMinimumWidth` and `setMaximumWidth` instead of `setFixedWidth`
- ✅ Wrap long content in `QScrollArea` (or inherit from `BasePage` which provides one)
- ✅ Use `addStretch()` to push content into intentional positions
- ✅ Use `setMinimumSize()` to declare what you need, not `setFixedSize()`

### When fixed dimensions ARE acceptable
- Icons / avatars / logos (visual elements with intentional dimensions)
- Decorative elements (e.g. accent lines)
- Modal dialogs with constrained content
- Form cards centred in a flexible parent (use min/max, not fixed)

---

## Specific patterns to use

### Centred form/card
```python
# DON'T: card.setFixedWidth(520) inside a tight container
# DO: flexible width with sensible bounds
card.setMinimumWidth(360)
card.setMaximumWidth(520)
# Then centre it via wrapping HBoxLayout with stretches on both sides
```

### Two-column layout that collapses
```python
# Watch the parent width via resizeEvent and hide one column
# below a threshold (e.g. 900px). See login_page.py (TODO) for example.
```

### Pages with potentially overflowing content
```python
# Inherit from BasePage — it provides QScrollArea automatically
class MyPage(BasePage):
    def __init__(self):
        super().__init__(title="My Page")
        self.content_layout.addWidget(...)  # add anything; it scrolls
```

### Action buttons in a row
```python
# Use addStretch() to push them to the right
row = QHBoxLayout()
row.addStretch()
row.addWidget(SecondaryButton("Cancel"))
row.addWidget(PrimaryButton("Save"))
# At narrow widths, both buttons stay visible and right-aligned
```

---

## Font and spacing rules

- Use only token values from `tokens.py` (FONT_SIZE_*, SPACE_*)
- Don't invent intermediate sizes — if 14px and 16px exist and you want 15px, ask why
- Body text should never be smaller than `FONT_SIZE_BASE` (14px)
- Touch targets (buttons, clickable rows) should be at least 40px tall

---

## Pre-merge sign-off

Before considering any new screen complete:

- [ ] Tested at 1920×1080 (or larger)
- [ ] Tested at 1366×768
- [ ] Tested at 1024×600 (the floor)
- [ ] No `setFixedSize` / `setFixedWidth` on content widgets
- [ ] All long content scrollable, not clipped
- [ ] Action buttons remain visible at all sizes
- [ ] Inputs and labels do not overlap
- [ ] Text remains readable (no truncation without ellipsis)

If any box is unchecked, the screen is not done.