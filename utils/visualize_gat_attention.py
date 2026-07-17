"""
Visualize the GAT + Temporal Attention (gat_attention) hybrid model architecture.
Shows data flow, tensor shapes, optional components (MLP/FFN, positional encoding),
paper equations (23–26). Temporal module is expanded like transformer attention:
H_i → Q/K/V (23) → Scaled Dot-Product Attention (24) → Concat+project → optional FFN (25).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


# Default example dimensions for labels
DEFAULT_NUM_FRAMES = 1
DEFAULT_NUM_NODES = "H×W"
DEFAULT_NUM_FEATURES = 9
DEFAULT_HIDDEN = 64
DEFAULT_OUTPUT_CHANNELS = 5


def _add_box(ax, xy, width, height, text, facecolor="lightblue", optional=False, edgecolor="black", fontsize=9, wrap=True):
    """Draw a rounded box with text. Use $...$ in text for math (mathtext)."""
    box = FancyBboxPatch(
        xy, width, height,
        boxstyle="round,pad=0.02,rounding_size=0.5",
        facecolor=facecolor,
        edgecolor="orange" if optional else edgecolor,
        linewidth=2 if optional else 1,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text,
            ha="center", va="center", fontsize=fontsize, wrap=wrap)


def _add_arrow(ax, start, end, label="", lw=2):
    """Draw an arrow from start to end with no gap (shrinkA=shrinkB=0 so line touches boxes)."""
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(arrowstyle="->", color="black", lw=lw, shrinkA=0, shrinkB=0),
        fontsize=8,
    )
    if label:
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(mid[0], mid[1], label, fontsize=7, ha="center", style="italic")


def visualize_gat_attention_architecture(
    num_frames=DEFAULT_NUM_FRAMES,
    num_nodes=DEFAULT_NUM_NODES,
    num_features=DEFAULT_NUM_FEATURES,
    hidden_channels=DEFAULT_HIDDEN,
    output_channels=DEFAULT_OUTPUT_CHANNELS,
    num_gat_layers=1,
    num_temporal_layers=1,
    use_positional_encoding=False,
    use_feed_forward=False,
    save_path="gat_attention_architecture.png",
    figsize=(10, 38),
):
    """
    Draw the GAT + Temporal Attention architecture with data flow and shapes.

    Parameters
    ----------
    num_frames : int or str
        Number of temporal frames (e.g. 1 or "T").
    num_nodes : int or str
        Number of nodes (e.g. "H×W" or integer).
    num_features : int
        Input feature dimension.
    hidden_channels : int
        Hidden dimension.
    output_channels : int
        Output channel dimension.
    num_gat_layers : int
        Number of GAT layers.
    num_temporal_layers : int
        Number of temporal attention layers.
    use_positional_encoding : bool
        Whether to show positional encoding as present (solid) or optional (dashed).
    use_feed_forward : bool
        Whether to show MLP/FFN as present (solid) or optional (dashed).
    save_path : str
        Path to save the figure.
    figsize : tuple
        Figure (width, height).
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 54)
    ax.axis("off")

    nodes_str = str(num_nodes)
    frames_str = str(num_frames)

    box_w = 6
    box_h = 1.5    # taller boxes so equations and multi-line text fit
    step = 2.5     # vertical gap between layer centers (longer arrows)
    x_center = 5
    y = 42

    def box_bottom(y_center, h=None):
        return y_center - (h or box_h) / 2
    def box_top(y_center, h=None):
        return y_center + (h or box_h) / 2

    # ---------- Preprocessing section ----------
    ax.text(x_center, 42.8, "GAT + Temporal Attention (gat_attention)", fontsize=14, ha="center", fontweight="bold")
    ax.text(x_center, 42.3, "Fully attention-based (no recurrence). Preprocessing → graph → Model → Output (num_nodes, output_channels)", fontsize=8, ha="center")
    y -= 0.9
    # Raw data box; arrow from above into it; bold label to the left of that arrow
    y_raw = y - 0.35
    arrow_pre_top = y_raw + box_h / 2 + 0.5
    arrow_pre_bottom = y_raw + box_h / 2
    _add_arrow(ax, (x_center, arrow_pre_top), (x_center, arrow_pre_bottom))
    mid_pre = (arrow_pre_top + arrow_pre_bottom) / 2
    ax.text(4.15, mid_pre, "Preprocessing (raw data → model input)", fontsize=11, ha="right", va="center", fontweight="bold")
    y = y_raw
    # 1. Raw data
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             "Raw data: Landsat NetCDF\nload_netcdf_data()\nshape: (T, H, W, C)\nT=timesteps, H×W=grid, C=5 (bands) or +NDVI +static → 6–9", facecolor="#E8E8E8")
    y -= step

    # 2. Normalize
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             "Normalize: channel-wise min-max [0, 1]\nnormalize_with_padding_dataset()\nshape: (T, H, W, C) unchanged", facecolor="#E8F4F8")
    _add_arrow(ax, (x_center, box_bottom(y_raw)), (x_center, box_top(y)))
    y_norm = y
    y -= step

    # 3. [Optional] Downsample
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             "[Optional] Downsample spatial (--no-downsample to disable)\ndownsample_spatial(stride=2)\nshape: (T, H′, W′, C)  H′=H/2, W′=W/2", facecolor="#F8D7DA", optional=True)
    _add_arrow(ax, (x_center, box_bottom(y_norm)), (x_center, box_top(y)))
    y_down = y
    y -= step

    # 4. Temporal sequences
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             "Temporal sequences: preprocess_netcdf_data(num_frames=1)\nX: (N, num_frames, H′, W′, C),  y: (N, H′, W′, 5)\nN = num_samples (train/val/test)", facecolor="#D4EDDA")
    _add_arrow(ax, (x_center, box_bottom(y_down)), (x_center, box_top(y)))
    y_seq = y
    y -= step

    # 5. Spatial to graph
    graph_in_shape = f"({frames_str}, {nodes_str}, {num_features})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             f"Spatial to graph: spatial_to_graph_data(X, y)\nReshape each sample: (num_frames, H′, W′, C) → (num_frames, H′×W′, C)\nEdge index: 4- or 8-connectivity. Output shape: {graph_in_shape}\n→ passed to model as batch of Data(x, edge_index)", facecolor="#D1ECF1")
    _add_arrow(ax, (x_center, box_bottom(y_seq)), (x_center, box_top(y)))
    y_preprocess = y
    y -= step

    # Model section: arrow from Spatial-to-graph into Input box; bold label to the left of that arrow
    y_input = y - 0.35
    arrow_model_top = box_bottom(y_preprocess)
    arrow_model_bottom = box_top(y_input)
    _add_arrow(ax, (x_center, arrow_model_top), (x_center, arrow_model_bottom))
    mid_model = (arrow_model_top + arrow_model_bottom) / 2
    ax.text(4.15, mid_model, "Model (GAT + Temporal Attention)", fontsize=11, ha="right", va="center", fontweight="bold")
    y = y_input
    # 1. Input (first layer of model)
    input_shape = f"({frames_str}, {nodes_str}, {num_features})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             f"Input (per-sample graph)\nshape: {input_shape}\nData.x = (num_frames, num_nodes, num_features)", facecolor="#E8F4F8")
    y -= step

    # 2. Input projection
    out_shape = f"({frames_str}, {nodes_str}, {hidden_channels})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             f"Linear: Input projection\nin: {num_features} → out: {hidden_channels}\nshape: {out_shape}", facecolor="#D4EDDA")
    _add_arrow(ax, (x_center, box_bottom(y_input)), (x_center, box_top(y)))
    y_proj = y
    y -= step

    # 3. GAT (per frame) — Spatial module (as in Model 1); output h(GAT)_{i,t}
    gat_text = (f"GAT layers × {num_gat_layers} (per frame)\nSpatial module: node embeddings h(GAT)_{{i,t}} per node i, time t\n"
                f"shape: ({frames_str}, {nodes_str}, {hidden_channels})")
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h, gat_text, facecolor="#FFF3CD")
    _add_arrow(ax, (x_center, box_bottom(y_proj)), (x_center, box_top(y)))
    y_gat = y
    y -= step

    # 4. [Optional] Positional encoding
    pos_text = f"[Optional] Positional encoding\nuse_positional_encoding=True\nshape: ({frames_str}, {nodes_str}, {hidden_channels})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h, pos_text, facecolor="#F8D7DA", optional=True)
    _add_arrow(ax, (x_center, box_bottom(y_gat)), (x_center, box_top(y)), "+ pos_emb" if use_positional_encoding else "")
    y_pos = y
    y -= step

    # ---------- Temporal module (Multi-head self-attention) — label beside arrow entering Input H_i ----------
    step_small = 1.65
    box_h_small = 0.85
    box_w_small = 1.55
    box_w_wide = 5.2
    # 5a. Input H_i (feeds temporal module) — math notation; arrow flush with box edges
    _add_box(ax, (x_center - box_w / 2, y - box_h_small / 2), box_w, box_h_small,
             r"Input $H_i = [h_{i,1}^{\mathrm{(GAT)}}, \ldots, h_{i,T}^{\mathrm{(GAT)}}]$ (per node $i$)", facecolor="#E2D5F1", fontsize=8, wrap=False)
    _add_arrow(ax, (x_center, box_bottom(y_pos)), (x_center, box_top(y, box_h_small)))
    mid_ta = (box_bottom(y_pos) + box_top(y, box_h_small)) / 2
    ax.text(4.15, mid_ta, "Temporal module\n(Multi-head self-attention)", fontsize=10, ha="right", va="center", fontweight="bold")
    y_hi = y
    y -= step_small

    # 5b. Q, K, V — three parallel linear transforms (Eq 23); arrows from H_i bottom to each Q,K,V top
    qkv_y = y
    box_w_qkv = 1.85
    qkv_specs = [(x_center - 2.0, r"$Q = H_i W_Q$", "q"), (x_center, r"$K = H_i W_K$", "k"), (x_center + 2.0, r"$V = H_i W_V$", "v")]
    arrow_start_x_offset = [-0.5, 0, 0.5]
    for (xx, math_label, _), start_dx in zip(qkv_specs, arrow_start_x_offset):
        _add_box(ax, (xx - box_w_qkv / 2, qkv_y - box_h_small / 2), box_w_qkv, box_h_small,
                 math_label + "\n(23)", facecolor="#DDA0DD", fontsize=8, wrap=False)
        _add_arrow(ax, (x_center + start_dx, box_bottom(y_hi, box_h_small)), (xx, box_top(qkv_y, box_h_small)))
    y -= step_small

    # 5c. Scaled Dot-Product Attention (Eq 24); arrows from Q,K,V bottom to this box top
    _add_box(ax, (x_center - box_w_wide / 2, y - box_h_small / 2), box_w_wide, box_h_small,
             r"Scaled Dot-Product: $\mathrm{softmax}(QK^T/\sqrt{d_k})V$ (24)", facecolor="#E6E6FA", fontsize=8, wrap=False)
    for xx in [x_center - 2.0, x_center, x_center + 2.0]:
        _add_arrow(ax, (xx, box_bottom(qkv_y, box_h_small)), (x_center, box_top(y, box_h_small)))
    y_att = y
    y -= step_small

    # 5d. Multi-head: two sentences on two lines
    _add_box(ax, (x_center - box_w_wide / 2, y - box_h_small / 2), box_w_wide, box_h_small,
             "Multi-head: outputs from H heads concatenated + linear projection.\nResidual + LayerNorm.", facecolor="#E2D5F1", fontsize=8, wrap=False)
    _add_arrow(ax, (x_center, box_bottom(y_att, box_h_small)), (x_center, box_top(y, box_h_small)))
    y_mha = y
    y -= step_small

    # 5e. [Optional] Feed-Forward (FFN) — Eq (25); taller box so all text fits inside; arrow flush
    box_h_ffn = 1.25
    _add_box(ax, (x_center - box_w_wide / 2, y - box_h_ffn / 2), box_w_wide, box_h_ffn,
             r"[Optional] $\mathrm{FFN}(x) = W_2\phi(W_1 x + b_1) + b_2$ (25)" + "\n"
             r"Linear$\to$GELU$\to$Linear(4$\times$hidden). Residual + LayerNorm", facecolor="#F8D7DA", optional=True, fontsize=8, wrap=False)
    _add_arrow(ax, (x_center, box_bottom(y_mha, box_h_small)), (x_center, box_top(y, box_h_ffn)))
    y_ffn = y
    ffn_bottom = y_ffn - box_h_ffn / 2
    y -= step_small

    # 7. Temporal aggregation — arrow from FFN bottom to aggregation top (flush)
    agg_shape = f"({nodes_str}, {hidden_channels})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             f"Temporal aggregation (mean over time)\nshape: {agg_shape}", facecolor="#D1ECF1")
    _add_arrow(ax, (x_center, ffn_bottom), (x_center, box_top(y)))
    y_agg = y
    y -= step

    # 8. Output projection — Eq (26) — LaTeX-style math
    out_final = f"({nodes_str}, {output_channels})"
    _add_box(ax, (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
             r"Output: $\hat{y}_{i,t+1} = W_o z_i + b_o$ (26). Five-band. shape: " + out_final, facecolor="#D4EDDA", wrap=False)
    _add_arrow(ax, (x_center, box_bottom(y_agg)), (x_center, box_top(y)))

    # Legend for optional
    opt_patch = mpatches.Patch(facecolor="#F8D7DA", edgecolor="orange", linewidth=2, label="Optional (CLI: --use-feed-forward / --use-positional-encoding)")
    ax.legend(handles=[opt_patch], loc="lower center", fontsize=8)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    return save_path


def _draw_step_flowchart(ax, step_id, nodes_str, frames_str, num_features, hidden_channels, output_channels,
                         box_w, box_h, step, x_center, _add_box, _add_arrow, box_bottom, box_top,
                         box_h_small, step_small, box_w_wide, box_w_qkv):
    """Draw one big step's flowchart in ax. Arrows go strictly between boxes (from box_bottom to box_top)."""
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    y = 8.8
    bh = box_h * 1.0
    bhs = box_h_small * 1.0
    if step_id == "preprocess":
        y_raw = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "Raw data: Landsat NetCDF.\nShape: (T, H, W, C).", facecolor="#E8E8E8", fontsize=8)
        y -= step
        y_norm = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "Normalize [0, 1].", facecolor="#E8F4F8", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_raw, bh)), (x_center, box_top(y_norm, bh)))
        y -= step
        y_down = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "[Optional] Downsample.\nstride=2 → (T, H′, W′, C).", facecolor="#F8D7DA", optional=True, fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_norm, bh)), (x_center, box_top(y_down, bh)))
        y -= step
        y_seq = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "Temporal sequences.", facecolor="#D4EDDA", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_down, bh)), (x_center, box_top(y_seq, bh)))
        y -= step
        y_spat = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 f"Spatial to graph.\n→ ({frames_str}, {nodes_str}, {num_features}).", facecolor="#D1ECF1", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_seq, bh)), (x_center, box_top(y_spat, bh)))
    elif step_id == "spatial":
        y_in = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 f"Input (per-sample graph).\nShape: ({frames_str}, {nodes_str}, {num_features}).", facecolor="#E8F4F8", fontsize=8)
        y -= step
        y_lin = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 f"Linear: {num_features}→{hidden_channels}.", facecolor="#D4EDDA", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_in, bh)), (x_center, box_top(y_lin, bh)))
        y -= step
        y_gat = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "GAT layers (per frame).\nNode embeddings h(GAT)_{i,t}.", facecolor="#FFF3CD", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_lin, bh)), (x_center, box_top(y_gat, bh)))
        y -= step
        y_pos = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 "[Optional] Positional encoding.", facecolor="#F8D7DA", optional=True, fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_gat, bh)), (x_center, box_top(y_pos, bh)))
    elif step_id == "temporal":
        y_hi = y
        _add_box(ax, (x_center - box_w / 2, y - bhs / 2), box_w, bhs,
                 r"Input $H_i$ (GAT emb. sequence).", facecolor="#E2D5F1", fontsize=8)
        y -= step_small
        qkv_y = y
        for dx, lbl in [(-0.5, "Q"), (0, "K"), (0.5, "V")]:
            xx = x_center + dx * 3.2
            _add_box(ax, (xx - box_w_qkv / 2, qkv_y - bhs / 2), box_w_qkv, bhs, f"{lbl} (23).", facecolor="#DDA0DD", fontsize=7)
            _add_arrow(ax, (x_center + dx * 0.3, box_bottom(y_hi, bhs)), (xx, box_top(qkv_y, bhs)))
        y -= step_small
        y_att = y
        _add_box(ax, (x_center - box_w_wide / 2, y - bhs / 2), box_w_wide, bhs,
                 r"Scaled Dot-Product (24).", facecolor="#E6E6FA", fontsize=8)
        for dx in [-0.5, 0, 0.5]:
            xx = x_center + dx * 3.2
            _add_arrow(ax, (xx, box_bottom(qkv_y, bhs)), (x_center, box_top(y_att, bhs)))
        y -= step_small
        y_mha = y
        _add_box(ax, (x_center - box_w_wide / 2, y - bhs / 2), box_w_wide, bhs,
                 "Multi-head: concat + linear project.\nResidual + LayerNorm.", facecolor="#E2D5F1", fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_att, bhs)), (x_center, box_top(y_mha, bhs)))
        y -= step_small
        y_ffn = y
        _add_box(ax, (x_center - box_w_wide / 2, y - bhs / 2), box_w_wide, bhs,
                 "[Optional] FFN (25).", facecolor="#F8D7DA", optional=True, fontsize=8)
        _add_arrow(ax, (x_center, box_bottom(y_mha, bhs)), (x_center, box_top(y_ffn, bhs)))
    else:
        y_agg = y
        _add_box(ax, (x_center - box_w / 2, y - bh / 2), box_w, bh,
                 f"Temporal aggregation (mean).\nShape: ({nodes_str}, {hidden_channels}).", facecolor="#D1ECF1", fontsize=8)
        y -= step
        y_out = y
        bh_out = bh * 1.35
        out_text = "Output (26): " + r"$\hat{y}_{i,t+1}=W_o z_i+b_o$." + "\nFive-band.\n" + f"Shape: ({nodes_str}, {output_channels})."
        _add_box(ax, (x_center - box_w / 2, y - bh_out / 2), box_w, bh_out,
                 out_text, facecolor="#D4EDDA", fontsize=8, wrap=False)
        _add_arrow(ax, (x_center, box_bottom(y_agg, bh)), (x_center, box_top(y_out, bh_out)))


