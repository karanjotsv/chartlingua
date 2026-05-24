import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Initialize Figure ---
fig = go.Figure()
s = chart_data['sections']
style = chart_data['style']
footer = chart_data['footer']

# --- 3. Add Traces for each section ---

# Population
pop_sec = s['population']
fig.add_trace(go.Pie(
    values=pop_sec['data']['values'],
    labels=['', ''],
    hole=0.7,
    marker=dict(colors=pop_sec['colors']),
    domain={'x': [0.0, 0.35], 'y': [0.68, 0.88]},
    hoverinfo='none',
    textinfo='none',
    sort=False
))

# Economic Output
econ_sec = s['economic_output']
fig.add_trace(go.Pie(
    values=econ_sec['data']['values'],
    labels=['', ''],
    hole=0.7,
    marker=dict(colors=econ_sec['colors']),
    domain={'x': [0.0, 0.35], 'y': [0.41, 0.61]},
    hoverinfo='none',
    textinfo='none',
    sort=False
))

# Unemployment
unemp_sec = s['unemployment']
fig.add_trace(go.Bar(
    x=unemp_sec['data']['categories'],
    y=unemp_sec['data']['values'],
    marker_color=unemp_sec['colors'],
    text=[f"{v}%" for v in unemp_sec['data']['values']],
    textposition='outside',
    textfont=dict(size=14, family=style['font_family']),
    hoverinfo='none',
    xaxis='x1',
    yaxis='y1'
))

# Working-age population with no qualifications
work_sec = s['working_age']
fig.add_trace(go.Bar(
    x=work_sec['data']['values'],
    y=work_sec['data']['categories'],
    orientation='h',
    marker_color=work_sec['colors'][0],
    text=[f"{v}%" for v in work_sec['data']['values']],
    textposition='outside',
    textfont=dict(size=14, family=style['font_family']),
    hoverinfo='none',
    xaxis='x2',
    yaxis='y2'
))

# Crime
crime_sec = s['crime']
fig.add_trace(go.Bar(
    x=crime_sec['data']['values'],
    y=crime_sec['data']['categories'],
    orientation='h',
    marker_color=crime_sec['colors'],
    text=crime_sec['data']['values'],
    textposition='inside',
    texttemplate='<b>%{text}</b>',
    textfont=dict(size=24, color='white', family=style['font_family']),
    insidetextanchor='middle',
    hoverinfo='none',
    width=0.6,
    xaxis='x3',
    yaxis='y3'
))


# --- 4. Define Layout and Annotations ---
annotations = []

# Main Title
annotations.append(dict(
    text=f"<b>{chart_data['title']}</b>",
    xref="paper", yref="paper", x=0.0, y=1.0, xanchor='left', yanchor='top',
    showarrow=False, font=dict(size=26, color=style['text_color'])
))

# Section Headers (as colored rectangles with text)
header_y = 0.92
section_headers_map = {
    'population':      {'x': 0.175, 'y': header_y},
    'median_age':      {'x': 0.5, 'y': header_y},
    'life_expectancy': {'x': 0.825, 'y': header_y},
    'economic_output': {'x': 0.175, 'y': 0.63},
    'unemployment':    {'x': 0.175, 'y': 0.35},
    'working_age':     {'x': 0.5, 'y': 0.35},
    'crime':           {'x': 0.825, 'y': 0.35},
}
for name, pos in section_headers_map.items():
    section = s[name]
    annotations.append(dict(
        text=f"<b>{section['title']}</b>",
        xref="paper", yref="paper", x=pos['x'], y=pos['y'],
        showarrow=False, align='center',
        font=dict(size=12, color='white'),
        bgcolor=section['header_color'],
        borderpad=6, width=180 if name != 'working_age' else 200
    ))

# Population Donut Annotations
annotations.append(dict(xref="paper", yref="paper", x=0.175, y=0.78, text=f"<b>{pop_sec['center_text']}</b>", showarrow=False, font=dict(size=24)))
annotations.append(dict(xref="paper", yref="paper", x=0.175, y=0.65, text=pop_sec['subtext'], showarrow=False, font=dict(size=12), align='center'))

# Economic Output Donut Annotations
annotations.append(dict(xref="paper", yref="paper", x=0.175, y=0.51, text=f"<b>{econ_sec['center_text']}</b>", showarrow=False, font=dict(size=24)))
annotations.append(dict(xref="paper", yref="paper", x=0.175, y=0.38, text=econ_sec['subtext'], showarrow=False, font=dict(size=12), align='center'))

# Median Age Text Block
ma_sec = s['median_age']
ma_y_start = 0.84
for i, item in enumerate(ma_sec['data']):
    y_pos = ma_y_start - i * 0.06
    annotations.append(dict(xref="paper", yref="paper", x=0.42, y=y_pos, text=item['label'], showarrow=False, font=dict(size=14), xanchor='left'))
    annotations.append(dict(xref="paper", yref="paper", x=0.58, y=y_pos, text=f"<b>{item['value']}</b><span style='font-size:12px'> {item['unit']}</span>", showarrow=False, font=dict(size=28, color=ma_sec['header_color']), xanchor='right'))
