import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for plotting
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family="Arial", color='black', size=12)
))

# Create annotations for source and note
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            text=texts['note'],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color='#0073e5')
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

# Configure the layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=True,
        gridcolor='#F0F0F0',
        gridwidth=1,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 150],
        tickmode='array',
        tickvals=[0, 25, 50, 75, 100, 125, 150],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=annotations
)

# Derive the output filename from the input JSON path
# Handles paths like './path/to/chart.json' -> 'chart.png'
base_name = json_file_path.split('/')[-1].split('\\')[-1].split('.')[0]
output_image_path = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")