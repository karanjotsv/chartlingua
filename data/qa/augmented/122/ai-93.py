import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_filename_base = json_file_path.stem

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# --- 2. Create the Chart ---
fig = go.Figure()

# Add a trace for each data series, preserving the order from the JSON
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=series['data'],
        textposition='inside',
        texttemplate='%{text}',
        textfont=dict(color='white', family='Arial', size=14)
    ))

# --- 3. Configure Layout and Styling ---
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        range=[0, 60000],
        tickformat=' ' # Use space as thousands separator
    ),
    xaxis=dict(
        showgrid=False,
        ticks='outside',
        ticklen=5
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    # Add annotation for the source text
    annotations=[
        dict(
            showarrow=False,
            text=f"{texts['source']} &nbsp;&nbsp; {texts['note']}",
            xref='paper',
            yref='paper',
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# --- 4. Output the Image ---
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")