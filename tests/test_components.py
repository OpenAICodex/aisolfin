from __future__ import annotations

from tokens import THEME, css_variables, flatten_tokens


def test_token_flatten_has_primary_color() -> None:
    flat = flatten_tokens()
    assert flat["colors_primary"] == THEME.colors.primary


def test_css_variables_contains_primary() -> None:
    css = css_variables()
    assert "--colors-primary" in css
