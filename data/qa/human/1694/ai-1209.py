import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['data'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=[f"{val}%" for val in series['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14, family='Arial')
    ))

# Combine title and subtitle
title_text = f"<b style='font-size: 24px;'>{texts['title']}</b><br><span style='font-size: 16px; color:#555555'>{texts['subtitle']}</span>"

# Combine source and footer notes
source_footer_text = f"{texts['source']}<br><br><b>{texts['footer']}</b>"

# Create annotations for the custom legend on top of the first bar
annotations = []
first_bar_y_index = len(categories) - 1
bad_value = series_data[0]['data'][first_bar_y_index]
good_value = series_data[1]['data'][first_bar_y_index]

annotations.append(dict(
    x=bad_value / 2,
    y=first_bar_y_index,
    text=f"<b>{series_data[0]['name']}</b>",
    showarrow=False,
    font=dict(family='Arial', size=14, color='#333333'),
    yshift=25
))
annotations.append(dict(
    x=bad_value + (good_value / 2),
    y=first_bar_y_index,
    text=f"<b>{series_data[1]['name']}</b>",
    showarrow=False,
    font=dict(family='Arial', size=14, color='#333333'),
    yshift=25
))

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0, 101] # Percentages sum up to ~100
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=14, family='Arial')
    ),
    annotations=[
        # Source and footer note
        dict(
            text=source_footer_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family='Arial', size=12, color='#555555')
        )
    ] + annotations,
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=100, r=40, t=150, b=200) # Increased bottom margin for source
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")