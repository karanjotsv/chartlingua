import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON specified by command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 2. Create Plotly Figure ---
fig = go.Figure()

# --- 3. Add Data Traces ---
# Iterate through each data series in the JSON and add it to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=series['y'],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Prevents text labels at the top from being clipped
    ))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich text formatting
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12),
        linecolor='#E0E0E0',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        range=[0, 305],
        tickvals=[0, 50, 100, 150, 200, 250, 300],
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    # Add source text as an annotation at the bottom-right
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.18,
            xanchor='right', yanchor='top',
            font=dict(size=10, color='#666666')
        )
    ]
)

# --- 5. Output Chart as PNG ---
output_filename_base = json_path.stem
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")