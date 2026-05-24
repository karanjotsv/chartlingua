import sys
import json
import os
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

pull_values = [0.05 if v < 6 else 0 for v in values]

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='percent',
    textfont=dict(color='white', size=14, family="Arial"),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=50,
    pull=pull_values
))

title_text = f"{texts['title']}<br><span style='font-size: 16px; color: #808080;'>{texts['subtitle']}</span>"

annotations = []
cumulative_percent = 0
rotation_offset = 50 
r_text = 0.65
r_arrow = 0.48

for i, item in enumerate(data):
    slice_percent = item['value'] / 100.0
    mid_percent_of_slice = slice_percent / 2
    mid_angle_percent = cumulative_percent + mid_percent_of_slice
    
    # Plotly angles: 0 is 3 o'clock, positive is CCW. We use clockwise, so angles are negative.
    mid_angle_deg = rotation_offset - (mid_angle_percent * 360)
    mid_angle_rad = math.radians(mid_angle_deg)
    
    x_pos = 0.5 + r_text * math.cos(mid_angle_rad)
    y_pos = 0.5 + r_text * math.sin(mid_angle_rad)
    
    ax_pos = 0.5 + r_arrow * math.cos(mid_angle_rad)
    ay_pos = 0.5 + r_arrow * math.sin(mid_angle_rad)

    xanchor_val = 'left' if x_pos > 0.5 else 'right'
    
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=x_pos, y=y_pos,
            axref="paper", ayref="paper",
            ax=ax_pos, ay=ay_pos,
            text=item['category'],
            showarrow=True,
            arrowhead=0,
            arrowwidth=1,
            arrowcolor="#636363",
            font=dict(family="Arial", size=12, color="black"),
            align="center",
            xanchor=xanchor_val,
            yanchor="middle"
        )
    )
    cumulative_percent += slice_percent

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(family="Arial", size=24),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=150, r=150, t=100, b=50),
    annotations=annotations,
    font=dict(family="Arial")
)


base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")