import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
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

# Extract data and text from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
x_values = [str(d['x']) for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Initialize a Plotly Figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    texttemplate='%{text:,}', # Format text with comma separators
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12
    )
))

# Update the layout of the chart for a professional and accurate look
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=50, r=40, b=80, l=100),
    yaxis=dict(
        title=texts.get('yaxis_title'),
        range=[0, 6100],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('xaxis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    )
)

# Add source annotation if it exists in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=10, color="#888888")
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved successfully to {output_filename}")