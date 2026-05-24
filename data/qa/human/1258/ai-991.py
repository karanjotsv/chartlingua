import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        y=chart_data['categories'],
        x=series['data'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=series['data'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14, family='Arial')
    ))

title_text = f"<span style='font-size:24px;'><b>{texts['title']}</b></span><br><span style='font-size:16px;'>{texts['subtitle']}</span>"

source_text = f"{texts['source']}<br><br><b>{texts['footer']}</b>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        visible=False,
        range=[0, max(chart_data['net_values']) + 15]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.82]
    ),
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=50, t=150, b=180),
    height=650
)

# Add NET values as annotations
for i, category in enumerate(chart_data['categories']):
    net_value = chart_data['net_values'][i]
    fig.add_annotation(
        x=net_value + 2,
        y=category,
        text=f"<b>{net_value}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(color='black', size=14, family='Arial')
    )

# Add column headers
header_y_pos = len(chart_data['categories']) - 0.4
fig.add_annotation(
    x=22, y=header_y_pos, text=f"<b>{texts['series_headers'][0]}</b>",
    showarrow=False, xanchor='center', font=dict(size=14, family='Arial')
)
fig.add_annotation(
    x=65, y=header_y_pos, text=f"<b>{texts['series_headers'][1]}</b>",
    showarrow=False, xanchor='center', font=dict(size=14, family='Arial')
)
fig.add_annotation(
    x=92, y=header_y_pos, text=f"<b>{texts['net_header']}</b>",
    showarrow=False, xanchor='center', font=dict(size=14, family='Arial')
)

# Add source note and footer
fig.add_annotation(
    text=source_text,
    xref='paper', yref='paper',
    x=0, y=-0.1,
    showarrow=False,
    align='left',
    xanchor='left', yanchor='top',
    font=dict(size=12, family='Arial')
)

# Add separator line
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=-0.08, x1=1, y1=-0.08,
    line=dict(color="black", width=1.5)
)

output_filename = f"{pathlib.Path(json_path).stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")