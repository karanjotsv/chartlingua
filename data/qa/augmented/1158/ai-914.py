import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load the chart data and configuration from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- 2. Create the Chart Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
# Iterate through the data series in the JSON to create a bar for each
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='outside',
        textfont=dict(family="Arial", size=12)
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=60, r=40, t=40, b=120),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[-7, 7],
        tickvals=[-6, -4, -2, 0, 2, 4, 6],
        ticksuffix='%',
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.5
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")