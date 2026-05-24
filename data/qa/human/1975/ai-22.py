import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file specified by command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
chart_texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Prepare data for Plotly ---
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the chart figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text:s}',  # Use space as thousands separator
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

# --- 4. Configure layout and styling ---
fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=120, r=80, t=40, b=80),
    xaxis=dict(
        title=chart_texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.25],  # Auto-adjust range to fit text
        tickformat='s'
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False
    ),
    showlegend=False
)

# Add source annotation
source_text = chart_texts.get('source')
if source_text:
    fig.add_annotation(
        dict(
            x=0.99,
            y=-0.15,
            xref='paper',
            yref='paper',
            text=source_text,
            showarrow=False,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color="#555555")
        )
    )

# --- 5. Output the chart as a PNG file ---
output_filename = f"{json_filepath.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")