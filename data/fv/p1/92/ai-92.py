import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data from the JSON object
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
chart1_data = chart_data['chart1']
chart2_data = chart_data['chart2']

# Create a figure object
fig = go.Figure()

# Add traces for the first chart (1855-1856) on the left subplot
for series in reversed(chart1_data['series']): # Reverse to stack correctly (bottom layer first)
    fig.add_trace(go.Barpolar(
        r=series['data'],
        theta=chart1_data['categories'],
        name=series['name'],
        marker_color=colors[series['name']],
        subplot="polar"
    ))

# Add traces for the second chart (1854-1855) on the right subplot
for series in reversed(chart2_data['series']):
    fig.add_trace(go.Barpolar(
        r=series['data'],
        theta=chart2_data['categories'],
        name=series['name'],
        marker_color=colors[series['name']],
        subplot="polar2"
    ))

# Configure the layout of the figure
fig.update_layout(
    title={
        'text': texts['main_title'],
        'y': 0.98,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    template="plotly_white",
    showlegend=False,
    font_family="Arial",
    width=1200,
    height=800,
    margin=dict(l=50, r=50, t=100, b=220),
    barmode='stack',

    # Configure the left polar subplot
    polar=dict(
        domain=dict(x=[0, 0.45], y=[0.1, 0.9]),
        hole=0,
        radialaxis=dict(
            visible=False,
            showticklabels=False,
            showline=False,
            range=[0, 35] # Set common range for comparison
        ),
        angularaxis=dict(
            direction="clockwise",
            rotation=90,
            tickvals=list(range(12)),
            ticktext=chart1_data['categories'],
            showline=False,
            showticklabels=True
        )
    ),

    # Configure the right polar subplot
    polar2=dict(
        domain=dict(x=[0.55, 1], y=[0.1, 0.9]),
        hole=0,
        radialaxis=dict(
            visible=False,
            showticklabels=False,
            showline=False,
            range=[0, 35] # Set common range for comparison
        ),
        angularaxis=dict(
            direction="clockwise",
            rotation=90,
            tickvals=list(range(12)),
            ticktext=chart2_data['categories'],
            showline=False,
            showticklabels=True
        )
    )
)

# Add annotations for subtitles, description, and source
fig.add_annotation(
    x=0.225, y=0.95, xref="paper", yref="paper",
    text=texts['title2'], showarrow=False,
    font=dict(family="Arial", size=12),
    xanchor='center', yanchor='bottom',
    align='center'
)
fig.add_annotation(
    x=0.775, y=0.95, xref="paper", yref="paper",
    text=texts['title1'], showarrow=False,
    font=dict(family="Arial", size=12),
    xanchor='center', yanchor='bottom',
    align='center'
)
fig.add_annotation(
    x=0, y=-0.1, xref="paper", yref="paper",
    text=texts['description'], showarrow=False,
    font=dict(family="Arial", size=11),
    xanchor='left', yanchor='top',
    align='left'
)
fig.add_annotation(
    x=1.0, y=-0.25, xref="paper", yref="paper",
    text=texts['source'], showarrow=False,
    font=dict(family="Arial", size=10, color="grey"),
    xanchor='right', yanchor='bottom',
    align='right'
)

# Generate the output filename from the input JSON path
output_filename = json_path.stem + ".png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")