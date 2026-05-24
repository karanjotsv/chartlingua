import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
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

    # --- Extract data from JSON ---
    texts = chart_data['texts']
    data = chart_data['chart_data']
    colors = chart_data['colors']
    
    reasons = data['reasons']
    subplots_data = data['subplots']
    subplot_titles = [sp['title'] for sp in subplots_data]

    # --- Create Figure ---
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=subplot_titles,
        shared_xaxes=True,
        shared_yaxes=True,
        vertical_spacing=0.1,
        horizontal_spacing=0.03
    )

    # --- Plot Data ---
    # To get a single legend, we create one trace per reason, and for each trace,
    # we add a bar to each of the four subplots.
    for i, reason in enumerate(reasons):
        color = colors.get(reason, '#CCCCCC')
        
        # Add a trace for each subplot for the current reason
        for j, subplot_info in enumerate(subplots_data):
            row = j // 2 + 1
            col = j % 2 + 1
            
            value_info = subplot_info['data'][i]
            val = value_info['value']
            text = value_info['text']
            
            # Show legend only for the first set of traces
            show_legend = (j == 0)
            
            fig.add_trace(go.Bar(
                y=[reason],
                x=[val] if val > 0 else [None], # Don't plot zero-value bars
                text=[text] if val > 0 else [''],
                name=reason,
                legendgroup=reason,
                showlegend=show_legend,
                marker_color=color,
                orientation='h',
                textposition='outside',
                textfont=dict(size=10, family="Arial"),
                cliponaxis=False
            ), row=row, col=col)

    # --- Update Layout ---
    title_text = f"<b>{texts['title']}</b><br><sup>{texts['subtitle']}</sup>"
    
    fig.update_layout(
        height=800,
        width=1200,
        font=dict(family="Arial", size=12),
        title=dict(text=title_text, x=0.5, y=0.95, xanchor='center', yanchor='top'),
        margin=dict(l=300, r=30, t=100, b=150),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            title=texts.get('legend_title', ''),
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            traceorder='normal'
        ),
        barmode='stack' # Stack bars with same y-category
    )

    # --- Update Axes ---
    fig.update_xaxes(
        range=[0, 100],
        ticksuffix='%',
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        zeroline=False
    )
    # Add x-axis titles only to the bottom subplots
    fig.update_xaxes(title_text=texts['x_axis_title'], row=2, col=1)
    fig.update_xaxes(title_text=texts['x_axis_title'], row=2, col=2)

    fig.update_yaxes(
        autorange="reversed",
        showgrid=False,
        tickfont=dict(size=10)
    )
    # Add y-axis titles only to the left subplots
    fig.update_yaxes(title_text=f"<b>{texts['y_axis_title']}</b>", row=1, col=1)
    fig.update_yaxes(title_text=f"<b>{texts['y_axis_title']}</b>", row=2, col=1)

    # --- Add Source Annotation ---
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0, y=-0.2,
        showarrow=False,
        align="left",
        xanchor='left', yanchor='bottom',
        font=dict(size=10)
    )

    # --- Output Image ---
    # Derive filename from JSON path
    base_name = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()