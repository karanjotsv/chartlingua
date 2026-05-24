import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the JSON object
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(
            color=colors['series'][i],
            width=4,
            shape=series.get('line_shape', 'linear'),
            smoothing=1.3 if series.get('line_shape') == 'spline' else 0
        ),
        marker=dict(
            color=colors['series'][i],
            size=12,
            symbol='circle'
        ),
        hoverinfo='none'
    ))

# Combine title and subtitle using HTML
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 18px; color:{colors.get('subtitle', '#666666')};'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=14),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24, color=colors.get('title', '#333333'))
    ),
    margin=dict(l=50, r=180, t=120, b=40),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[min(data_series[0]['x']) - 0.5, max(data_series[0]['x']) + 0.8]
    ),
    yaxis=dict(
        autorange='reversed',
        range=[6.5, 0.5],
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        showline=False,
        zeroline=False,
        tickvals=[1, 2, 3, 4, 5, 6],
        tickfont=dict(color=colors['axes_labels'], size=16),
        title_text=texts.get('y_axis_title')
    )
)

# Add annotations for years at the top
years = data_series[0]['x']
for year in years:
    fig.add_annotation(
        x=year,
        y=0.5,
        yref='y',
        text=f"<b>{year}</b>",
        showarrow=False,
        font=dict(color=colors['axes_labels'], size=18),
        yanchor='bottom',
        yshift=10
    )

# Add annotations for series labels at the end of the lines
for i, series in enumerate(data_series):
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=f"<b>{series['label']}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=20,
        font=dict(family="Arial", size=14, color='#000000')
    )

# Define output filename
output_filename = json_file_path.with_suffix(".png")

# Write the image file
fig.write_image(output_filename, scale=2, width=800, height=500)

print(f"Chart saved to {output_filename}")