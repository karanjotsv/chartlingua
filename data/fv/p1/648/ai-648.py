import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and configuration from the JSON object
data_series = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize a Plotly figure
fig = go.Figure()

# Iterate through the data series in the JSON to create chart traces
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x_values'],
        y=series['y_values'],
        mode='lines+markers',
        name=series['name'],
        line=dict(
            color=colors['lines'][i],
            width=4,
            shape=series['line_shape'],
            smoothing=0.7 if series['line_shape'] == 'spline' else 1.3
        ),
        marker=dict(
            color=colors['lines'][i],
            size=12,
            symbol='circle'
        ),
        hoverinfo='none'
    ))

# Add annotations for the labels at the end of each line
for series in data_series:
    fig.add_annotation(
        x=series['x_values'][-1],
        y=series['y_values'][-1],
        text=f"<b>{series['end_label']}</b>",
        showarrow=False,
        font=dict(
            family="Arial",
            size=14,
            color="#000000"
        ),
        xanchor='left',
        xshift=20,
        yanchor='middle'
    )

# Construct the title using HTML for styling
title_text = (
    f"<b style='font-size: 26px;'>{texts['title']}</b>"
    f"<br><span style='font-size: 18px; color:{colors['subtitle']};'>{texts['subtitle']}</span>"
)
x_axis_categories = data_series[0]['x_values']

# Update the figure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        visible=False,
        range=[-0.2, len(x_axis_categories) - 1 + 0.5] # Add padding for annotations
    ),
    xaxis2=dict(
        overlaying='x',
        side='top',
        tickvals=x_axis_categories,
        ticktext=[f"<b>{year}</b>" for year in x_axis_categories],
        tickfont=dict(
            family="Arial",
            size=18,
            color=colors['axes_labels']
        ),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        autorange='reversed',
        tickvals=[1, 2, 3, 4, 5, 6],
        ticktext=[f"<b>{i}</b>" for i in [1, 2, 3, 4, 5, 6]],
        tickfont=dict(
            family="Arial",
            size=18,
            color=colors['axes_labels']
        ),
        showgrid=True,
        gridcolor=colors['grid'],
        zeroline=False,
        showline=False,
        title_text="",
        range=[6.5, 0.5] # Inverted range with padding
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=150, t=120, b=40),
    font=dict(family="Arial")
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")