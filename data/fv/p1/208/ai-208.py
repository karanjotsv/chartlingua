import sys
import json
import pathlib
import plotly.graph_objects as go

def create_banner(fig, x0, x1, y0, y1, color, text):
    """Helper to create a colored banner with text."""
    fig.add_shape(
        type="rect",
        x0=x0, x1=x1, y0=y0, y1=y1,
        fillcolor=color,
        line_color=color,
        xref="paper", yref="paper"
    )
    fig.add_shape( # Downward pointing triangle
        type="path",
        path=f" M {(x0+x1)/2}, {y0} L {(x0+x1)/2 - 0.02}, {y0-0.03} L {(x0+x1)/2 + 0.02}, {y0-0.03} Z",
        fillcolor=color,
        line_color=color,
        xref="paper", yref="paper"
    )
    fig.add_annotation(
        x=(x0 + x1) / 2, y=(y0 + y1) / 2,
        text=text,
        showarrow=False,
        font=dict(color="white", size=14, family="Arial"),
        xref="paper", yref="paper"
    )

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
output_filename = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

texts = chart_data["texts"]
data_sections = chart_data["chart_data"]

fig = go.Figure()

fig.add_annotation(
    x=0.02, y=0.98,
    text=f"<b>{texts['title']}</b>",
    showarrow=False,
    font=dict(size=28, family="Arial", color="#003D4F"),
    xref="paper", yref="paper",
    align="left",
    xanchor="left", yanchor="top"
)

