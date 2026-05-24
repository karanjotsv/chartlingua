import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#000000'),
    showlegend=False
))

title_parts = []
if texts.get("title"):
    title_parts.append(texts["title"])
if texts.get("subtitle"):
    title_parts.append(f"<br><sub>{texts['subtitle']}</sub>")
final_title_text = "".join(title_parts)

source_note_parts = []
if texts.get("source"):
    source_note_parts.append(texts["source"])
if texts.get("note"):
    source_note_parts.append(texts["note"])
final_source_note_text = "<br>".join(source_note_parts)

fig.update_layout(
    title=dict(
        text=final_title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#CCCCCC',
        zeroline=False,
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        ticks='outside'
    ),
    plot_bgcolor='#F0F0F0',
    paper_bgcolor='#F0F0F0',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    showlegend=False,
    margin=dict(l=50, r=30, t=80, b=80),
    annotations=[
        dict(
            text=final_source_note_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            align='left'
        )
    ] if final_source_note_text else []
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")