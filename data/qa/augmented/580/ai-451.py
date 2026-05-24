import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Load all chart data and settings from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Extract data for plotting
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]
text_labels = [item['text'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12),
        categoryorder='array',
        categoryarray=x_values
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False,
        range=[0, 180],
        tickvals=[0, 25, 50, 75, 100, 125, 150, 175]
    ),
    margin=dict(l=90, r=20, t=30, b=100)
)

# Add source annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='top',
        font=dict(size=12)
    )

# Save the generated chart to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully saved to {output_filename}")