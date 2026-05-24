import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
series_names = chart_info['series_names']
texts = chart_info['texts']
colors = chart_info['colors']
categories = [d['category'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series_name in enumerate(series_names):
    x_values = [d['values'][i] for d in chart_data]
    text_labels = [d['labels'][i] for d in chart_data]
    fig.add_trace(go.Bar(
        y=categories,
        x=x_values,
        name=series_name,
        orientation='h',
        marker_color=colors[i],
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=18, weight='bold'),
        hoverinfo='none'
    ))

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 15px;'>{texts['subtitle']}</span>"

# Combine note, source, and footer using HTML
source_text = f"{texts['note']}<br>{texts['source']}<br><br><b>{texts['footer']}</b>"

# Update layout for a clean, publication-ready appearance
fig.update_layout(
    barmode='stack',
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        font=dict(size=20),
        x=0.01,
        y=0.96,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        visible=False,
        range=[0, 100]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed',
        tickfont=dict(size=14, weight='bold')
    ),
    margin=dict(l=120, r=20, t=180, b=220),
    annotations=[] # Initialize list for custom text
)

# Add annotations for column headers above the bars
header_y_position = 1.08
# Calculate center position for the first bar segment
x_pos1 = chart_data[0]['values'][0] / 2
fig.add_annotation(
    x=x_pos1,
    y=header_y_position,
    yref='paper',
    text=f"<b>{series_names[0]}</b>",
    showarrow=False,
    font=dict(size=14),
    xanchor='center',
    yanchor='bottom',
    align='center'
)
# Calculate center position for the second bar segment
x_pos2 = chart_data[0]['values'][0] + (chart_data[0]['values'][1] / 2)
fig.add_annotation(
    x=x_pos2,
    y=header_y_position,
    yref='paper',
    text=f"<b>{series_names[1]}</b>",
    showarrow=False,
    font=dict(size=14),
    xanchor='center',
    yanchor='bottom',
    align='center'
)

# Add a single annotation for the note, source, and footer at the bottom
fig.add_annotation(
    xref='paper', yref='paper',
    x=0, y=-0.25,
    text=source_text,
    showarrow=False,
    align='left',
    xanchor='left',
    yanchor='top',
    font=dict(size=11)
)

# Generate the output PNG file
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")