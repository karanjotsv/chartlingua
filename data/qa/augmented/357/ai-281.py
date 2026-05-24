import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='auto',
    texttemplate='%{text:.2f}',
    marker_color=colors[0],
    hovertemplate='Year: %{x}<br>GVA: %{y:.2f} billion GBP<extra></extra>'
))

# Update the layout to match the original chart's appearance
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        type='category',
        showgrid=False,
        linecolor='lightgray',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 25],
        tickvals=[0, 5, 10, 15, 20, 25],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom'
        ),
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")