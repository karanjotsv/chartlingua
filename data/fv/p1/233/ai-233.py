import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Create and Configure the Chart ---
fig = go.Figure()

# Add data series (lines) to the figure
for i, series in enumerate(chart_info['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(color=chart_info['colors'][i], width=3),
        hoverinfo='none' # Disable hover labels on lines
    ))

# Add annotations for each series
for series in chart_info['chart_data']:
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['annotation_text'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=10,
        font=dict(family="Arial", size=14, color='black'),
        align='left'
    )

# --- 3. Apply Layout and Styling ---
title_text = chart_info['texts']['title']
if chart_info['texts']['source']:
    title_text += f"<br><span style='font-size: 12px;'>{chart_info['texts']['source']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=22)
    ),
    xaxis_title=chart_info['texts']['x_axis_title'],
    yaxis_title=chart_info['texts']['y_axis_title'],
    font=dict(family="Arial", size=16),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=180, t=120, b=80),

    # X-Axis Configuration
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False,
        gridcolor='#D3D3D3',
        tickmode='array',
        tickvals=[3, 6, 9, 12],
        range=[-0.5, 12.5]
    ),

    # Y-Axis Configuration
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        gridcolor='#D3D3D3',
        tickmode='array',
        tickvals=[-4, -3, -2, -1, 0, 1, 2, 3],
        tickformat='.1f',
        range=[-4.1, 3.1]
    )
)

# --- 4. Save the Output ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)