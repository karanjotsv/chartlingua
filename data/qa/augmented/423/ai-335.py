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

# Extract data and texts from the JSON structure
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the bar chart trace
trace = go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:,}'.replace(',', ' ') if v is not None else '' for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
)

# Create the figure
fig = go.Figure(data=[trace])

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title_text=texts['title'] if texts.get('title') else None,
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        range=[0, 150000],
        tickvals=[0, 25000, 50000, 75000, 100000, 125000, 150000],
        ticktext=['0', '25 000', '50 000', '75 000', '100 000', '125 000', '150 000'],
        tickfont=dict(size=12)
    ),
    margin=dict(l=100, r=30, t=50, b=120),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='#0073e6')
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12)
        )
    ]
)

# Update text angle for values on bars to prevent overlap if needed (not needed here)
fig.update_traces(textangle=0)


# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")