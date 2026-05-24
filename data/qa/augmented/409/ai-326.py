import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

# --- 2. Extract data and texts ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to match the visual order (Plotly plots from bottom to top)
categories.reverse()
values.reverse()

# --- 3. Create the chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# --- 4. Configure Layout ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=240, r=40, t=30, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.18],  # Add padding for text labels
        tickvals=[i for i in range(0, 50, 5)]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    showlegend=False
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.12,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12)
    )

# --- 5. Output the image ---
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)