annotations.append(dict(xref="paper", yref="paper", x=0.5, y=ma_y_start - (len(ma_sec['data'])) * 0.06, text=ma_sec['subtext'], showarrow=False, font=dict(size=12), align='center'))

# Life Expectancy Text Block
le_sec = s['life_expectancy']
le_y_start = 0.84
for i, item in enumerate(le_sec['data']):
    y_pos = le_y_start - i * 0.07
    annotations.append(dict(xref="paper", yref="paper", x=0.825, y=y_pos + 0.01, text=f"<b>{item['label']}</b>", showarrow=False, font=dict(size=14), xanchor='center'))
    annotations.append(dict(xref="paper", yref="paper", x=0.75, y=y_pos - 0.02, text=f"<b>{item['male']}</b><br><span style='font-size:11px'>{le_sec['unit']}</span>", showarrow=False, font=dict(size=18, color=le_sec['header_color']), xanchor='center', align='center'))
    annotations.append(dict(xref="paper", yref="paper", x=0.9, y=y_pos - 0.02, text=f"<b>{item['female']}</b><br><span style='font-size:11px'>{le_sec['unit']}</span>", showarrow=False, font=dict(size=18, color=le_sec['header_color']), xanchor='center', align='center'))
annotations.append(dict(xref="paper", yref="paper", x=0.825, y=0.69, text=le_sec['subtext'], showarrow=False, font=dict(size=12), align='center'))

# Bar chart subtexts
annotations.append(dict(xref="paper", yref="paper", x=0.175, y=0.07, text=unemp_sec['subtext'], showarrow=False, font=dict(size=12)))
annotations.append(dict(xref="paper", yref="paper", x=0.5, y=0.07, text=work_sec['subtext'], showarrow=False, font=dict(size=12)))
annotations.append(dict(xref="paper", yref="paper", x=0.825, y=0.2, text=crime_sec['subtext'], showarrow=False, font=dict(size=12), align='center'))
annotations.append(dict(xref="paper", yref="paper", x=0.825, y=0.07, text=crime_sec['note'], showarrow=False, font=dict(size=12), align='center'))

# Crime bar icons
annotations.append(dict(xref='x3', yref='y3', x=10, y=crime_sec['data']['categories'][0], text="🏠", showarrow=False, font=dict(size=40, color='white'), xanchor='left'))
annotations.append(dict(xref='x3', yref='y3', x=10, y=crime_sec['data']['categories'][1], text="🏠", showarrow=False, font=dict(size=40, color='white'), xanchor='left'))

# Footer
annotations.append(dict(xref="paper", yref="paper", x=0, y=0.03, text=f"<b>{footer['website']}</b>", showarrow=False, font=dict(size=14), xanchor='left', yanchor='bottom'))
annotations.append(dict(xref="paper", yref="paper", x=0, y=0, text=footer['source_note'], showarrow=False, font=dict(size=10), xanchor='left', yanchor='bottom', align='left'))
annotations.append(dict(xref="paper", yref="paper", x=0.98, y=0.02, text=f"<b>{footer['logo_text']}</b>", showarrow=False, font=dict(size=12), xanchor='right', yanchor='bottom', align='right'))


fig.update_layout(
    width=800,
    height=1200,
    showlegend=False,
    paper_bgcolor=style['background_color'],
    plot_bgcolor=style['background_color'],
    font=dict(family=style['font_family'], color=style['text_color']),
    margin=dict(t=80, b=80, l=40, r=40),
    annotations=annotations,
    # Axes for Unemployment
    xaxis1=dict(domain=[0.05, 0.3], anchor='y1', showgrid=False, zeroline=False, showline=False, visible=False),
    yaxis1=dict(domain=[0.12, 0.3], anchor='x1', showgrid=False, zeroline=False, showline=False, visible=False, range=[-1, 12]),
    # Axes for Working Age
    xaxis2=dict(domain=[0.4, 0.65], anchor='y2', showgrid=False, zeroline=False, showline=False, visible=False, range=[0, 15]),
    yaxis2=dict(domain=[0.12, 0.3], anchor='x2', showgrid=False, zeroline=False, showline=False, autorange='reversed', tickfont=dict(size=10)),
    # Axes for Crime
    xaxis3=dict(domain=[0.72, 0.98], anchor='y3', showgrid=False, zeroline=False, showline=False, visible=False, range=[0, 260]),
    yaxis3=dict(domain=[0.12, 0.3], anchor='x3', showgrid=False, zeroline=False, showline=False, autorange='reversed', tickfont=dict(size=12)),
)
fig.update_traces(cliponaxis=False, selector=dict(type='bar'))


# --- 5. Output Image ---
base_name = json_path.stem
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")