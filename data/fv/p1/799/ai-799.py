import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
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

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])
    
    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Bar(
            x=series.get('x', []),
            y=series.get('y', []),
            name=series.get('name', ''),
            marker_color=colors[i % len(colors)] if colors else None
        ))
    
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            font=dict(size=24)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            tickangle=-45,
            automargin=True,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[0, 15],
            dtick=2,
            automargin=True,
            showgrid=True,
            gridcolor='lightgrey',
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            x=1.02,
            y=0.5,
            xanchor='left',
            yanchor='middle'
        ),
        margin=dict(l=80, r=150, t=100, b=150)
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2, width=900, height=600)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()