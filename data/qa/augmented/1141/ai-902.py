import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    texttemplate='%{x}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text from being clipped at the axis edge
))

# Create annotations list
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.1, # Position below x-axis title
            xanchor='right',
            yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=50, t=30, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=14),
        tickfont=dict(size=12),
        ticksuffix='%',
        range=[0, max(values) * 1.15], # Set range with padding
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False
    ),
    yaxis=dict(
        autorange='reversed',  # To display categories from top to bottom
        tickfont=dict(size=12)
    ),
    annotations=annotations
)

# Determine output filename from input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")