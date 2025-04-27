#!/usr/bin/env python3

import nbformat
import sys
import os


def clean_metadata(notebook_path):
    if not os.path.exists(notebook_path):
        return False

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    changed = False

    # Remove problematic metadata.widgets if it lacks 'state'
    widgets = nb.metadata.get("widgets", {})
    if "state" not in widgets:
        if "widgets" in nb.metadata:
            print(f"Removing invalid metadata.widgets from {notebook_path}")
            del nb.metadata["widgets"]
            changed = True

    # Remove Colab-specific metadata
    if "colab" in nb.metadata:
        print(f"Removing metadata.colab from {notebook_path}")
        del nb.metadata["colab"]
        changed = True

    if changed:
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
    return changed

if __name__ == "__main__":
    any_changes = False
    files = sys.argv[1:]

    for notebook in files:
        if notebook.endswith(".ipynb") and clean_metadata(notebook):
            any_changes = True

    if any_changes:
        print("Notebooks cleaned.")
    else:
        print("No cleaning needed.")