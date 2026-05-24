import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']
    
    categories = chart_data['categories']
    series = chart_data['series']

    fig = go.Figure()

    # Add bar traces for the data
    for i, s in enumerate(series):
        fig.add_trace(go.Bar(
            x=categories,
            y=s['data'],
            name=s['name'],
            marker_color=colors[i],
            text=[f"<b>{v}%</b>" for v in s['data']],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(
                family="Arial",
                size=16,
                color='white'
            ),
            hoverinfo='none',
            showlegend=False  # Hide default bar legends
        ))

    # Add dummy scatter traces for custom circle legends
    for i, s in enumerate(series):
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                color=colors[i],
                symbol='circle',
                size=12
            ),
            name=s['name'],
            showlegend=True
        ))

    # Combine title and subtitle if they exist
    title_text = texts.get('title') or ''
    subtitle_text = texts.get('subtitle') or ''
    if title_text and subtitle_text:
        chart_title = f"<b>{title_text}</b><br>{subtitle_text}"
    elif title_text:
        chart_title = f"<b>{title_text}</b>"
    else:
        chart_title = subtitle_text

    fig.update_layout(
        barmode='stack',
        title=dict(
            text=chart_title,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            type='category',
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            linecolor='black'
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 101],
            ticksuffix='%',
            showgrid=True,
            gridcolor='#E0E0E0',
            zeroline=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(
            family="Arial",
            size=12
        ),
        margin=dict(l=80, r=40, t=50, b=150)
    )

    # Add source annotation
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0.99, y=-0.28,
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=12, color="grey")
        )

    # Generate output file path and save image
    base_filename = json_path.rsplit('.', 1)[0]
    output_path = f"{base_filename}.png"
    
    fig.write_image(output_path, scale=2, width=1000, height=600)
    print(f"Chart saved to {output_path}")

if __name__ == '__main__':
    main()