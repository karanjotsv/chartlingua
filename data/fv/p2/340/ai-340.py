import sys
import json
import plotly.graph_objects as go
import os

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

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    fig = go.Figure()

    # Extract data
    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]

    # Add trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        line=dict(color=colors[0], width=2),
        marker=dict(color=colors[0], symbol='diamond', size=10),
        name=''
    ))

    # Build title
    title_text = f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Update layout
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        title_font=dict(
            family="Arial",
            size=18,
            color="dimgray"
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=x_values,
            tickformat='d',
            showgrid=True,
            gridcolor='#D3D3D3',
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            range=[2300, 2800],
            dtick=50,
            showgrid=True,
            gridcolor='#D3D3D3',
            zeroline=False,
            showline=False
        ),
        plot_bgcolor='#F0F0F0',
        paper_bgcolor='#F0F0F0',
        showlegend=False,
        margin=dict(l=120, r=40, t=100, b=80),
        height=500,
        width=800
    )

    # Determine output filename from JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()