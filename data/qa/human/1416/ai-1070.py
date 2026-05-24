import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=80,
    texttemplate="%{value}%<br><b>%{label}</b>",
    textposition='inside',
    textinfo='text',
    insidetextorientation='horizontal',
    hoverinfo='label+percent',
    textfont=dict(
        family="Arial",
        size=16,
        color='black'
    )
))

title_text = f"<b>{texts.get('title', '')}</b><br><i style='color:#444444; font-size:1em;'>{texts.get('subtitle', '')}</i>"
note_text = texts.get('note', '')
source_text = texts.get('source', '')
source_note_text = f"{note_text}<br><b>{source_text}</b>" if note_text and source_text else note_text or f"<b>{source_text}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    width=500,
    height=700,
    margin=dict(l=40, r=40, t=150, b=100),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.05,
            y=0.03,
            xanchor='left',
            yanchor='bottom',
            align='left'
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")