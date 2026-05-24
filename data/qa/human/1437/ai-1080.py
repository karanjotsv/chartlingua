import sys
import json
import plotly.graph_objects as go
import os

# Check if the command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create text for display inside slices, e.g., "Not safe<br>76%"
pie_text = [f"<b>{d['label']}</b><br><b>{d['value']}%</b>" for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=pie_text,
    textinfo='text',
    textfont=dict(
        family='Arial',
        size=22,
        color=colors['slice_text']
    ),
    marker=dict(
        colors=colors['slices'],
        line=dict(color='white', width=1) # Add a thin white line between slices
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    hoverinfo='none'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine note and source for the footer
footer_text = f"{texts['note']}<br><br>{texts['source']}"

# Update layout for a clean and accurate look
fig.update_layout(
    showlegend=False,
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(
            family='Arial',
            size=28,
            color=colors['title']
        ),
        x=0.05,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=40, r=40, t=140, b=220),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    annotations=[
        dict(
            text=footer_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=0.0,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(
                family='Arial',
                size=14
            )
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")