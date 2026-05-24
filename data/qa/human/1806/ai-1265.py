import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
base_name = pathlib.Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        y=chart_data['categories'],
        x=series['data'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=series['text'],
        textposition='inside',
        textfont=dict(color='black', size=14),
        insidetextanchor='middle',
        hoverinfo='none'
    ))

title_text = f"<b>{texts['title']}</b><br><span style='color:#555555; font-size:16px; font-style:italic;'>{texts['subtitle']}</span>"
source_note_text = f"{texts['note']}<br>{texts['source']}"
logo_text = f"<b>{texts['logo']}</b>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=14, color="black"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        visible=False,
        range=[0, 100.1] 
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    margin=dict(l=100, r=20, t=100, b=120),
    annotations=[]
)

# Add series labels above the top bar
total_disapprove = chart_data['series'][0]['data'][-1]
total_approve = chart_data['series'][1]['data'][-1]
y_pos_labels = len(chart_data['categories']) - 0.55

fig.add_annotation(
    x=total_disapprove / 2,
    y=y_pos_labels,
    text=texts['series_labels'][0],
    showarrow=False,
    font=dict(size=14)
)

fig.add_annotation(
    x=total_disapprove + (total_approve / 2),
    y=y_pos_labels,
    text=texts['series_labels'][1],
    showarrow=False,
    font=dict(size=14)
)

# Add source, note, and logo at the bottom
fig.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.15,
    xanchor='left', yanchor='top',
    align='left',
    text=source_note_text,
    showarrow=False,
    font=dict(size=12, color="#555555")
)

fig.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.22,
    xanchor='left', yanchor='top',
    align='left',
    text=logo_text,
    showarrow=False,
    font=dict(size=13)
)

output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")