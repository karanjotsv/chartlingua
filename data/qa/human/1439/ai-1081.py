import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = data['chart_data']
    texts = data['texts']
    colors = data['colors']

    fig = go.Figure()

    # Plotly plots y-axis categories from bottom to top, so we reverse the lists to match the image.
    y_categories = chart_data['categories'][::-1]

    for i, series in enumerate(chart_data['series']):
        x_values = series['values'][::-1]
        fig.add_trace(go.Bar(
            y=y_categories,
            x=x_values,
            name=series['name'],
            orientation='h',
            marker=dict(color=colors[i], line=dict(width=0)),
            text=x_values,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(family="Arial", color='#000000', size=14)
        ))
    
    title_text = f"<b>{texts['title']}</b><br><span style='font-size:15px;color:#444444;'>{texts['subtitle']}</span>"
    
    annotations = [
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            text=f"{texts['note']}<br>{texts['source']}",
            showarrow=False,
            align='left',
            font=dict(family="Arial", size=12, color='#666666')
        ),
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.22,
            xanchor='left', yanchor='top',
            text=f"<b>{texts['branding']}</b>",
            showarrow=False,
            align='left',
            font=dict(family="Arial", size=12, color='#000000')
        )
    ]

    fig.update_layout(
        barmode='stack',
        title=dict(
            text=title_text,
            y=0.98,
            x=0.01,
            xanchor='left',
            yanchor='top',
            font=dict(size=22)
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
            domain=[0.2, 1] # create space for y-axis labels
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(size=14)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.9,
            xanchor="left",
            x=0.21,
            traceorder='normal',
            title_text=''
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=20, t=160, b=130),
        font=dict(family="Arial", color='#333333'),
        annotations=annotations,
        height=500
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()