# --- Process Sections ---
# Section 1: Population
pop_section = data_sections[0]
create_banner(fig, 0.05, 0.3, 0.9, 0.94, pop_section['color'], pop_section['section_title'])
fig.add_trace(go.Pie(
    values=[pop_section['value'], 100 - pop_section['value']],
    hole=0.7,
    marker_colors=[pop_section['color'], '#E6E6E6'],
    sort=False,
    direction='clockwise',
    showlegend=False, textinfo='none',
    domain={'x': [0.05, 0.3], 'y': [0.77, 0.89]}
))
fig.add_annotation(x=0.175, y=0.84, text=f"<b>{pop_section['label_top']}</b>", showarrow=False, font=dict(size=30, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.81, text=pop_section['label_bottom'], showarrow=False, font=dict(size=12, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.74, text=f"<b>{pop_section['note_1']}</b>", showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.72, text=pop_section['note_2'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")

# Section 2: Median Age
age_section = data_sections[1]
create_banner(fig, 0.35, 0.65, 0.9, 0.94, age_section['color'], age_section['section_title'])
y_pos = 0.86
for item in age_section['data']:
    fig.add_annotation(x=0.40, y=y_pos, text=item['label'], showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper", xanchor="left")
    fig.add_annotation(x=0.58, y=y_pos, text=f"<b>{item['value']}</b>", showarrow=False, font=dict(size=30, family="Arial", color=age_section['color']), xref="paper", yref="paper", xanchor="right")
    fig.add_annotation(x=0.61, y=y_pos - 0.005, text=age_section['unit'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper", xanchor="left")
    y_pos -= 0.05
fig.add_annotation(x=0.5, y=0.7, text=age_section['note'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")

# Section 3: Life Expectancy
life_section = data_sections[2]
create_banner(fig, 0.7, 0.95, 0.9, 0.94, life_section['color'], life_section['section_title'])
y_pos = 0.85
for item in life_section['data']:
    fig.add_annotation(x=0.825, y=y_pos, text=f"<b>{item['label']}</b>", showarrow=False, font=dict(size=14, family="Arial", color=life_section['color']), xref="paper", yref="paper")
    fig.add_annotation(x=0.77, y=y_pos - 0.03, text=f"&#128104; {item['male']}<br><span style='font-size:10px;color:grey;'>{life_section['unit']}</span>", showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper")
    fig.add_annotation(x=0.88, y=y_pos - 0.03, text=f"&#128105; {item['female']}<br><span style='font-size:10px;color:grey;'>{life_section['unit']}</span>", showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper")
    y_pos -= 0.08
fig.add_annotation(x=0.825, y=0.69, text=life_section['note'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")

# Section 4: Economic Output
eco_section = data_sections[3]
create_banner(fig, 0.05, 0.3, 0.65, 0.69, eco_section['color'], eco_section['section_title'])
fig.add_trace(go.Pie(
    values=[eco_section['value'], 100 - eco_section['value']],
    hole=0.7,
    marker_colors=[eco_section['color'], '#E6E6E6'],
    sort=False,
    direction='clockwise',
    showlegend=False, textinfo='none',
    domain={'x': [0.05, 0.3], 'y': [0.52, 0.64]}
))
fig.add_annotation(x=0.175, y=0.59, text=f"<b>{eco_section['label_top']}</b>", showarrow=False, font=dict(size=30, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.56, text=eco_section['label_bottom'], showarrow=False, font=dict(size=12, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.49, text=eco_section['note_1'], showarrow=False, font=dict(size=11, family="Arial"), xref="paper", yref="paper")
fig.add_annotation(x=0.175, y=0.47, text=eco_section['note_2'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")


# Section 5: Unemployment
unemp_section = data_sections[4]
create_banner(fig, 0.05, 0.3, 0.4, 0.44, unemp_section['color'], unemp_section['section_title'])
categories = [d['category'] for d in unemp_section['data']]
values = [d['value'] for d in unemp_section['data']]
colors = [d['color'] for d in unemp_section['data']]
fig.add_trace(go.Bar(
    x=categories, y=values,
    marker_color=colors,
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    xaxis='x1', yaxis='y1'
))
fig.add_annotation(x=0.175, y=0.18, text=unemp_section['note'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")


# Section 6: Working-age population with no qualifications
work_section = data_sections[5]
create_banner(fig, 0.35, 0.65, 0.4, 0.44, work_section['color'], work_section['section_title'])
categories = [d['category'] for d in work_section['data']]
values = [d['value'] for d in work_section['data']]
fig.add_trace(go.Bar(
    x=values, y=categories,
    orientation='h',
    marker_color=work_section['color'],
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    xaxis='x2', yaxis='y2'
))
fig.add_annotation(x=0.5, y=0.23, text=work_section['note'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")


# Section 7: Crime
crime_section = data_sections[6]
create_banner(fig, 0.7, 0.95, 0.4, 0.44, crime_section['color'], crime_section['section_title'])
categories = [d['category'] for d in crime_section['data']]
values = [d['value'] for d in crime_section['data']]
colors = [d['color'] for d in crime_section['data']]
fig.add_trace(go.Bar(
    x=values, y=categories,
    orientation='h',
    marker_color=colors,
    marker_line_color='black', marker_line_width=1,
    text=[f"<b>{v}</b>" for v in values],
    textposition='inside',
    textfont=dict(color='black', size=24, family="Arial"),
    insidetextanchor='start',
    xaxis='x3', yaxis='y3'
))
fig.add_annotation(x=0.74, y=0.33, text="&#127968;", showarrow=False, font=dict(size=40, family="Arial", color=crime_section['color']), xref="paper", yref="paper", xanchor='left')
fig.add_annotation(x=0.74, y=0.27, text="&#127968;", showarrow=False, font=dict(size=40, family="Arial", color=crime_section['color']), xref="paper", yref="paper", xanchor='left')
fig.add_annotation(x=0.825, y=0.19, text=crime_section['note_1'] + "<br>" + crime_section['note_2'], showarrow=False, font=dict(size=11, family="Arial", color="grey"), xref="paper", yref="paper")

# --- Footer ---
fig.add_annotation(x=0.02, y=0.06, text=f"<b>{texts['footer_url']}</b>", showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper", xanchor="left", yanchor="bottom")
fig.add_annotation(x=0.02, y=0.03, text=texts['footer_source'], showarrow=False, font=dict(size=10, family="Arial", color="grey"), xref="paper", yref="paper", xanchor="left", yanchor="top", align="left")
fig.add_annotation(x=0.98, y=0.03, text=f"<b>{texts['footer_logo_text']}</b>", showarrow=False, font=dict(size=14, family="Arial"), xref="paper", yref="paper", xanchor="right", yanchor="middle", align="right")
fig.add_shape(type="rect", x0=0.8, x1=0.84, y0=0.02, y1=0.06, fillcolor="black", line_color="black", xref="paper", yref="paper")


# --- Layout Update ---
fig.update_layout(
    width=900, height=1400,
    paper_bgcolor="#F5F5F5",
    plot_bgcolor="#F5F5F5",
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family="Arial"),
    xaxis1=dict(domain=[0.05, 0.3], anchor='y1', range=[0, 12], showticklabels=False, showgrid=False, zeroline=False, visible=False),
    yaxis1=dict(domain=[0.18, 0.38], anchor='x1', showgrid=False, zeroline=False, linecolor='lightgrey', ticks="outside", ticklen=5),
    xaxis2=dict(domain=[0.38, 0.62], anchor='y2', range=[0, 15], showticklabels=False, showgrid=False, zeroline=False, visible=False),
    yaxis2=dict(domain=[0.25, 0.38], anchor='x2', autorange="reversed", showgrid=False, zeroline=False, linecolor='lightgrey', side='right', ticks=""),
    xaxis3=dict(domain=[0.7, 0.98], anchor='y3', range=[0, 300], showticklabels=False, showgrid=False, zeroline=False, visible=False),
    yaxis3=dict(domain=[0.25, 0.38], anchor='x3', autorange="reversed", showticklabels=False, showgrid=False, zeroline=False, visible=False)
)

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")