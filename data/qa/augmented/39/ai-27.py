import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_filepath} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_filepath} is not a valid JSON.")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
y_categories = [item['category'] for item in chart_data]
x_values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=x_values,
    textposition='outside',
    cliponaxis=False,  # Allow text to be drawn outside the plot area
    textfont=dict(family='Arial', size=12, color='black')
))

# Configure layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        range=[0, max(x_values) * 1.15],  # Add padding for outside text
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        autorange='reversed',  # To display data from top to bottom
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=120, r=40, t=30, b=80),  # Adjust margins for labels
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family='Arial', size=12, color='#666666')
        )
    ]
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")