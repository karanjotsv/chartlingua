import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_image_path = json_file_path.with_suffix('.png')

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Data Extraction ---
chart_data = config["chart_data"]
texts = config["texts"]
colors = config["colors"]

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_color = colors[0] if colors else '#2772DB'

# --- 3. Chart Creation ---
fig = go.Figure()

# Add Bar Trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_color,
    width=0.6
))

# --- 4. Layout and Styling ---
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')

if title_text and subtitle_text:
    combined_title = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
elif title_text:
    combined_title = f"<b>{title_text}</b>"
else:
    combined_title = None

annotations = []

# Add data labels
for i, item in enumerate(chart_data):
    annotations.append(
        dict(
            x=item['category'],
            y=item['value'],
            text=f"{item['value']}%",
            showarrow=False,
            font=dict(family="Arial", size=14, color="black"),
            xanchor='center',
            yanchor='bottom',
            yshift= -30 # Position inside the bar from the top
        )
    )

# Add source text
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='grey')
        )
    )

fig.update_layout(
    title_text=combined_title,
    title_x=0.05,
    title_font=dict(family="Arial", size=20),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=2,
        linecolor='black',
        tickfont=dict(family="Arial", size=14)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 750],
        tickvals=[i * 100 for i in range(8)],
        ticktext=[f"{i * 100}%" for i in range(8)],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        title_font=dict(family="Arial", size=14),
        tickfont=dict(family="Arial", size=14),
    ),
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# --- 5. Output ---
fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")