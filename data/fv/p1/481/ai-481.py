import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    # Add data traces
    for i, series in enumerate(chart_data['chart_data']):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(color=chart_data['colors'][i], width=3),
            showlegend=False
        ))

    # Add vertical lines and annotations
    y_max = 30
    for item in chart_data.get('annotations_and_lines', []):
        fig.add_shape(
            type="line",
            x0=item['x'], y0=0, x1=item['x'], y1=y_max,
            line=dict(color="black", width=2)
        )
        fig.add_annotation(
            x=item['x'],
            y=y_max,
            text=item['text'],
            showarrow=False,
            font=dict(family="Arial", size=12),
            yanchor="bottom",
            yshift=5
        )

    # Update layout
    texts = chart_data['texts']
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color='black'),
        showlegend=False,
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            range=[1989.5, 2016.5],
            showline=True,
            linewidth=1,
            linecolor='black',
            tickmode='linear',
            dtick=2,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 31],
            showline=True,
            linewidth=1,
            linecolor='black',
            tickmode='linear',
            dtick=5,
            showgrid=False,
            zeroline=False
        )
    )

    # Determine output filename and save
    if json_path.endswith('.json'):
        output_filename = json_path[:-5] + '.png'
    else:
        output_filename = json_path + '.png'
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()