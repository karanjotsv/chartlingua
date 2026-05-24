import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script must be called with the JSON file path as the single command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and configuration from the JSON object
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for plotting. Plotly plots y-axis categories from bottom to top,
# so we reverse the lists to display them from top to bottom as in the original chart.
categories = [d['category'] for d in chart_data][::-1]
values = [d['value'] for d in chart_data][::-1]

# Prepare text labels for bars. The original chart shows a '%' sign only on the top value.
# After reversal, this corresponds to the last item in our `values` list.
text_labels = [str(v) for v in values]
if text_labels:
    text_labels[-1] += '%'

# Create the horizontal bar chart trace
bar_trace = go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    hoverinfo='none',
    width=0.6
)

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px; color:#555555;'>{texts['subtitle']}</span>"

# Combine source and note for the footer annotation
source_text = f"<span style='font-size:10px; color:#555555;'>{texts['source']}</span><br><b style='font-size:11px'>{texts['note']}</b>"

# Configure the chart layout
layout = go.Layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, max(values) * 1.18]  # Add padding for text labels on the right
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=220, r=40, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=-0.12,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Create the figure object
fig = go.Figure(data=[bar_trace], layout=layout)

# Generate the output PNG filename from the input JSON filename stem
output_filename = Path(json_path).stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)