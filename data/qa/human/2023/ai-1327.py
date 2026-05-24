import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for the chart
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly Pie chart
# The original chart shows "Label Value%" as text outside the pie.
# A standard Plotly legend is the most robust way to replicate this information.
# We format the labels for the legend to match the original text.
labels_for_legend = [f"{item['label']} {item['value']}%" for item in data]
values = [item['value'] for item in data]
labels_for_pie = [item['label'] for item in data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels_for_legend,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='percent',
    insidetextorientation='radial',
    hovertemplate='%{customdata}<br>%{value}%<extra></extra>',
    customdata=labels_for_pie
)])

# Update layout
annotations = []
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.1,
            xanchor='left',
            yanchor='top'
        )
    )
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.1,
            xanchor='right',
            yanchor='top'
        )
    )

fig.update_layout(
    showlegend=False, # The labels are outside the pie
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=80, r=80, t=50, b=80),
    annotations=annotations,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.update_traces(
    textposition='outside',
    texttemplate='%{label}',
    pull=[0.02] * len(labels_for_legend) # slight pull for better label visibility
)


# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")