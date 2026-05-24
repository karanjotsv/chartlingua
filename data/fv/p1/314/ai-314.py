import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    # Create an explosion effect for all slices except the first one
    pull_values = [0] + [0.2] * (len(values) - 1)

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        pull=pull_values,
        texttemplate='%{value:,}',
        textposition='outside',
        textfont=dict(size=12, family="Arial"),
        hoverinfo='label+percent+value',
        rotation=90,
        sort=False  # Preserve the original data order
    ))
    
    # Construct title
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sup>{texts['subtitle']}</sup>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        showlegend=True,
        legend=dict(
            traceorder='normal',
            font=dict(family="Arial", size=12)
        ),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # The original chart has no background color
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    output_filename_base = json_path.rsplit('.', 1)[0]
    output_filename = f"{output_filename_base}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()