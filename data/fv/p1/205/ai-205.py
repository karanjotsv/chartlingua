import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)


# Extract data and texts
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

fig = go.Figure()

# Add traces by iterating through the chart data
for i, series in enumerate(chart_data):
    series_name = series.get('name', '')
    color = colors[i] if i < len(colors) else '#000000'

    if series_name == "Median daily statistic (45 years)":
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series_name,
            mode='markers',
            marker=dict(
                symbol='triangle-up',
                size=10,
                color='#FFD700',  # Fill color
                line=dict(
                    color=color,  # Outline color from JSON
                    width=1.5
                )
            )
        ))
    elif series_name == "Period of approved data":
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series_name,
            mode='lines',
            line=dict(color=color, width=10)
        ))
    elif series_name == "Discharge":
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series_name,
            mode='lines',
            line=dict(color=color, width=1.5)
        ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(family="Arial", size=16, color='black')
    ),
    yaxis_title=texts.get('y_axis_title'),
    yaxis=dict(
        type='log',
        tickvals=[2.0, 10.0, 100.0, 1000.0, 2000.0],
        ticktext=['2.0', '10.0', '100.0', '1000.0', '2000.0'],
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickformat='%b<br>%d<br>%Y',
        dtick='D1',
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=150),
    width=700,
    height=500
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")