import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data['chart_data']
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    hoverinfo='label+percent',
    marker_colors=data['colors'],
    sort=False,
    insidetextorientation='horizontal'
)])

fig.update_traces(
    insidetextfont=dict(
        family="Arial",
        size=18,
        color="white"
    ),
    pull=[0, 0, 0, 0.05, 0, 0] # Slightly pull out the largest slice for emphasis
)

fig.update_layout(
    title_text=data['texts']['title'],
    title_font=dict(
        family="Arial",
        size=24,
        color="#000080"
    ),
    title_x=0.5,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font_family="Arial",
    margin=dict(t=100, b=50, l=50, r=50)
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)