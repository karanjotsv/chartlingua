import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract Data and Texts ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly, preserving order
x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    cliponaxis=False,  # Prevent text labels from being clipped at the top
    texttemplate='%{y}',
    textfont=dict(family="Arial", size=12, color='black')
))

# --- 4. Configure Layout ---
annotations = []

# Add source annotation if it exists
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="rgb(128,128,128)")
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.4,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=10,
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        tickmode='linear',
        tick0=0,
        dtick=2.5,
        range=[0, 18],
        tickfont=dict(family="Arial")
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# --- 5. Output the Image ---
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")