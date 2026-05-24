import sys
import json
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
output_filename = json_file_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

labels = [f"{item['category']} ({item['value']}%)" for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hole=0,
    sort=False,
    direction='counterclockwise',
    rotation=90,
    textinfo='none',
    hoverinfo='label+percent'
))

layout_images = []
current_angle_deg = 90
total_value = sum(values)

for item in chart_data:
    if item.get('image_url'):
        slice_angle_deg = (item['value'] / total_value) * 360
        mid_angle_deg = current_angle_deg - (slice_angle_deg / 2)
        mid_angle_rad = math.radians(mid_angle_deg)
        
        radius_factor = 0.35
        x_pos = 0.5 + radius_factor * math.cos(mid_angle_rad)
        y_pos = 0.5 + radius_factor * math.sin(mid_angle_rad)
        
        layout_images.append(dict(
            source=item['image_url'],
            xref="paper", yref="paper",
            x=x_pos, y=y_pos,
            sizex=0.2, sizey=0.2,
            xanchor="center", yanchor="middle",
            layer="above",
            sizing="contain"
        ))
    
    current_angle_deg -= (item['value'] / total_value) * 360

title_text = f"<b>{texts['title']}</b>" if texts.get('title') else None

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    title_font_size=18,
    legend=dict(
        traceorder='normal',
        font=dict(size=12)
    ),
    margin=dict(l=50, r=50, t=80, b=50),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white',
    images=layout_images
)

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")