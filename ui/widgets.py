import streamlit as st

def dropdown_fk(label: str, options: list[tuple[int, str]], key: str, default_id: int | None = None):
    if not options:
        st.warning(f"No options available for: {label}")
        return None

    ids = [o[0] for o in options]
    labels = [o[1] for o in options]

    # If editing, preselect existing FK
    index = None
    if default_id in ids:
        index = ids.index(default_id)

    picked = st.selectbox(
        label,
        options=list(range(len(ids))),
        format_func=lambda i: labels[i],
        index=index,
        key=key,
    )

    # When index=None and user hasn't picked, Streamlit returns None
    if picked is None:
        return None

    return ids[picked]


def pick_row_by_id(label: str, rows: list[dict], id_key="id", display_key="nombre", key="pick"):
    """
    Let user pick an existing row for edit/delete.
    """
    if not rows:
        st.info("No rows found.")
        return None

    # build labels
    id_list = [r[id_key] for r in rows]
    labels = []
    for r in rows:
        val = r.get(display_key)
        if val is None:
            val = str(r[id_key])
        labels.append(f"{r[id_key]} — {val}")

    idx = st.selectbox(label, options=list(range(len(rows))), format_func=lambda i: labels[i], key=key)
    return rows[idx]
