import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

# Read JSON data
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for plotting
plots_data = config['chart_data']
colors = config['colors']
subplot_titles = [p['title'] for p in plots_data]

# Create subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=subplot_titles,
    horizontal_spacing=0.08,
    vertical_spacing=0.15
)

# Add traces to each subplot
for i, plot in enumerate(plots_data):
    row, col = i // 2 + 1, i % 2 + 1
    for series in plot['series']:
        if series['name'] == 'Actual':
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                line=dict(color=colors['actual'], width=3),
                name=series['name']
            ), row=row, col=col)
        elif series['name'] == 'Trend':
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                line=dict(color=colors['trend'], width=2),
                name=series['name']
            ), row=row, col=col)
        elif series['name'] == 'Target':
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='markers',
                marker=dict(
                    color=colors['target'],
                    symbol='line-ew',
                    size=12,
                    line=dict(width=3)
                ),
                name=series['name']
            ), row=row, col=col)

# Update axes properties
fig.update_xaxes(
    showgrid=True,
    gridcolor='#EEEEEE',
    zeroline=False,
    tickvals=[2014, 2015, 2016, 2017, 2018, 2019],
    range=[2013.7, 2019.3],
    showline=False,
    ticks=''
)

fig.update_yaxes(
    showgrid=True,
    gridcolor='#EEEEEE',
    zeroline=False,
    showline=False,
    ticks=''
)

# Set specific y-axis ranges for each subplot
fig.update_yaxes(range=plots_data[0]['y_range'], row=1, col=1)
fig.update_yaxes(range=plots_data[1]['y_range'], row=1, col=2)
fig.update_yaxes(range=plots_data[2]['y_range'], row=2, col=1)
fig.update_yaxes(range=plots_data[3]['y_range'], row=2, col=2)

# Update overall layout
fig.update_layout(
    width=900,
    height=650,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#444444'),
    margin=dict(l=50, r=20, t=80, b=50),
    showlegend=False
)

# Adjust subplot title alignment and style
for i, annotation in enumerate(fig.layout.annotations):
    xaxis_ref = f'xaxis{i+1}'
    annotation.update(
        x=fig.layout[xaxis_ref].domain[0],
        xanchor='left',
        font=dict(family="Arial", size=16, color='black'),
        align='left'
    )

# Generate output image file name
output_filename = json_path.stem + ".png"

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")