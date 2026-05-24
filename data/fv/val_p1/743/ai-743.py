import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
labels = [item['label'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=labels,
    textposition='outside',
    marker_color=colors,
    cliponaxis=False 
))

# Configure the layout
title_text = f"{texts['subtitle']}<br><b>{texts['title']}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 101],
        tickvals=[i for i in range(0, 101, 10)],
        ticktext=[f"{i}%" for i in range(0, 101, 10)],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=100),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2, # Adjust this value if source note overlaps with x-axis labels
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12)

# Generate output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`).")
    sys.exit(1)