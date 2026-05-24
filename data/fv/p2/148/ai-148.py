import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def find_annotation(annotations, type_key):
    for ann in annotations:
        if ann.get("type") == type_key:
            return ann["text"]
    return ""

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

# Section positioning on a 3x2 grid
positions = {
    "population":       {"domain": {"x": [0.0, 0.33], "y": [0.66, 1.0]}, "ax_ref": ""},
    "life_expectancy":  {"domain": {"x": [0.33, 0.66], "y": [0.66, 1.0]}, "ax_ref": ""},
    "qualifications":   {"domain": {"x": [0.66, 1.0], "y": [0.66, 1.0]}, "ax_ref": "2"},
    "economic_output":  {"domain": {"x": [0.0, 0.33], "y": [0.3, 0.63]}, "ax_ref": ""},
    "unemployment":     {"domain": {"x": [0.0, 0.33], "y": [0.0, 0.3]}, "ax_ref": "3"},
    "earnings":         {"domain": {"x": [0.33, 0.66], "y": [0.0, 0.3]}, "ax_ref": ""},
    "house_prices":     {"domain": {"x": [0.66, 1.0], "y": [0.0, 0.3]}, "ax_ref": "4"},
}

for section in chart_data["sections"]:
    sec_id = section["id"]
    pos = positions[sec_id]
    domain = pos["domain"]

    # Add header
    header_x_center = (domain["x"][0] + domain["x"][1]) / 2
    header_y = domain["y"][1] - 0.02
    header_width = 0.18
    fig.add_shape(type="rect",
        xref="paper", yref="paper",
        x0=header_x_center - header_width/2, y0=header_y - 0.02,
        x1=header_x_center + header_width/2, y1=header_y + 0.02,
        fillcolor=section["header_color"], line_width=0
    )
    fig.add_shape(type="path",
        path=f'M {header_x_center-0.015},{header_y-0.02} L {header_x_center},{header_y-0.05} L {header_x_center+0.015},{header_y-0.02} Z',
        xref="paper", yref="paper", fillcolor=section["header_color"], line_width=0
    )
    fig.add_annotation(
        text=section["header"],
        xref="paper", yref="paper",
        x=header_x_center, y=header_y,
        showarrow=False, font=dict(color="white", size=11, family="Arial")
    )
    
    # Add chart elements based on type
    if section["type"] == "donut":
        chart_domain = {'x': [domain['x'][0], domain['x'][1]], 'y': [domain['y'][0] + 0.05, domain['y'][1] - 0.1]}
        fig.add_trace(go.Pie(
            values=[section["data"]["value"], 100 - section["data"]["value"]],
            labels=["", ""],
            hole=0.7,
            marker_colors=section["colors"],
            domain=chart_domain,
            hoverinfo='none',
            textinfo='none',
            sort=False
        ))
        
        center_x = (chart_domain['x'][0] + chart_domain['x'][1]) / 2
        center_y = (chart_domain['y'][0] + chart_domain['y'][1]) / 2
        
        fig.add_annotation(
            text=f'<b>{find_annotation(section["annotations"], "main")}</b>',
            xref="paper", yref="paper", x=center_x, y=center_y + 0.02,
            showarrow=False, font=dict(size=24, family="Arial")
        )
        fig.add_annotation(
            text=find_annotation(section["annotations"], "sub"),
            xref="paper", yref="paper", x=center_x, y=center_y - 0.02,
            showarrow=False, font=dict(size=11, family="Arial")
        )
        
        footer_main = find_annotation(section["annotations"], "footer_main")
        if footer_main:
             fig.add_annotation(
                text=f'<b>{footer_main}</b>',
                xref="paper", yref="paper", x=center_x, y=chart_domain['y'][0]-0.02,
                showarrow=False, font=dict(size=14, family="Arial")
            )
        fig.add_annotation(
            text=find_annotation(section["annotations"], "footer_sub"),
            xref="paper", yref="paper", x=center_x, y=chart_domain['y'][0]- (0.05 if footer_main else 0.02),
            showarrow=False, font=dict(size=10, family="Arial"), align="center"
        )
        
    elif section["type"] == "bar":
        ax_ref = pos["ax_ref"]
        bar_domain = {'x': [domain['x'][0]+0.02, domain['x'][1]-0.02], 'y': [domain['y'][0], domain['y'][1]-0.15]}
        fig.add_trace(go.Bar(
            x=section["data"]["categories"],
            y=section["data"]["values"],
            marker_color=section["colors"],
            hoverinfo='none',
            xaxis=f'x{ax_ref}',
            yaxis=f'y{ax_ref}'
        ))
        fig.update_layout({
            f'xaxis{ax_ref}': {'domain': bar_domain['x'], 'anchor': f'y{ax_ref}', 'showticklabels': True, 'showgrid': False, 'linecolor': 'lightgrey'},
            f'yaxis{ax_ref}': {'domain': bar_domain['y'], 'anchor': f'x{ax_ref}', 'showticklabels': False, 'showgrid': False, 'range': [0, max(section["data"]["values"]) * 1.25]}
        })
        for i, val in enumerate(section["data"]["values"]):
             suffix = find_annotation(section["annotations"], "value_suffix")
             fig.add_annotation(
                 x=section["data"]["categories"][i], y=val,
                 text=f'{val}%<br>{suffix}' if suffix else f'{val}%',
                 showarrow=False, yshift=15 if suffix else 10,
                 font=dict(size=11, family="Arial"),
                 xaxis=f'x{ax_ref}', yaxis=f'y{ax_ref}', align="center"
             )
        fig.add_annotation(
            text=find_annotation(section["annotations"], "footer_sub"),
            xref="paper", yref="paper",
            x=(bar_domain['x'][0] + bar_domain['x'][1]) / 2, y=bar_domain['y'][0] - 0.01,
            showarrow=False, font=dict(size=10, family="Arial"), align="center"
        )

    elif section["type"] == "horizontal_bar":
        ax_ref = pos["ax_ref"]
        bar_domain = {'x': [domain['x'][0]+0.05, domain['x'][1]-0.02], 'y': [domain['y'][0], domain['y'][1]-0.15]}
        fig.add_trace(go.Bar(
            y=section["data"]["categories"],
            x=section["data"]["values"],
            orientation='h',
            marker_color=section["colors"][0],
            hoverinfo='none',
            xaxis=f'x{ax_ref}',
            yaxis=f'y{ax_ref}'
        ))
        fig.update_layout({
            f'xaxis{ax_ref}': {'domain': bar_domain['x'], 'anchor': f'y{ax_ref}', 'showticklabels': False, 'showgrid': False, 'range': [0, max(section["data"]["values"]) * 1.2]},
            f'yaxis{ax_ref}': {'domain': bar_domain['y'], 'anchor': f'x{ax_ref}', 'showticklabels': True, 'showgrid': False, 'autorange': 'reversed', 'linecolor': 'lightgrey'}
        })
        for i, val in enumerate(section["data"]["values"]):
            fig.add_annotation(
                y=section["data"]["categories"][i], x=val,
                text=f' {val}%',
                showarrow=False, xshift=15,
                font=dict(size=11, family="Arial"),
                xaxis=f'x{ax_ref}', yaxis=f'y{ax_ref}', align="left"
            )
        fig.add_annotation(
            text=find_annotation(section["annotations"], "footer_sub"),
            xref="paper", yref="paper",
            x=(bar_domain['x'][0] + bar_domain['x'][1]) / 2, y=bar_domain['y'][0] - 0.01,
            showarrow=False, font=dict(size=10, family="Arial"), align="center"
        )
    
    elif section["type"] == "text_block":
        base_x = (domain['x'][0] + domain['x'][1]) / 2
        base_y = domain['y'][1] - 0.15
        for i, series in enumerate(section['data']):
            y_pos = base_y - i * 0.09
            fig.add_annotation(text=f"<b>{series['group']}</b>", xref="paper", yref="paper", x=base_x, y=y_pos + 0.02,
                               showarrow=False, font=dict(size=13, family="Arial", color=section['colors']['highlight'] if series['group'] == 'South East' else 'black'))
            fig.add_annotation(text=f"<b>{series['male']}</b><br>years", xref="paper", yref="paper", x=base_x - 0.05, y=y_pos - 0.02,
                               showarrow=False, font=dict(size=12, family="Arial"), align="center")
            fig.add_annotation(text=f"<b>{series['female']}</b><br>years", xref="paper", yref="paper", x=base_x + 0.05, y=y_pos - 0.02,
                               showarrow=False, font=dict(size=12, family="Arial"), align="center")
        fig.add_annotation(
            text=find_annotation(section["annotations"], "footer_sub"),
            xref="paper", yref="paper", x=base_x, y=domain['y'][0],
            showarrow=False, font=dict(size=10, family="Arial"), align="center"
        )

    elif section["type"] == "annotated_circles":
        base_x = (domain['x'][0] + domain['x'][1]) / 2
        base_y = domain['y'][1] - 0.2
        positions = [(base_x, base_y + 0.05), (base_x - 0.06, base_y - 0.03), (base_x + 0.06, base_y - 0.03)] # NE, London, SE
        
        for i, series in enumerate(section['data']):
            pos_index = 0 if series['group'] == 'North East' else (1 if series['group'] == 'London' else 2)
            cx, cy = positions[pos_index]
            radius = 0.045
            
            fig.add_shape(type="circle", xref="paper", yref="paper",
                x0=cx - radius, y0=cy - radius, x1=cx + radius, y1=cy + radius,
                fillcolor=section['colors'][0], line=dict(color=section['colors'][0], width=4), opacity=0.3
            )
            fig.add_shape(type="circle", xref="paper", yref="paper",
                x0=cx - radius + 0.005, y0=cy - radius + 0.005, x1=cx + radius - 0.005, y1=cy + radius - 0.005,
                fillcolor='white', line_width=0
            )
            fig.add_annotation(text=f"<span style='color:{section['colors'][0]}'>{series['group']}</span><br><b style='font-size:16px'>{series['prefix']}{series['value']}</b>",
                xref="paper", yref="paper", x=cx, y=cy, showarrow=False, font=dict(family="Arial"), align="center"
            )
        fig.add_annotation(
            text=find_annotation(section["annotations"], "footer_sub"),
            xref="paper", yref="paper", x=base_x, y=domain['y'][0] - 0.01,
            showarrow=False, font=dict(size=10, family="Arial"), align="center"
        )

fig.update_layout(
    title=dict(
        text=f'<b>{chart_data["title"]}</b>',
        y=0.98, x=0.5, xanchor='center', yanchor='top',
        font=dict(size=22, family="Arial", color="#003D4F")
    ),
    showlegend=False,
    paper_bgcolor='#F2F2F2',
    plot_bgcolor='#F2F2F2',
    font_family="Arial",
    margin=dict(l=20, r=20, t=50, b=60),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True)
)

fig.add_annotation(
    text=chart_data["source"],
    xref="paper", yref="paper",
    x=0, y=0,
    xanchor='left', yanchor='bottom',
    showarrow=False,
    font=dict(size=10, family="Arial"),
    align="left"
)

fig.add_annotation(
    text=f'<b>{chart_data["logo"]}</b>',
    xref="paper", yref="paper",
    x=0.98, y=0.01,
    xanchor='right', yanchor='bottom',
    showarrow=False,
    font=dict(size=12, family="Arial"),
    align="right"
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2, width=600, height=850)
print(f"Chart saved to {output_filename}")