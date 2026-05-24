import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d.get('category', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise',
    textposition='outside',
    textinfo='label',
    insidetextorientation='radial',
    showlegend=False,
    automargin=True
))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get("source"):
    source_text = f"Source: {texts['source']}"

annotations = []
if source_text:
    annotations.append(
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            align='left'
        )
    )

fig.update_traces(textfont_size=12)

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14
    ),
    margin=dict(l=100, r=100, t=80, b=80),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved as {output_filename}")