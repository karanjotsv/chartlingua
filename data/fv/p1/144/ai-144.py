import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires plotly and kaleido to be installed:
# pip install plotly kaleido

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

filename_base = pathlib.Path(json_path).stem

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,
    textinfo='none',
    hole=0,
    domain={'x': [0, 0.7]}  # Allocate space on the right for the legend
))

# Construct title
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine note and source for a single annotation block
source_note_parts = []
if texts.get('note') and texts['note'].strip():
    source_note_parts.append(texts['note'])
if texts.get('source') and texts['source'].strip():
    source_note_parts.append(texts['source'])
source_note_text = "<br><br>".join(source_note_parts)

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.72,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor="Black",
        borderwidth=1
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='#FFFFFF',
    margin=dict(l=40, r=40, t=80, b=220),  # Increased bottom margin for text
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10)
        )
    ]
)

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")