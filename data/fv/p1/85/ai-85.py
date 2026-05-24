import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

# Read data from the specified JSON file
json_file_path = sys.argv[1]
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data components from the loaded JSON
chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']

# Prepare data for plotting
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
# The domain property creates space on the right for the legend, similar to the original image
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    sort=False,
    hoverinfo='label+percent',
    textinfo='none',
    domain=dict(x=[0, 0.75])
))

# Configure the layout to match the original chart's appearance
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    font_family="Arial",
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder='normal'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=20)
)

# Determine the output filename from the input JSON filename
# e.g., if the input is 'my_chart.json', the output will be 'my_chart.png'
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")