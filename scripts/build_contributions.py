"""Build assets/contributions.svg: a ship that shoots the contribution calendar into view.

The calendar starts as empty outlines. A ship crosses under it from left to
right and fires a beam at every column that has activity; each hit cell then
stays lit until the loop restarts.

Usage:
    GITHUB_TOKEN=... python scripts/build_contributions.py <login> [output.svg]

Standard library only.
"""

import json
import os
import sys
import urllib.request
from datetime import date

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel weekday } }
      }
    }
  }
}
"""

# Geometry
WIDTH, HEIGHT = 1200, 280
CELL, PITCH = 13, 17
GRID_TOP = 72
SHIP_Y = 236          # ship centre; its nose sits 14 px above
NOSE_Y = SHIP_Y - 14

# Timeline, in seconds
LOOP = 18.0
SWEEP_START = 1.0
PER_COLUMN = 0.2
BEAM_LIFE = 0.16
FADE_START, FADE_END = 16.4, 17.2

LEVEL_OPACITY = {
    "FIRST_QUARTILE": 0.35,
    "SECOND_QUARTILE": 0.55,
    "THIRD_QUARTILE": 0.78,
    "FOURTH_QUARTILE": 1.0,
}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fetch_calendar(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "User-Agent": "contribution-svg"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def k(seconds: float) -> str:
    """A time on the loop as a keyTimes fraction."""
    return f"{seconds / LOOP:.4f}"


def build_svg(calendar: dict) -> str:
    weeks = calendar["weeks"]
    columns = len(weeks)
    grid_width = columns * PITCH - (PITCH - CELL)
    left = (WIDTH - grid_width) / 2

    def column_x(c: int) -> float:
        return left + c * PITCH + CELL / 2

    outlines, cells, beams, labels = [], [], [], []
    previous_month = None

    for c, week in enumerate(weeks):
        hit_time = SWEEP_START + c * PER_COLUMN
        top_active_row = None

        first_day = date.fromisoformat(week["contributionDays"][0]["date"])
        if first_day.month != previous_month:
            if previous_month is not None or first_day.day <= 7:
                labels.append(
                    f'<text class="lbl" x="{left + c * PITCH:.1f}" y="{GRID_TOP - 12}">'
                    f"{MONTHS[first_day.month - 1]}</text>"
                )
            previous_month = first_day.month

        for day in week["contributionDays"]:
            row = day["weekday"]
            x = left + c * PITCH
            y = GRID_TOP + row * PITCH
            outlines.append(f'<rect x="{x:.1f}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5"/>')

            if day["contributionCount"] == 0:
                continue
            if top_active_row is None or row < top_active_row:
                top_active_row = row

            # Lower rows are closer to the ship, so they light up first.
            lit = hit_time + (6 - row) * 0.018
            opacity = LEVEL_OPACITY.get(day["contributionLevel"], 0.35)
            count = day["contributionCount"]
            noun = "contribution" if count == 1 else "contributions"
            cells.append(
                f'<rect class="hit" x="{x:.1f}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill-opacity="{opacity}" opacity="0">'
                f"<title>{day['date']}: {count} {noun}</title>"
                f'<animate attributeName="opacity" dur="{LOOP}s" repeatCount="indefinite" '
                f'values="0;0;1;1;0;0" '
                f'keyTimes="0;{k(lit)};{k(lit + 0.05)};{k(FADE_START)};{k(FADE_END)};1"/>'
                f"</rect>"
            )

        if top_active_row is not None:
            x = column_x(c)
            target_y = GRID_TOP + top_active_row * PITCH + CELL / 2
            beams.append(
                f'<line class="beam" x1="{x:.1f}" y1="{NOSE_Y}" x2="{x:.1f}" y2="{target_y:.1f}" opacity="0">'
                f'<animate attributeName="opacity" dur="{LOOP}s" repeatCount="indefinite" '
                f'values="0;0;1;0;0" '
                f'keyTimes="0;{k(hit_time - 0.01)};{k(hit_time)};{k(hit_time + BEAM_LIFE)};1"/>'
                f"</line>"
            )

    sweep_end = SWEEP_START + (columns - 1) * PER_COLUMN
    ship_path = (
        f"-40 {SHIP_Y};{column_x(0):.1f} {SHIP_Y};{column_x(columns - 1):.1f} {SHIP_Y};"
        f"{WIDTH + 40} {SHIP_Y};{WIDTH + 40} {SHIP_Y}"
    )
    ship_times = f"0;{k(SWEEP_START)};{k(sweep_end)};{k(sweep_end + 1.4)};1"

    weekday_labels = "".join(
        f'<text class="lbl" x="{left - 10:.1f}" y="{GRID_TOP + row * PITCH + 10.5}" text-anchor="end">{name}</text>'
        for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" role="img" aria-label="Contribution calendar for the last year. A ship fires at the calendar and each active day lights up.">
  <style>
    :root {{ --ink: #1f2328; --mute: #656d76; --line: #d0d7de; --acc: #cf4a12; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --ink: #e6edf3; --mute: #8b949e; --line: #30363d; --acc: #ff6b2c; }}
    }}
    text {{ font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }}
    .head {{ fill: var(--ink); font-size: 13px; letter-spacing: 1.5px; }}
    .lbl {{ fill: var(--mute); font-size: 11px; }}
    .grid rect {{ fill: none; stroke: var(--line); stroke-width: 1; }}
    .hit {{ fill: var(--acc); }}
    .beam {{ stroke: var(--acc); stroke-width: 2; stroke-linecap: round; }}
    .hull {{ fill: var(--ink); }}
    .flame {{ fill: var(--acc); animation: burn .18s steps(2, start) infinite; }}
    @keyframes burn {{ to {{ opacity: .35; }} }}
  </style>

  <text class="head" x="{left:.1f}" y="30">CONTRIBUTIONS / LAST 12 MONTHS</text>

  {"".join(labels)}
  {weekday_labels}
  <g class="grid">{"".join(outlines)}</g>
  <g>{"".join(beams)}</g>
  <g>{"".join(cells)}</g>

  <g>
    <animateTransform attributeName="transform" type="translate" dur="{LOOP}s" repeatCount="indefinite"
      values="{ship_path}" keyTimes="{ship_times}"/>
    <polygon class="flame" points="-3,7 0,17 3,7"/>
    <polygon class="hull" points="0,-14 4,-3 12,7 5,4 0,8 -5,4 -12,7 -4,-3"/>
  </g>
</svg>
"""


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    login = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "assets/contributions.svg"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set.")

    svg = build_svg(fetch_calendar(login, token))
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(svg)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
