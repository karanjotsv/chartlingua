import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for the pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Generate custom text labels as seen in the image
custom_labels = []
for item in chart_data:
    # The 'Other' category has a different prefix in the original image
    if item['category'] == 'Other':
        custom_labels.append(f"· {item['category']} {item['value']}%")
    else:
        custom_labels.append(f"- {item['category']} {item['value']}%")

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    text=custom_labels,
    textinfo='text',
    textposition='outside',
    sort=False, # Preserve the order from the JSON file
    direction='clockwise',
    hoverinfo='label+percent',
    textfont=dict(size=14, family="Arial")
)

# Create the layout
layout = go.Layout(
    title=texts.get('title'),
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=80, t=50, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Create the figure
fig = go.Figure(data=[pie_trace], layout=layout)

# Add source note as an annotation if it exists
if texts.get('source_note'):
    fig.add_annotation(
        text=texts['source_note'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=0.01,
        font=dict(family="Arial", size=10, color="grey")
    )

# Determine the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")