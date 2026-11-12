# v1: keep answers inside the sources

System prompt (app/rag_chain.py) gains three rules aimed at the baseline failures: no steps, reasons or consequences the sources do not state; answer when the sources answer (yes/no first) instead of declining over a small gap; when declining a product mix-up, say what the Veloria product is.
