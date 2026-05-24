import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config["chart_data"]
texts = config["texts"]
colors = config["colors"]
settings = config["special_settings"]

categories = [d["category"] for d in chart_data]
values = [d["value"] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors["bars"],
    hoverinfo="none",
    width=0.75
))

annotations = []
highlight_cat = settings["highlight_category"]
try:
    highlight_idx = categories.index(highlight_cat)
    annotations.append(go.layout.Annotation(
        x=highlight_cat,
        y=values[highlight_idx],
        text=f"{values[highlight_idx]:.1f}",
        showarrow=False,
        font=dict(color=colors["special_category_color"], size=12, family="Arial"),
        yshift=10
    ))
except ValueError:
    pass

annotation_cat = settings["annotation_category"]
try:
    annotation_idx = categories.index(annotation_cat)
    annotations.append(go.layout.Annotation(
        x=annotation_cat,
        y=values[annotation_idx],
        text=texts["usa_annotation"],
        showarrow=True,
        arrowhead=6,
        arrowcolor="#BFBFBF",
        ax=-60,
        ay=-30,
        bordercolor="#BFBFBF",
        borderwidth=1,
        bgcolor="#FFFFFF",
        align="left"
    ))
except ValueError:
    pass

annotations.append(go.layout.Annotation(
    text=texts["source"],
    xref="paper", yref="paper",
    x=0.99, y=0.99,
    showarrow=False,
    xanchor="right", yanchor="top",
    font=dict(family="Arial", size=12)
))

tick_texts = [
    f"<span style='color:{colors['special_category_color']}'>{cat}</span>" if cat == highlight_cat else cat
    for cat in categories
]

title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px;color:#555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    font_family="Arial",
    title=dict(text=title_text, x=0.01, y=0.97, xanchor='left', yanchor='top'),
    xaxis=dict(
        tickvals=categories,
        ticktext=tick_texts,
        tickangle=-45,
        linecolor='rgba(0,0,0,0)',
        tickfont_size=12
    ),
    yaxis=dict(
        range=[0, 100],
        gridcolor=colors["grid"],
        zeroline=False,
        showline=False
    ),
    plot_bgcolor=colors["plot_bg"],
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=100, b=80),
    annotations=annotations,
    shapes=[dict(
        type="line", xref="paper", yref="paper",
        x0=0, x1=1, y0=0.9, y1=0.9,
        line=dict(color=colors["title_line"], width=2)
    )]
)

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")