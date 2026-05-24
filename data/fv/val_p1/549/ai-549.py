import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract Data and Texts ---
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# --- 3. Create the Chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # This is crucial to maintain the original order
    direction='clockwise'
))

# --- 4. Configure Layout ---
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=100, b=100),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top'
    )


# --- 5. Save the Output ---
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")