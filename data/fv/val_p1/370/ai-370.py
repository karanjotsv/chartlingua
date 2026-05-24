import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and decode the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and text from the JSON structure
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for Plotly trace
x_values = [item['category'] for item in data]
y_values = [item['value'] for item in data]

# Initialize a Plotly Figure
fig = go.Figure()

# Add the bar chart trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none',
    cliponaxis=False  # Prevent data labels from being clipped
))

# Combine title and subtitle using HTML for styling
title_text = f"<b><span style='font-size: 26px; color: #D35400;'>{texts['title']}</span></b><br><span style='font-size: 18px; color: #D35400;'>{texts['subtitle']}</span>"

# Configure the chart layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='grey',
        linewidth=1,
        tickfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ),
    yaxis=dict(
        visible=False,
        range=[0, max(y_values) * 1.18]  # Add padding for the highest data label
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=120, b=80, l=40, r=40),
    font=dict(
        family="Arial"
    )
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")