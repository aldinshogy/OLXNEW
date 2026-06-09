import re
import requests
import streamlit as st

def extract_ids_from_urls(urls):
    """
    Uzima samo zadnji broj iz OLX URL-a (ID oglasa)
    """
    ids = []
    pattern = re.compile(r'/(\d+)\s*$')  # hvata broj na kraju URL-a

    for url in urls:
        url = url.strip()
        match = pattern.search(url)
        if match:
            ids.append(match.group(1))

    return ids


def get_listing_state(listing_id):
    """
    Poziva OLX API i vraća state (new/used)
    """
    api_url = f"https://olx.ba/api/listings/{listing_id}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("state")
    except:
        return None


# ---------------- STREAMLIT APP ---------------- #

st.title("OLX - Filter samo 'Novo' oglasi")

urls = st.text_area("Unesi OLX URL-ove (jedan po liniji):")

if urls:
    urls_list = urls.strip().split('\n')

    # 1. extract ID-eva
    ids = extract_ids_from_urls(urls_list)

    st.write("🔎 Ekstrahovani ID-evi:", ",".join(ids))

    # 2. provjera state
    novo_links = []
    results = []

    for url, listing_id in zip(urls_list, ids):
        state = get_listing_state(listing_id)
        results.append((url, listing_id, state))

        if state == "new":
            novo_links.append(url)

    # 3. prikaz svih rezultata
    st.subheader("📊 Rezultati")
    for url, lid, state in results:
        st.write(f"{url} → {lid} → {state}")

    # 4. samo novo
    st.subheader("🟢 SAMO NOVO OGLASI")
    for link in novo_links:
        st.write(link)
