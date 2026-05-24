import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_file_path}'")
    sys.exit(1)

# Prepare data for Plotly
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create labels and values for the pie chart
values = [d['value'] for d in chart_data]

# The label for the "Don't know/Refused" slice will be handled by an annotation.
# We create custom text for the other slices to include the percentage.
pie_labels = [chart_data[0]['label'], chart_data[1]['label'], '']
pie_text = [
    f"<b>{chart_data[0]['label']}</b><br>{chart_data[0]['value']}%",
    f"<b>{chart_data[1]['label']}</b><br>{chart_data[1]['value']}%",
    f"{chart_data[2]['value']}%"
]

# Create the pie chart trace
trace = go.Pie(
    labels=pie_labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    text=pie_text,
    textinfo='text',
    textposition=['inside', 'inside', 'none'],
    textfont=dict(color='white', size=14),
    sort=False,
    direction='counterclockwise',
    rotation=90,
    pull=[0, 0, 0.05]
)

# Create the figure
fig = go.Figure(data=[trace])

# Update layout
fig.update_layout(
    title=dict(
        text=f"{texts['title']}<br><br>{texts['subtitle']}",
        font=dict(family="Arial", size=16, color="black"),
        y=0.98,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=40, r=40, t=220, b=100),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align="left",
            font=dict(family="Arial", size=12, color="grey")
        ),
        dict(
            text=f"<b>Don't<br>know/<br>Refused<br>(VOL)</b>",
            align='left',
            showarrow=True,
            xref="paper",
            yref="paper",
            x=0.24, # Arrow tip x-coordinate
            y=0.4,  # Arrow tip y-coordinate
            ax=-50, # Text x-offset from tip
            ay=-60, # Text y-offset from tip
            arrowhead=7,
            arrowsize=1.2,
            arrowwidth=1.5,
            arrowcolor='black',
            font=dict(family="Arial", size=14, color="black")
        )
    ]
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")