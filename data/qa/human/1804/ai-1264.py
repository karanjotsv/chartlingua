import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
    sys.exit(1)

# Get the JSON file path and check for its existence
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)

# Derive the output image filename from the input JSON filename
output_filename = json_file_path.with_suffix(".png")

# Load all chart data and text from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize a Plotly graph objects figure
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
# The data is iterated in order to match the legend and color assignments
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        y=chart_data['categories'],
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        hoverinfo='none'
    ))

# Prepare a list to hold all annotations
annotations = []

# Create and position annotations for the first data series ("Wrong decision")
wrong_decision_values = chart_data['series'][0]['values']
for i, val in enumerate(wrong_decision_values):
    if val is not None:
        annotations.append(dict(
            x=0,
            y=chart_data['categories'][i],
            text=str(val),
            showarrow=False,
            xanchor='right',
            xshift=-5,
            font=dict(color='#333333', size=12, family='Arial')
        ))

# Create and position annotations for the second data series ("Right decision")
right_decision_values = chart_data['series'][1]['values']
cumulative_values = [v1 + v2 if v1 is not None and v2 is not None else 0 for v1, v2 in zip(wrong_decision_values, right_decision_values)]
for i, val in enumerate(right_decision_values):
    if val is not None:
        annotations.append(dict(
            x=cumulative_values[i],
            y=chart_data['categories'][i],
            text=str(val),
            showarrow=False,
            xanchor='left',
            xshift=5,
            font=dict(color='#333333', size=12, family='Arial')
        ))
        
# Add the source and credit text as a single annotation at the bottom
annotations.append(go.layout.Annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.15,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(family="Arial", size=10, color="#666666")
))

# Configure the figure's layout for accurate visual replication
fig.update_layout(
    barmode='stack',
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size:14px;color:#5a5a5a;'>{texts['subtitle']}</span>",
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18, color='black')
    ),
    xaxis=dict(
        visible=False,
        range=[-20, 105] # Provide padding for annotations
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(family='Arial', size=12, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.86,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12),
        traceorder='normal'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=40, b=120, t=140),
    annotations=annotations,
    font=dict(family="Arial")
)

# Generate and save the chart as a high-resolution PNG file
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")