import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series = chart_data['series']

# Create the figure object
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        y=categories,
        x=s['data'],
        name=s['name'],
        orientation='h',
        marker_color=colors[i],
        text=[f"{val}%" for val in s['data']],
        textposition='auto',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=40, t=50, b=120),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        ticksuffix='%',
        range=[0, 95] # Set range to give space for text labels
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        tickmode='linear' # Ensure all category labels are displayed
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    title=dict(
        text=texts.get('title', ''),
        x=0.05,
        xanchor='left'
    ),
)

# Add source annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.28,
        xanchor='right',
        yanchor='bottom',
        font=dict(
            family="Arial",
            size=10,
            color="#666666"
        )
    )

# Determine the output filename from the input JSON path
base_name = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")