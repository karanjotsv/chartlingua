import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=labels,
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none',
    cliponaxis=False
))

# Prepare annotations for source and note
annotations = []
if texts.get('source'):
    annotations.append(go.layout.Annotation(
        x=1, y=-0.15,
        xref='paper', yref='paper',
        text=texts['source'],
        showarrow=False,
        xanchor='right', yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color='#666666')
    ))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.5,
        tickvals=[-50, 0, 50, 100, 150],
        ticktext=['-50%', '0%', '50%', '100%', '150%'],
        range=[-90, 165],
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=40, b=100),
    annotations=annotations
)

# Derive the output filename from the input JSON file path
base_name = json_file_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Write the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")