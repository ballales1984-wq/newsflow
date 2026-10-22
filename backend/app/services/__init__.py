"""
Application services layer.

Holds the four collection strategies (RSS, generic API, Google News RSS,
HTML scraper) and the NLP pipeline (analysis + classification). Each
service traps its own errors so a single misbehaving source cannot abort
an entire collection run.
"""

# Services package

