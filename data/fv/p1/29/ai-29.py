import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

subplot_titles = [f"<b>{config['texts']['title']}</b>" for config in chart_data['charts']]

fig = make_subplots(
    rows=len(chart_data['charts']),
    cols=1,
    subplot_titles=subplot_titles,
    vertical_spacing=0.25 
)

for i, config in enumerate(chart_data['charts']):
    row_num = i + 1
    
    x_data = [item['category'] for item in config['chart_data']]
    y_data = [item['value'] for item in config['chart_data']]
    
    # Filter out zero values for text display
    text_values = [v if v > 0 else '' for v in y_data]

    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        text=text_values,
        textposition='outside',
        marker=dict(
            color=config['colors']['bar_fill'],
            line=dict(
                color=config['colors']['bar_border'],
                width=1.5
            )
        ),
        cliponaxis=False,
        textfont=dict(size=10, family="Arial")
    ), row=row_num, col=1)

    # Add subtitle as an annotation below the main title
    fig.add_annotation(
        text=config['texts']['subtitle'],
        xref="paper", yref="paper",
        x=0.5, y=fig.layout[f'yaxis{row_num}']['domain'][1] - 0.02,
        xanchor='center', yanchor='top',
        showarrow=False,
        font=dict(size=12, family="Arial")
    )
    
    # Add Mode/Mean text as an annotation inside the plot
    fig.add_annotation(
        text=config['texts']['mode_mean_text'],
        xref=f'x{row_num} domain', yref=f'y{row_num} domain',
        x=0.01, y=0.98,
        xanchor='left', yanchor='top',
        showarrow=False,
        font=dict(size=10, family="Arial")
    )

    max_y = max(y_data) if y_data else 1
    fig.update_yaxes(
        range=[0, max_y * 1.25],
        visible=False,
        row=row_num, col=1
    )
    fig.update_xaxes(
        title_text=config['texts']['x_axis_title'],
        title_font=dict(size=11),
        tickfont=dict(size=10),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        row=row_num, col=1
    )
    
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=120, r=40, b=80, l=40),
    height=400 * len(chart_data['charts'])
)

for annotation in fig.layout.annotations:
    if '<b>' in annotation.text: 
        annotation.font.size = 14
        annotation.y = fig.layout[f'yaxis{int(annotation.xref.replace("x", "").replace(" domain", ""))}']['domain'][1] + 0.05 if annotation.xref and ' domain' not in annotation.xref else annotation.y
        if annotation.y > 1: annotation.y = 1

fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')

output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")