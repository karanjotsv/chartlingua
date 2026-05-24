import sys
import json
import plotly.graph_objects as go

# Ensure a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
colors = chart_info['colors']
texts = chart_info['texts']

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{label} %{percent}',
    textposition='outside',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    showlegend=False
)])

# Update layout for a clean appearance and to match the original
fig.update_layout(
    font=dict(family="Arial", size=14),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=80),  # Add margins to prevent label clipping
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=1,
            y=0,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="bottom",
            font=dict(size=12)
        )
    ]
)

# Determine the base filename for the output image from the input JSON path
base_name = json_path.split('/')[-1].split('.')[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")