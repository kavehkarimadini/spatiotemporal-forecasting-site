/* Paper data extracted from Karimadini & Pourebrahim (2026), Sci Rep */
window.PAPER_DATA = {
  meta: {
    title: "Simulation of long-term spatio-temporal environmental dynamics using a unified benchmark of neighbor augmenting, LSTM and graph attention models",
    journal: "Scientific Reports",
    year: 2026,
    doi: "10.1038/s41598-026-56762-5",
    received: "9 March 2026",
    accepted: "2 June 2026",
    authors: [
      { name: "Kaveh Karimadini", affiliation: "School of Computing, Macquarie University, Sydney, Australia", email: "kaveh.karimadini@students.mq.edu.au" },
      { name: "Sharareh Pourebrahim", affiliation: "Jeffrey Sachs Center on Sustainable Development & Sunway Institute for Global Strategy & Competitiveness, Sunway University, Malaysia", email: "shararehp@sunway.edu.my", corresponding: true }
    ],
    keywords: ["Spatio-temporal forecasting", "Geospatial time series", "LSTM", "Graph Attention Network (GAT)", "Environmental monitoring"],
    funding: "Sunway University grant GRTIN-RAG (02)-JSC-01-2024; HPC laptop from DecisionSigma Company",
    studyArea: { name: "Klang River Basin", location: "Peninsular Malaysia", areaHa: 127326, grid: "1825 × 1867 pixels" }
  },

  models: [
    { id: "model_1", short: "Model 1", name: "GAT–Temporal Attention (MLP)", aux: false, sGat: 2, t: 1, params: 59269, family: "gat-ta" },
    { id: "model_2", short: "Model 2", name: "GAT–Temporal Attention (MLP)", aux: false, sGat: 1, t: 1, params: 54981, family: "gat-ta" },
    { id: "model_3", short: "Model 3", name: "NA-LSTM (with auxiliary inputs)", aux: true, sGat: null, t: 1, params: 16485, family: "nalstm", best: true },
    { id: "model_4", short: "Model 4", name: "NA-LSTM (without auxiliary inputs)", aux: false, sGat: null, t: 1, params: 10725, family: "nalstm" },
    { id: "model_5", short: "Model 5", name: "GAT–Temporal Attention (MLP, with aux)", aux: true, sGat: 1, t: 1, params: 55301, family: "gat-ta" }
  ],

  indices: ["NDVI", "NDBI", "NDWI", "MNDWI", "EVI", "SAVI", "MSAVI", "BSI", "GNDVI", "OSAVI"],
  indexGroups: {
    vegetation: ["NDVI", "GNDVI", "SAVI", "MSAVI", "OSAVI"],
    water: ["NDWI", "MNDWI"],
    built: ["NDBI"],
    challenging: ["EVI", "BSI"]
  },

  metrics: [
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "NDVI", rmse: 0.1308, mae: 0.1026, mape: 106.1529, correlation: 0.8570, r2: 0.6352, meanDiff: 0.1026, stdDiff: 0.1296 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "NDBI", rmse: 0.1268, mae: 0.1042, mape: 53.0599, correlation: 0.9238, r2: 0.4886, meanDiff: 0.1042, stdDiff: 0.1244 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "NDWI", rmse: 0.1268, mae: 0.1042, mape: 53.0599, correlation: 0.9238, r2: 0.4886, meanDiff: 0.1042, stdDiff: 0.1244 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "MNDWI", rmse: 0.1268, mae: 0.1042, mape: 53.0599, correlation: 0.9238, r2: 0.4886, meanDiff: 0.1042, stdDiff: 0.1244 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "EVI", rmse: 0.1652, mae: 0.1294, mape: 154.8633, correlation: 0.8956, r2: 0.4971, meanDiff: 0.1294, stdDiff: 0.1304 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "SAVI", rmse: 0.0919, mae: 0.0798, mape: 134.5598, correlation: 0.9265, r2: 0.5565, meanDiff: 0.0798, stdDiff: 0.0919 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "MSAVI", rmse: 0.0949, mae: 0.0826, mape: 149.2168, correlation: 0.9244, r2: 0.5324, meanDiff: 0.0826, stdDiff: 0.0947 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "BSI", rmse: 0.1166, mae: 0.0928, mape: 382.0753, correlation: 0.6772, r2: 0.0462, meanDiff: 0.0928, stdDiff: 0.0998 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "GNDVI", rmse: 0.1268, mae: 0.1042, mape: 53.0599, correlation: 0.9238, r2: 0.4886, meanDiff: 0.1042, stdDiff: 0.1244 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_1", sGat: 2, t: 1, index: "OSAVI", rmse: 0.0933, mae: 0.0792, mape: 122.5745, correlation: 0.9183, r2: 0.6139, meanDiff: 0.0792, stdDiff: 0.0931 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "NDVI", rmse: 0.1424, mae: 0.1176, mape: 101.9778, correlation: 0.9234, r2: 0.5677, meanDiff: 0.1176, stdDiff: 0.0839 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "NDBI", rmse: 0.0934, mae: 0.0747, mape: 30.2828, correlation: 0.9433, r2: 0.7227, meanDiff: 0.0747, stdDiff: 0.0805 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "NDWI", rmse: 0.0934, mae: 0.0747, mape: 30.2828, correlation: 0.9433, r2: 0.7227, meanDiff: 0.0747, stdDiff: 0.0805 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "MNDWI", rmse: 0.0934, mae: 0.0747, mape: 30.2828, correlation: 0.9433, r2: 0.7227, meanDiff: 0.0747, stdDiff: 0.0805 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "EVI", rmse: 0.2787, mae: 0.2673, mape: 183.7852, correlation: 0.9359, r2: -0.4322, meanDiff: 0.2673, stdDiff: 0.0829 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "SAVI", rmse: 0.0816, mae: 0.0693, mape: 113.4220, correlation: 0.9488, r2: 0.6509, meanDiff: 0.0693, stdDiff: 0.0485 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "MSAVI", rmse: 0.0808, mae: 0.0699, mape: 123.0859, correlation: 0.9455, r2: 0.6612, meanDiff: 0.0699, stdDiff: 0.0472 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "BSI", rmse: 0.0911, mae: 0.0753, mape: 99.2389, correlation: 0.9060, r2: 0.4174, meanDiff: 0.0753, stdDiff: 0.0578 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "GNDVI", rmse: 0.0934, mae: 0.0747, mape: 30.2828, correlation: 0.9433, r2: 0.7227, meanDiff: 0.0747, stdDiff: 0.0805 },
    { model: "GAT–Temp Attn (MLP)", modelId: "model_2", sGat: 1, t: 1, index: "OSAVI", rmse: 0.0912, mae: 0.0777, mape: 108.9220, correlation: 0.9469, r2: 0.6304, meanDiff: 0.0777, stdDiff: 0.0518 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "NDVI", rmse: 0.0571, mae: 0.0370, mape: 29.2285, correlation: 0.9652, r2: 0.9305, meanDiff: 0.0370, stdDiff: 0.0571 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "NDBI", rmse: 0.0449, mae: 0.0303, mape: 15.4073, correlation: 0.9682, r2: 0.9360, meanDiff: 0.0303, stdDiff: 0.0449 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "NDWI", rmse: 0.0449, mae: 0.0303, mape: 15.4073, correlation: 0.9682, r2: 0.9360, meanDiff: 0.0303, stdDiff: 0.0449 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "MNDWI", rmse: 0.0449, mae: 0.0303, mape: 15.4073, correlation: 0.9682, r2: 0.9360, meanDiff: 0.0303, stdDiff: 0.0449 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "EVI", rmse: 0.0700, mae: 0.0459, mape: 30.3401, correlation: 0.9539, r2: 0.9096, meanDiff: 0.0459, stdDiff: 0.0700 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "SAVI", rmse: 0.0375, mae: 0.0247, mape: 28.9224, correlation: 0.9627, r2: 0.9263, meanDiff: 0.0247, stdDiff: 0.0375 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "MSAVI", rmse: 0.0394, mae: 0.0260, mape: 29.9344, correlation: 0.9592, r2: 0.9194, meanDiff: 0.0260, stdDiff: 0.0394 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "BSI", rmse: 0.0344, mae: 0.0247, mape: 80.2508, correlation: 0.9586, r2: 0.9169, meanDiff: 0.0247, stdDiff: 0.0344 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "GNDVI", rmse: 0.0449, mae: 0.0303, mape: 15.4073, correlation: 0.9682, r2: 0.9360, meanDiff: 0.0303, stdDiff: 0.0449 },
    { model: "LSTM (with aux)", modelId: "model_3", sGat: null, t: 1, index: "OSAVI", rmse: 0.0395, mae: 0.0258, mape: 28.7094, correlation: 0.9652, r2: 0.9309, meanDiff: 0.0258, stdDiff: 0.0395 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "NDVI", rmse: 0.0775, mae: 0.0563, mape: 32.6249, correlation: 0.9650, r2: 0.8721, meanDiff: 0.0563, stdDiff: 0.0730 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "NDBI", rmse: 0.0837, mae: 0.0686, mape: 32.2712, correlation: 0.9634, r2: 0.7772, meanDiff: 0.0686, stdDiff: 0.0655 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "NDWI", rmse: 0.0837, mae: 0.0686, mape: 32.2712, correlation: 0.9634, r2: 0.7772, meanDiff: 0.0686, stdDiff: 0.0655 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "MNDWI", rmse: 0.0837, mae: 0.0686, mape: 32.2712, correlation: 0.9634, r2: 0.7772, meanDiff: 0.0686, stdDiff: 0.0655 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "EVI", rmse: 7.4517, mae: 0.2364, mape: 96.6464, correlation: 0.0329, r2: -1022.5537, meanDiff: 0.2364, stdDiff: 7.4493 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "SAVI", rmse: 0.0415, mae: 0.0283, mape: 28.9869, correlation: 0.9605, r2: 0.9095, meanDiff: 0.0283, stdDiff: 0.0414 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "MSAVI", rmse: 0.0425, mae: 0.0291, mape: 30.0641, correlation: 0.9582, r2: 0.9064, meanDiff: 0.0291, stdDiff: 0.0423 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "BSI", rmse: 0.1115, mae: 0.1005, mape: 430.2640, correlation: 0.9383, r2: 0.1271, meanDiff: 0.1005, stdDiff: 0.0567 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "GNDVI", rmse: 0.0837, mae: 0.0686, mape: 32.2712, correlation: 0.9634, r2: 0.7772, meanDiff: 0.0686, stdDiff: 0.0655 },
    { model: "LSTM (without aux)", modelId: "model_4", sGat: null, t: 1, index: "OSAVI", rmse: 0.0474, mae: 0.0326, mape: 29.8677, correlation: 0.9630, r2: 0.9002, meanDiff: 0.0326, stdDiff: 0.0469 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "NDVI", rmse: 2.5350, mae: 0.1799, mape: 117.5658, correlation: 0.0075, r2: -135.9599, meanDiff: 0.1799, stdDiff: 2.5344 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "NDBI", rmse: 0.1181, mae: 0.0800, mape: 55.3663, correlation: 0.8313, r2: 0.5567, meanDiff: 0.0800, stdDiff: 0.1001 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "NDWI", rmse: 0.1181, mae: 0.0800, mape: 55.3663, correlation: 0.8313, r2: 0.5567, meanDiff: 0.0800, stdDiff: 0.1001 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "MNDWI", rmse: 0.1181, mae: 0.0800, mape: 55.3663, correlation: 0.8313, r2: 0.5567, meanDiff: 0.0800, stdDiff: 0.1001 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "EVI", rmse: 0.2823, mae: 0.2425, mape: 177.4950, correlation: -0.5105, r2: -0.4685, meanDiff: 0.2425, stdDiff: 0.2730 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "SAVI", rmse: 0.1326, mae: 0.1142, mape: 145.4538, correlation: 0.5020, r2: 0.0772, meanDiff: 0.1142, stdDiff: 0.1281 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "MSAVI", rmse: 0.1361, mae: 0.1155, mape: 160.9344, correlation: 0.4599, r2: 0.0387, meanDiff: 0.1155, stdDiff: 0.1298 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "BSI", rmse: 0.0772, mae: 0.0507, mape: 379.3436, correlation: 0.8201, r2: 0.5820, meanDiff: 0.0507, stdDiff: 0.0687 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "GNDVI", rmse: 0.1181, mae: 0.0800, mape: 55.3663, correlation: 0.8313, r2: 0.5567, meanDiff: 0.0800, stdDiff: 0.1001 },
    { model: "GAT–Temp Attn (MLP, with aux)", modelId: "model_5", sGat: 1, t: 1, index: "OSAVI", rmse: 0.1427, mae: 0.1227, mape: 133.2936, correlation: 0.5952, r2: 0.0957, meanDiff: 0.1227, stdDiff: 0.1378 }
  ],

  rollingOrigin: [
    { modelId: "model_3", name: "NA-LSTM (with aux)", y2024: 0.948, y2024std: 0.021, y2021: 0.906, y2020: 0.915, y2019: 0.882, avg: 0.913 },
    { modelId: "model_1", name: "GAT–TA MLP (S-GAT=2)", y2024: 0.792, y2024std: 0.033, y2021: 0.932, y2020: 0.904, y2019: 0.894, avg: 0.880 },
    { modelId: "model_5", name: "GAT–TA MLP (with aux)", y2024: 0.754, y2024std: 0.038, y2021: 0.873, y2020: 0.874, y2019: 0.895, avg: 0.856 },
    { modelId: "model_2", name: "GAT–TA MLP (S-GAT=1)", y2024: 0.842, y2024std: 0.048, y2021: 0.835, y2020: 0.741, y2019: 0.806, avg: 0.814 },
    { modelId: "model_4", name: "NA-LSTM (without aux)", y2024: 0.777, y2024std: 0.028, y2021: 0.712, y2020: 0.701, y2019: 0.761, avg: 0.740 }
  ],

  noiseRobustness: [
    { modelId: "model_2", name: "Model 2", twoStep: 0.610, original: 0.872, n001: 0.857, n003: 0.845, n005: 0.824 },
    { modelId: "model_3", name: "Model 3", twoStep: 0.686, original: 0.951, n001: 0.910, n003: 0.879, n005: 0.821 },
    { modelId: "model_1", name: "Model 1", twoStep: 0.678, original: 0.802, n001: 0.776, n003: 0.772, n005: 0.764 },
    { modelId: "model_4", name: "Model 4", twoStep: 0.217, original: 0.786, n001: 0.754, n003: 0.746, n005: 0.723 },
    { modelId: "model_5", name: "Model 5", twoStep: 0.682, original: 0.781, n001: 0.761, n003: 0.754, n005: 0.740 }
  ],

  hyperparams: {
    gat: [
      { param: "hidden_channels", value: "64", desc: "Shared hidden width for GAT + temporal-attention blocks" },
      { param: "num_gat_layers", value: "2 / 1", desc: "Depth of spatial GAT stack" },
      { param: "num_temporal_layers", value: "1", desc: "Depth of temporal self-attention stack" },
      { param: "gat_heads", value: "1", desc: "Attention heads per GAT layer" },
      { param: "temporal_heads", value: "8", desc: "Heads in temporal self-attention" },
      { param: "gat_concat", value: "True", desc: "Concatenate GAT multi-head outputs" },
      { param: "dropout", value: "0.1", desc: "Regularization dropout" },
      { param: "learning_rate", value: "0.01", desc: "Optimizer step size" },
      { param: "num_epochs", value: "15", desc: "Training epochs" },
      { param: "batch_size", value: "1", desc: "Samples per optimization step" }
    ],
    lstm: [
      { param: "lstm_units", value: "32", desc: "LSTM memory capacity" },
      { param: "lstm_input_timesteps", value: "1", desc: "Time steps per sample" },
      { param: "dense_hidden_units", value: "16", desc: "Post-LSTM dense layer width" },
      { param: "dense_hidden_activation", value: "relu", desc: "Dense layer nonlinearity" },
      { param: "output_units", value: "5", desc: "Target output channels" },
      { param: "output_activation", value: "sigmoid", desc: "Output value range" },
      { param: "optimizer", value: "adam", desc: "Weight update rule" },
      { param: "loss", value: "huber", desc: "Robust training objective" },
      { param: "epochs", value: "15", desc: "Training epochs" },
      { param: "batch_size", value: "1024", desc: "Batch size" }
    ]
  },

  complexity: [
    { model: "NA-LSTM", spatial: "Local 3×3 neighbourhood per pixel", scaling: "O(HW·9C) + O(HW·T·h²)", cost: "Per-pixel sequence modelling" },
    { model: "GAT-LSTM", spatial: "Graph nodes/edges", scaling: "O(T·E·heads·h) + O(N·T·h²)", cost: "Edge-wise attention + LSTM" },
    { model: "GAT-Temporal Attention", spatial: "Graph + temporal self-attention", scaling: "O(T·E·heads·h) + O(N·T²·h)", cost: "Graph attention + quadratic temporal attention" }
  ],

  figures: [
    { id: "fig1a", label: "Figure 1a", title: "NA-LSTM full pipeline", file: "NA_LSTM_Architecture.png" },
    { id: "fig1b", label: "Figure 1b", title: "GAT–Temporal Attention full pipeline", file: "GAT_Attention_Architecture.png" },
    { id: "fig2", label: "Figure 2", title: "Study area: Klang River Basin", file: "study_area_map.png" },
    { id: "fig4a", label: "Figure 4a", title: "NA-LSTM with auxiliary inputs", file: "scatter_plot_lstm_with_aux.png" },
    { id: "fig4b", label: "Figure 4b", title: "NA-LSTM without auxiliary inputs", file: "scatter_plot_lstm_without_aux.png" },
    { id: "fig4c", label: "Figure 4c", title: "GAT–TA (S-GAT=1, T=1)", file: "scatter_plot_GAT_Attention_1_1.png" },
    { id: "fig4d", label: "Figure 4d", title: "GAT–TA (S-GAT=2, T=1)", file: "scatter_plot_GAT_Attention_2_1.png" },
    { id: "fig4e", label: "Figure 4e", title: "GAT–TA with auxiliary inputs", file: "scatter_plot_GAT_Attention_with_aux_1_1.png" },
    { id: "fig5", label: "Figure 5", title: "R² comparison", file: "R_squared_grouped_bar.png" },
    { id: "fig6", label: "Figure 6", title: "RMSE comparison", file: "RMSE_grouped_bar.png" },
    { id: "fig7", label: "Figure 7", title: "MAE comparison", file: "MAE_grouped_bar.png" },
    { id: "fig8", label: "Figure 8", title: "Correlation comparison", file: "Correlation_grouped_bar.png" },
    { id: "fig9", label: "Figure 9", title: "MAPE comparison", file: "MAPE_grouped_bar.png" },
    { id: "fig10", label: "Figure 10", title: "Mean prediction difference", file: "Mean_Diff_grouped_bar.png" },
    { id: "fig11", label: "Figure 11", title: "Std of prediction differences", file: "Std_Dif_grouped_bar.png" }
  ]
};