def visualize_gat_attention_architecture_steps(
    num_frames=DEFAULT_NUM_FRAMES,
    num_nodes=DEFAULT_NUM_NODES,
    num_features=DEFAULT_NUM_FEATURES,
    hidden_channels=DEFAULT_HIDDEN,
    output_channels=DEFAULT_OUTPUT_CHANNELS,
    save_path="gat_attention_architecture_steps.png",
    figsize=(14, 5.5),
):
    """
    Draw the GAT + Temporal Attention architecture as 4 big steps in 4 subplots,
    with a bold title on each subplot and arrows from one step to the next.
    """
    fig, axes = plt.subplots(1, 4, figsize=figsize)
    fig.suptitle("GAT + Temporal Attention (gat_attention): Preprocessing → Model → Output", fontsize=12, fontweight="bold", y=0.98)
    box_w, box_h, step = 8.0, 1.1, 2.25
    x_center = 5
    box_h_small, step_small, box_w_wide, box_w_qkv = 0.75, 1.6, 7.0, 2.0

    def box_bottom(y_center, h=None):
        return y_center - (h or box_h) / 2
    def box_top(y_center, h=None):
        return y_center + (h or box_h) / 2

    nodes_str = str(num_nodes)
    frames_str = str(num_frames)

    steps = [
        ("Preprocessing", "preprocess"),
        ("Spatial module (GAT)", "spatial"),
        ("Temporal module (MHA)", "temporal"),
        ("Output", "output"),
    ]
    for ax, (title, step_id) in zip(axes, steps):
        ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
        rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, edgecolor="gray", linestyle="--", linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(rect)
        _draw_step_flowchart(ax, step_id, nodes_str, frames_str, num_features, hidden_channels, output_channels,
                            box_w, box_h, step, x_center, _add_box, _add_arrow, box_bottom, box_top,
                            box_h_small, step_small, box_w_wide, box_w_qkv)

    plt.subplots_adjust(wspace=0.4)
    plt.tight_layout()
    # Arrows from previous step to next (in figure coordinates, between subplots)
    for i in range(3):
        ax_left, ax_right = axes[i], axes[i + 1]
        pos_left, pos_right = ax_left.get_position(), ax_right.get_position()
        x1 = pos_left.x1
        x2 = pos_right.x0
        y_mid = (pos_left.y0 + pos_left.y1) / 2
        arrow = FancyArrowPatch((x1, y_mid), (x2, y_mid), transform=fig.transFigure,
                                arrowstyle="-|>", color="black", lw=1.5, shrinkA=0, shrinkB=0,
                                mutation_scale=14)
        fig.add_artist(arrow)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    return save_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize GAT + Temporal Attention architecture")
    parser.add_argument("--output", "-o", default="gat_attention_architecture.png", help="Output image path")
    parser.add_argument("--steps", action="store_true", help="Draw 4 big steps in subplots with titles and arrows between steps")
    parser.add_argument("--num-frames", type=int, default=1, help="Example num_frames")
    parser.add_argument("--num-nodes", type=str, default="H×W", help="Example num_nodes (e.g. H×W or 850896)")
    parser.add_argument("--num-features", type=int, default=9, help="Input feature dim")
    parser.add_argument("--hidden", type=int, default=64, help="Hidden dimension")
    parser.add_argument("--output-channels", type=int, default=5, help="Output channels")
    parser.add_argument("--use-positional-encoding", action="store_true", help="Show positional encoding as enabled")
    parser.add_argument("--use-feed-forward", action="store_true", help="Show MLP/FFN as enabled")
    args = parser.parse_args()
    if args.steps:
        out_steps = args.output.replace(".png", "_steps.png") if args.output.endswith(".png") else args.output + "_steps.png"
        path = visualize_gat_attention_architecture_steps(
            num_frames=args.num_frames,
            num_nodes=args.num_nodes,
            num_features=args.num_features,
            hidden_channels=args.hidden,
            output_channels=args.output_channels,
            save_path=out_steps,
        )
    else:
        path = visualize_gat_attention_architecture(
            num_frames=args.num_frames,
            num_nodes=args.num_nodes,
            num_features=args.num_features,
            hidden_channels=args.hidden,
            output_channels=args.output_channels,
            use_positional_encoding=args.use_positional_encoding,
            use_feed_forward=args.use_feed_forward,
            save_path=args.output,
        )
    print(f"Saved: {path}")
