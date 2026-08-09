#!/usr/bin/env python3
"""Compound-Hazard Decision Pathway.

Plan: Link official post-earthquake threshold adjustment and rainfall exposure to
slope disruption, road failure, community isolation, service loss, and
intervention choice.
Framework: Section 5 scenario identification; Section 6 linked rainfall,
landslide-score, road-score, Monte Carlo network, consequence, and robust
intervention framework; Section 7 integration workflow and evidence gates.

The SVG is the authoritative editable figure. The planned PNG is rendered from
that SVG at 150 dpi by the same reproducible script.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import shutil
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = ROOT / "data/results/figures"
SVG_PATH = FIGURE_DIR / "Figure_compound_hazard_decision_pathway.svg"
PNG_PATH = FIGURE_DIR / "Figure_compound_hazard_decision_pathway.png"

WIDTH = 1600
HEIGHT = 720
PNG_WIDTH = 2400
PNG_HEIGHT = 1080

COLORS = {
    "ink": "#172033",
    "text": "#344054",
    "arrow": "#475467",
    "blue": "#DCEBFA",
    "blue_edge": "#3B78A8",
    "amber": "#FCECCB",
    "amber_edge": "#B7791F",
    "red": "#F9DEDC",
    "red_edge": "#B5473C",
    "purple": "#EAE1F5",
    "purple_edge": "#76549A",
    "green": "#DDF1E5",
    "green_edge": "#34835B",
    "grey": "#F2F4F7",
    "grey_edge": "#667085",
}


def multiline_text(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: float,
    weight: int = 400,
    fill: str = COLORS["text"],
    line_height: float = 1.2,
    anchor: str = "middle",
) -> str:
    """Return centered SVG text with one tspan per line."""
    spans = []
    for index, line in enumerate(lines):
        dy = "0" if index == 0 else f"{size * line_height:.1f}"
        spans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size:.1f}" font-weight="{weight}" fill="{fill}">'
        + "".join(spans)
        + "</text>"
    )


def box(
    x: float,
    y: float,
    width: float,
    height: float,
    heading: list[str],
    body: list[str],
    *,
    face: str,
    edge: str,
    heading_size: float = 16,
    body_size: float = 13,
    stroke_width: float = 2.4,
) -> str:
    """Return a rounded SVG process/evidence box."""
    heading_y = y + height * (0.34 if len(heading) == 1 else 0.27)
    body_y = y + height * (0.67 if len(heading) == 1 else 0.63)
    return "\n".join(
        [
            (
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" '
                f'fill="{face}" stroke="{edge}" stroke-width="{stroke_width}"/>'
            ),
            multiline_text(
                x + width / 2,
                heading_y,
                heading,
                size=heading_size,
                weight=700,
                fill=COLORS["ink"],
                line_height=1.05,
            ),
            multiline_text(
                x + width / 2,
                body_y,
                body,
                size=body_size,
                fill=COLORS["text"],
                line_height=1.18,
            ),
        ]
    )


def arrow(
    path: str,
    *,
    color: str = COLORS["arrow"],
    width: float = 2.6,
    marker: str = "arrow-grey",
) -> str:
    """Return an SVG path with a matching arrowhead marker."""
    return (
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{marker})"/>'
    )


def marker_definition(marker_id: str, color: str) -> str:
    """Return an SVG arrowhead marker definition."""
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="8.4" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
    )


def build_svg() -> str:
    """Build the vector diagram as an SVG document."""
    marker_specs = {
        "arrow-grey": COLORS["arrow"],
        "arrow-blue": COLORS["blue_edge"],
        "arrow-amber": COLORS["amber_edge"],
        "arrow-slate": COLORS["grey_edge"],
        "arrow-red": COLORS["red_edge"],
        "arrow-purple": COLORS["purple_edge"],
    }
    markers = "\n".join(marker_definition(name, color) for name, color in marker_specs.items())

    elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PNG_WIDTH}px" height="{PNG_HEIGHT}px" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<defs>",
        markers,
        "<style>",
        "text { font-family: Arial, Helvetica, sans-serif; }",
        "</style>",
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#FFFFFF"/>',
    ]

    # Inputs and assumptions.
    elements.extend(
        [
            multiline_text(
                25,
                30,
                ["Scenario and terrain inputs"],
                size=11.5,
                weight=700,
                fill=COLORS["grey_edge"],
                anchor="start",
            ),
            box(
                25,
                50,
                235,
                115,
                ["Rainfall exposure"],
                ["Hourly Rainfall", "1, 3, 24, 72 h accumulation", "Moderate  |  Heavy  |  Extreme"],
                face=COLORS["blue"],
                edge=COLORS["blue_edge"],
                heading_size=14.0,
                body_size=11.1,
            ),
            box(
                290,
                50,
                235,
                115,
                ["Earthquake-adjusted", "threshold"],
                ["Threshold Retention Factor", "Baseline 1.00  |  Central 0.80", "High 0.70"],
                face=COLORS["amber"],
                edge=COLORS["amber_edge"],
                heading_size=12.5,
                body_size=10.8,
            ),
            box(
                555,
                50,
                235,
                115,
                ["Terrain and warning", "context"],
                ["Elevation  |  slope  |  curvature", "Official warning-zone", "exposure"],
                face=COLORS["grey"],
                edge=COLORS["grey_edge"],
                heading_size=12.5,
                body_size=10.8,
            ),
        ]
    )

    # Main compound-hazard pathway.
    stage_x = [25, 290, 555, 820, 1085, 1350]
    stage_w = 220
    stage_y = 285
    stage_h = 180
    elements.append(
        multiline_text(
            820,
            265,
            ["Compound-hazard model chain"],
            size=11.5,
            weight=700,
            fill=COLORS["grey_edge"],
            anchor="start",
        )
    )
    stages = [
        (
            ["Scenario", "exceedance"],
            ["Xᵢ⁽ʳ,ᶠ⁾", "Rainfall load relative", "to retained threshold"],
            COLORS["blue"],
            COLORS["blue_edge"],
        ),
        (
            ["Slope", "disruption"],
            ["Hᵢ⁽ʳ,ᶠ⁾", "Relative landslide", "disruption score"],
            COLORS["amber"],
            COLORS["amber_edge"],
        ),
        (
            ["Road", "disruption"],
            ["Dₑ⁽ʳ,ᶠ⁾", "Upslope transfer to", "each Road Section ID"],
            COLORS["red"],
            COLORS["red_edge"],
        ),
        (
            ["Network", "disruption"],
            ["1,000 closure draws", "Low  |  Central  |  High", "closure mappings"],
            COLORS["purple"],
            COLORS["purple_edge"],
        ),
        (
            ["Community and", "service consequences"],
            ["Isolation frequency", "Total Population exposed", "Service reachability loss"],
            COLORS["red"],
            COLORS["red_edge"],
        ),
        (
            ["Decision", "screening"],
            ["Priority roads and communities", "Action-specific benefit", "Budget and rank robustness"],
            COLORS["green"],
            COLORS["green_edge"],
        ),
    ]
    for x, (heading, body, face, edge) in zip(stage_x, stages):
        elements.append(
            box(
                x,
                stage_y,
                stage_w,
                stage_h,
                heading,
                body,
                face=face,
                edge=edge,
                heading_size=14.5,
                body_size=12.0,
            )
        )
    for left, right in zip(stage_x[:-1], stage_x[1:]):
        elements.append(arrow(f"M {left + stage_w} {stage_y + stage_h / 2} L {right} {stage_y + stage_h / 2}"))

    # Input-to-model connectors use non-crossing Bezier curves.
    elements.extend(
        [
            arrow(
                "M 142.5 165 C 142.5 205, 142.5 245, 142.5 285",
                color=COLORS["blue_edge"],
                marker="arrow-blue",
            ),
            arrow(
                "M 407.5 165 C 407.5 218, 255 225, 195 285",
                color=COLORS["amber_edge"],
                marker="arrow-amber",
            ),
            arrow(
                "M 672.5 165 C 672.5 218, 520 225, 455 285",
                color=COLORS["grey_edge"],
                marker="arrow-slate",
            ),
        ]
    )

    # Validation and quality gates.
    gates = [
        (
            160,
            ["Landslide evidence gate"],
            ["2016 interpreted inventory", "Spatial blocks  |  held-out capture"],
            400,
            COLORS["amber_edge"],
            "arrow-amber",
        ),
        (
            620,
            ["Road evidence gate"],
            ["Observed restrictions", "Reliable matches  |  ranking stability"],
            665,
            COLORS["red_edge"],
            "arrow-red",
        ),
        (
            1080,
            ["Network quality gate"],
            ["Baseline connectivity  |  population", "service attachment  |  convergence"],
            1195,
            COLORS["purple_edge"],
            "arrow-purple",
        ),
    ]
    gate_y = 570
    gate_w = 360
    gate_h = 105
    elements.append(
        multiline_text(
            25,
            550,
            ["Evidence and quality gates"],
            size=11.5,
            weight=700,
            fill=COLORS["grey_edge"],
            anchor="start",
        )
    )
    for x, heading, body, target_x, edge, marker in gates:
        elements.append(
            box(
                x,
                gate_y,
                gate_w,
                gate_h,
                heading,
                body,
                face=COLORS["grey"],
                edge=edge,
                heading_size=13.3,
                body_size=11.8,
                stroke_width=2.0,
            )
        )
        elements.append(
            arrow(
                f"M {x + gate_w / 2} {gate_y} C {x + gate_w / 2} 520, {target_x} 520, {target_x} {stage_y + stage_h}",
                color=edge,
                width=2.2,
                marker=marker,
            )
        )

    # Interpretation limits remain in AnaSOP and the eventual caption, not in the artwork.
    elements.append("</svg>")
    return "\n".join(elements)


def find_chrome() -> Path:
    """Find a local Chromium-family browser suitable for SVG rasterization."""
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    for command in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        resolved = shutil.which(command)
        if resolved:
            candidates.append(Path(resolved))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RuntimeError("No Chrome or Chromium executable was found for SVG-to-PNG conversion.")


def render_png_from_svg() -> None:
    """Rasterize the authoritative SVG and attach 150 dpi metadata."""
    chrome = find_chrome()
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={PNG_WIDTH},{PNG_HEIGHT}",
        f"--screenshot={PNG_PATH}",
        SVG_PATH.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)

    with Image.open(PNG_PATH) as rendered:
        rendered.load()
        if rendered.size != (PNG_WIDTH, PNG_HEIGHT):
            raise RuntimeError(
                f"Unexpected PNG size {rendered.size}; expected {(PNG_WIDTH, PNG_HEIGHT)}."
            )
        output = rendered.convert("RGB")
    output.save(PNG_PATH, format="PNG", dpi=(150, 150), optimize=True)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(build_svg(), encoding="utf-8")
    render_png_from_svg()
    print(f"Saved SVG: {SVG_PATH.relative_to(ROOT)}")
    print(f"Saved PNG: {PNG_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
