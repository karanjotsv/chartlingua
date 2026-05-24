import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding
if not pathlib.Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False # Allows text to render outside the plot area
))

# Update layout for a clean and accurate representation
fig.update_layout(
    font_family="Arial",
    font_size=12,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis=dict(
        range=[0, 400],
        gridcolor='#E5E5E5',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2, # Position below x-axis
            xanchor='left',
            yanchor='top'
        )
    ]
)

# Customize text on bars
fig.update_traces(texttemplate='%{y}', textfont_size=12)

# Generate the output image filename from the input JSON path
output_base_name = pathlib.Path(json_path).stem
output_filename = f"{output_base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")