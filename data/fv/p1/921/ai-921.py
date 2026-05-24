import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python recreate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=4)
        ),
        textinfo='percent',
        texttemplate='%{value}%',
        insidetextfont=dict(family='Arial', size=16, color='white'),
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        rotation=120
    ))

    title_text = f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.05,
            xanchor='left',
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=14,
            color="black"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            traceorder='normal'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=150, b=80),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    # print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()