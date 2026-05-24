import sys
import json
import pathlib
import math
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# --- 2. Extract data and settings from JSON ---
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
axis_ranges = chart_data['axis_ranges']

# --- 3. Create the figure object ---
fig = go.Figure()

# --- 4. Add data traces ---
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(color=colors['trace'][i], width=3),
        name=series.get('name', ''),
        showlegend=False
    ))

# --- 5. Configure layout, axes, and annotations ---

# Calculate logarithmic axis ranges
log_x_min = math.log10(axis_ranges['x_primary_min'])
log_x_max = math.log10(axis_ranges['x_primary_max'])
log_y_min = math.log10(axis_ranges['y_primary_min'])
log_y_max = math.log10(axis_ranges['y_primary_max'])

log_x2_min = math.log10(axis_ranges['x_primary_min'] * axis_ranges['x_secondary_conversion'])
log_x2_max = math.log10(axis_ranges['x_primary_max'] * axis_ranges['x_secondary_conversion'])
log_y2_min = math.log10(axis_ranges['y_primary_min'] * axis_ranges['y_secondary_conversion'])
log_y2_max = math.log10(axis_ranges['y_primary_max'] * axis_ranges['y_secondary_conversion'])


fig.update_layout(
    title=dict(
        text=texts['title'],
        font=dict(size=32, color=colors['text']),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12, color=colors['text']),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    margin=dict(l=90, r=90, t=120, b=260),

    # Primary X-Axis (Bottom)
    xaxis=dict(
        title=texts['x_axis_title'],
        type='log',
        range=[log_x_min, log_x_max],
        side='bottom',
        gridcolor=colors['grid'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),

    # Primary Y-Axis (Left)
    yaxis=dict(
        title=dict(text=texts['y_axis_title'], standoff=10),
        type='log',
        range=[log_y_min, log_y_max],
        side='left',
        gridcolor=colors['grid'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),

    # Secondary X-Axis (Top)
    xaxis2=dict(
        title=texts['secondary_x_axis_title'],
        type='log',
        range=[log_x2_min, log_x2_max],
        side='top',
        overlaying='x',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),

    # Secondary Y-Axis (Right)
    yaxis2=dict(
        title=dict(text=texts['secondary_y_axis_title'], standoff=15),
        type='log',
        range=[log_y2_min, log_y2_max],
        side='right',
        overlaying='y',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),

    # Add the caption text block below the chart
    annotations=[
        dict(
            text=texts['caption'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.35, # Position below the x-axis title
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

# --- 6. Output the chart to a PNG file ---
p = pathlib.Path(json_file_path)
output_filename = p.with_suffix(".png")
fig.write_image(str(output_filename), scale=2, width=800, height=800)

print(f"Chart saved to {output_filename}")