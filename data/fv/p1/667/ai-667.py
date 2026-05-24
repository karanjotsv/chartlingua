import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and text from the JSON object
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
text_labels = [f"{v}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=16,
        color='black'
    )
))

# Update layout for a clean and accurate appearance
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(
            family="Arial",
            size=14,
            color='black'
        )
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        visible=False, # Hide y-axis line, ticks, labels, and gridlines
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=120, b=100) # Adjust margins for title and labels
)

# Determine the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png').name

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")