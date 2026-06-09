import requests
import streamlit as st

def extract_id(url: str):
    """
    Uzima samo OLX listing ID iz URL-a
    npr: https://olx.ba/artikal/76576474 -> 76576474
    """
    url = url.strip().rstrip("/")
    return url.split("/")[-1]


def get_listing_state(listing_id):
    api_url = f"https://olx.ba/api/listings/{listing_id}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json().get("state")
    except:
        return None


st.title("OLX filter - samo NOVO")

urls = st.text_area("Unesi OLX URL-ove (jedan po liniji):")

if urls:
    urls_list = [u.strip() for u in urls.split("\n") if u.strip()]

    results = []
    novo_links = []

    for url in urls_list:
        listing_id = extract_id(url)
        state = get_listing_state(listing_id)

        results.append((url, listing_id, state))

        if state == "new":
            novo_links.append(url)

    st.subheader("📊 Rezultati")

    for url, lid, state in results:
        st.write(f"{url} → {lid} → {state}")

    st.subheader("🟢 SAMO NOVO")
    for l in novo_links:
        st.write(l)
