import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare data for Plotly ---
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_text = [f"{v}%" for v in values]

# --- 3. Create the chart figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else '#357ABD',
    text=bar_text,
    textposition='outside',
    cliponaxis=False,
    insidetextanchor='start', # Not used, but good practice
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# --- 4. Configure layout and styling ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=150, r=60, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 230],
        dtick=25,
        ticksuffix='%'
    ),
    yaxis=dict(
        autorange="reversed", # Puts the first category at the top
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='black'
    ),
    showlegend=False
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=1, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12, color='#666666')
    )

# --- 5. Output the chart as a PNG image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")