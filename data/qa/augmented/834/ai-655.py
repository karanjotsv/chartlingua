import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
formatted_texts = [f"{v:,}".replace(',', ' ') for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=formatted_texts,
    textposition='outside',
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 8000],
        tickvals=[i for i in range(0, 9000, 1000)],
        ticktext=[f"{i:,}".replace(',', ' ') for i in range(0, 9000, 1000)],
        gridcolor='lightgrey',
        zeroline=False,
        linecolor='lightgrey'
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Style text on bars
fig.update_traces(
    textfont_size=12,
    textfont_color='black'
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")