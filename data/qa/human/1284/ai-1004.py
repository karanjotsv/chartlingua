import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

# Add traces from JSON data
for trace_data in chart_data:
    name = trace_data['name']
    color = colors.get(name, '#000000')
    fig.add_trace(go.Scatter(
        x=trace_data['x'],
        y=trace_data['y'],
        name=name,
        mode='lines+markers',
        line=dict(
            color=color,
            dash=trace_data.get('line_style', 'solid'),
            width=2.5
        ),
        marker=dict(
            color=color,
            size=7,
            symbol='circle'
        ),
        legendgroup=name,
        showlegend=False 
    ))

# Create annotations for country labels at the end of each line
annotations = []
processed_countries = set()
for trace in reversed(chart_data):
    name = trace['name']
    if name not in processed_countries:
        annotations.append(go.layout.Annotation(
            x=trace['x'][-1],
            y=trace['y'][-1],
            text=f"   {name}   ",
            showarrow=True,
            arrowhead=0,
            xanchor='left',
            ax=10,
            ay=0,
            font=dict(family="Arial", size=12, color='#333333'),
            bgcolor='rgba(255, 255, 255, 0.85)',
            borderpad=4
        ))
        processed_countries.add(name)

# Combine title and subtitle
title_text = f"<span style='font-size: 22px;'><b>{texts['title']}</b></span><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='#eaf0f4',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=120, t=120, b=50),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        dtick=1,
        tickformat='d', # Display years as integers
        showgrid=False,
        zeroline=False,
        linecolor='#cccccc',
        range=[2009.5, 2018.5]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='white',
        gridwidth=1.5,
        zeroline=False,
        linecolor='#cccccc',
        range=[40, 90]
    ),
    annotations=annotations
)

# Add custom title, subtitle, source, and decorative line using annotations and shapes
fig.add_annotation(
    text=title_text,
    xref="paper", yref="paper",
    x=0, y=1.03,
    xanchor='left', yanchor='bottom',
    showarrow=False,
    align='left',
    font=dict(family="Arial")
)

fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=1, y=1.03,
    xanchor='right', yanchor='bottom',
    showarrow=False,
    align='right',
    font=dict(family="Arial", size=12, color="#555555")
)

fig.add_shape(
    type='line',
    xref='paper', yref='paper',
    x0=0, x1=1,
    y0=0.98, y1=0.98,
    line=dict(
        color="#00AEEF",
        width=2
    )
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2, width=1000, height=600)

print(f"Chart saved to {output_path}")