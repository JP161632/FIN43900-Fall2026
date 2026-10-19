# Video2 - Google Colab alternative

Open the supplied Video-2-Colab.ipynb in Google Colab. Colab can load a public GitHub notebook directly:

https://colab.research.google.com/github/JP161632/FIN43900-Fall2026/blob/main/projects/project-1/Video-2-Colab.ipynb

Use the ordinary CPU runtime; no paid plan, GPU, pip install or Google Drive mount is needed for this project. Run the setup cell once before recording. It downloads the frozen chart-release commit6d0d76de08f034e02dfc0a736bcab8ab421f7277 into a new temporary directory and creates a no-pip virtual environment. It does not modify the GitHub repository or the original frozen outputs.

For Video2, keep the validation chart visible for most of the script. When the script says you are running the project, briefly show the Colab notebook and execute **cell2**. Record the actual output and return to the chart. Colab replaces the local terminal overlay; it does not require a different finance explanation.

Expected successful console summary: `NVIDIA: PASS 15/15 tests; WATCH/DEFER; base $118.58; outputs: video2-output`. This is an expectation, not a claim you have run it. If your run fails, retain the observed error and resolve it before describing success.

The run cell also saves an actual UTC/runtime/source-commit/console log beside the new results. The optional download cell creates a results ZIP for you to retain; it does not invent a prediction, peer discussion or completed student event. Save/download the executed notebook with outputs as well. Colab's temporary VM files are not included merely by sharing a notebook link.

The notebook is a supplemental execution wrapper around the existing frozen project, not a new valuation edition or a replacement for the locked-input record. It has no prefilled execution counts or fabricated outputs.

Google's official FAQ: https://research.google.com/colaboratory/faq.html (free availability, GitHub notebooks, temporary virtual machines, saving/sharing and CPU runtime). Verified October19,2026. The supplied Python setup/run logic was verified locally against the same frozen Git commit; this session did not sign into or execute a Google-hosted Colab runtime.
