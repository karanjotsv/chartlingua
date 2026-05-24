import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = pathlib.Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    textinfo='percent',
    texttemplate='%{value:.1f}%',
    textfont=dict(family="Arial", size=12, color='white'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    insidetextorientation='horizontal',
))

title_text = f"<b>{texts.get('title', '')}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=16,
            color='black'
        )
    ),
    legend=dict(
        orientation='v',
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        font=dict(
            family="Arial",
            size=12
        )
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=40, r=200, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=800,
    height=550
)

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")