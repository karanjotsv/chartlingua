import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_file_path}'.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly; horizontal bars are plotted from bottom to top, so we reverse the data
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
categories.reverse()
values.reverse()

# Format data labels to match original (e.g., "10%" instead of "10.0%")
text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(f'{int(v)}%')
    else:
        text_labels.append(f'{v}%')

# Create the main figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Configure the layout of the chart
fig.update_layout(
    height=750,
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=260, r=60, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        automargin=True,
        ticks='outside',
        ticklen=8
    )
)

# Add source information as an annotation at the bottom right
annotations = []
source_text = texts.get('source')
if source_text:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )
fig.update_layout(annotations=annotations)

# Determine the output image filename from the input JSON filename
output_path = pathlib.Path(json_file_path)
output_filename = output_path.with_suffix(".png").name

# Save the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")