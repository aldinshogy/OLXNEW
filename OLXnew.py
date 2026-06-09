import requests
import streamlit as st
import re


def extract_id(url: str):
    url = url.strip()

    # hvata prvi 6+ digit broj (OLX ID)
    match = re.search(r'(\d{6,})', url)
    return match.group(1) if match else None


def get_listing_state(listing_id):
    url = f"https://olx.ba/api/listings/{listing_id}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://olx.ba/"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        # 🔴 DEBUG (uključi ako treba)
        # st.write(listing_id, r.status_code, r.text[:200])

        if r.status_code != 200:
            return "ERROR_STATUS"

        # ako nije JSON → blokada
        try:
            data = r.json()
        except:
            return "NOT_JSON"

        # 🔥 višestruki fallback (OLX nije konzistentan)
        state = (
            data.get("state")
            or data.get("data", {}).get("state")
            or data.get("listing", {}).get("state")
        )

        return state if state else "NO_STATE"

    except:
        return "REQUEST_FAIL"


# ---------------- STREAMLIT ---------------- #

st.title("OLX filter - NOVO / USED")

urls = st.text_area("Unesi OLX URL-ove:")

if urls:
    urls_list = [u.strip() for u in urls.split("\n") if u.strip()]

    results = []
    novo = []

    for url in urls_list:
        listing_id = extract_id(url)

        if not listing_id:
            results.append((url, None, "BAD_URL"))
            continue

        state = get_listing_state(listing_id)
        results.append((url, listing_id, state))

        if state == "new":
            novo.append(url)

    st.subheader("📊 Rezultati")

    for u, i, s in results:
        st.write(f"{u} → {i} → {s}")

    st.subheader("🟢 SAMO NOVO")

    for n in novo:
        st.write(n)
