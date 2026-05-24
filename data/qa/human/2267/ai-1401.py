import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and settings from the configuration
series_names = chart_config.get("series_names", [])
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])
categories = [item['category'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series
for i, series_name in enumerate(series_names):
    y_values = [item['values'][i] for item in chart_data]
    text_labels = [f"{v}%" for v in y_values]

    fig.add_trace(go.Bar(
        x=categories,
        y=y_values,
        name=series_name,
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    title_text=texts.get('title'),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 25],
        tickvals=[0, 5, 10, 15, 20, 25],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor='#f0f0f0',
        griddash='dot'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=60, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")