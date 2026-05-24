import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Resolve the input file path
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series from the JSON data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5)
    ))

# Prepare annotations for series labels, placed next to the last data point
annotations = []
for i, series in enumerate(chart_data):
    if series['x'] and series['y']:
        annotations.append(dict(
            x=series['x'][-1],
            y=series['y'][-1],
            text=series['name'],
            showarrow=True,
            arrowhead=0,
            arrowcolor="#636363",
            ax=40,
            ay=0,
            xanchor="left",
            yanchor="middle",
            font=dict(family="Arial", size=12),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#cccccc",
            borderwidth=1,
            borderpad=4
        ))

# Add the source text as an annotation at the top right
if texts.get('source'):
    annotations.append(dict(
        x=1,
        y=1.05,
        xref='paper',
        yref='paper',
        xanchor='right',
        yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#555555")
    ))

# Combine title and subtitle using HTML for rich formatting
title_text = f"<b>{texts['title']}</b><span style='font-size: 0.8em; color: #555555;'>  {texts['subtitle']}</span>"

# Apply layout settings to match the original chart's appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    plot_bgcolor='#EBF2F8',
    paper_bgcolor='white',
    margin=dict(l=40, r=120, t=100, b=50),
    xaxis=dict(
        tickvals=[1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006],
        showgrid=False,
        showline=True,
        linecolor='darkgray',
        zeroline=False,
        ticks='outside',
        tickcolor='darkgray',
    ),
    yaxis=dict(
        range=[2.5, 11.8],
        showgrid=True,
        gridcolor='white',
        gridwidth=2,
        showline=False,
        zeroline=False,
        ticks='',
        tickcolor='darkgray'
    ),
    annotations=annotations
)

# Add a shape to create the top border line of the plot area
fig.add_shape(
    type="line",
    xref="paper", yref="y domain",
    x0=0, y0=1, x1=1, y1=1,
    line=dict(color="darkgray", width=1)
)

# Generate the output PNG filename from the input JSON filename
output_filename = f"{json_path.stem}.png"

# Save the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")