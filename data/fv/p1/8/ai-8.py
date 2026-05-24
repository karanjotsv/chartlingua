import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# --- 2. Create Plotly Figure ---
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    marker_symbol = 'square' if series.get('name') == 'H2' else 'diamond-open'
    marker_size = 8 if series.get('name') == 'H2' else 5

    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, symbol=marker_symbol, size=marker_size)
    ))

# --- 3. Configure Layout ---
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[200, 4200],
        tickvals=[500, 800, 1100, 1400, 1700, 2000, 2300, 2600, 2900, 3200, 3500, 3800, 4100],
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-20000, 90000],
        tickvals=[-20000, -10000, 0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000],
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=120) # Increased bottom margin for legend
)

# --- 4. Output image ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")