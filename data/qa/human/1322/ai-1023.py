import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

y_labels = [str(y) for y in chart_data['y_labels']]

for i, series in enumerate(chart_data['series']):
    bar_texts = []
    for j, val in enumerate(series['values']):
        if chart_data['y_labels'][j] == 1979:
            bar_texts.append(f"{val}%")
        else:
            bar_texts.append(str(val))

    fig.add_trace(go.Bar(
        y=y_labels,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors['bar_colors'][i],
            line=dict(color='white', width=1)
        ),
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color=colors['text_colors_inside_bar'][i]
        )
    ))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 17px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        y=0.97,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, family='Arial', color='black')
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0, 101]
    ),
    yaxis=dict(
        categoryorder='array',
        categoryarray=list(reversed(y_labels)),
        showgrid=False,
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='#ccc',
        tickfont=dict(size=14, family='Arial', color='black')
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=180, b=180),
    height=600,
    width=800
)

annotations = []
top_bar_values = [s['values'][0] for s in chart_data['series']]
mid_points_x = []
current_pos = 0
for val in top_bar_values:
    mid_points_x.append(current_pos + val / 2)
    current_pos += val

legend_y_base = 1.18

for i, series in enumerate(chart_data['series']):
    series_name = series['name']
    is_last_two = series_name in ("Green or regionalist", "Right-wing<br>to far right")
    
    if series_name == "Green or regionalist":
        x_val = mid_points_x[-2] + 2 # Position based on 'Right-wing' segment
        y_val_paper = legend_y_base + 0.08
    elif series_name == "Right-wing<br>to far right":
        x_val = mid_points_x[i] + 2
        y_val_paper = legend_y_base
    else:
        x_val = mid_points_x[i]
        y_val_paper = legend_y_base
    
    annotations.append(dict(
        xref='x', yref='paper',
        x=x_val, y=y_val_paper,
        text=series_name,
        showarrow=False,
        font=dict(
            family='Arial',
            size=13,
            color=colors['legend_text_colors'][i]
        ),
        align='center'
    ))

annotations.append(
    dict(
        xref='paper', yref='paper',
        x=0, y=-0.28,
        xanchor='left', yanchor='top',
        text=texts['note_source'],
        showarrow=False,
        align='left',
        font=dict(family='Arial', size=11, color='#666666')
    )
)

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")