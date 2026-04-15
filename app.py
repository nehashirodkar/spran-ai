import json
import os
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

st.set_page_config(page_title="SpranAI", page_icon="✨", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081120 0%, #0b172a 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

.hero-card {
    padding: 1.5rem 1.6rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #172554 100%);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.35rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 720px;
}

.mini-chip-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.mini-chip {
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e2e8f0;
    font-size: 0.88rem;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
    color: #f8fafc;
}

.section-muted {
    color: #94a3b8;
    font-size: 0.96rem;
    margin-bottom: 0.9rem;
}

.custom-card {
    padding: 1rem 1.05rem;
    border-radius: 16px;
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
}

.bucket-card {
    padding: 1rem;
    border-radius: 16px;
    background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 20px rgba(0,0,0,0.16);
    min-height: 100px;
}

.bucket-label {
    font-size: 0.85rem;
    color: #93c5fd;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

.bucket-value {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.45;
}

.result-title {
    font-size: 1.12rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.6rem;
}

.result-meta {
    color: #cbd5e1;
    line-height: 1.7;
    font-size: 0.96rem;
}

.summary-card {
    padding: 1.1rem 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(30,41,59,1) 0%, rgba(15,23,42,1) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 0.6rem;
}

div[data-testid="stMetric"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.7rem 0.85rem;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.14);
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 1.15rem !important;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    font-weight: 600;
    padding: 0.55rem 1rem;
}

div[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)


def load_suppliers() -> List[Dict[str, Any]]:
    with open("suppliers.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_openai_api_key() -> str:
    """
    Safely fetch the OpenAI API key without crashing if secrets.toml is missing.
    """
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key:
            return api_key
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY", "")


def rule_based_spec(
    product_name: str,
    category: str,
    description: str,
    quantity: int,
    target_price: float,
    material: str,
) -> Dict[str, Any]:
    desc = (description or "").lower()

    features = []
    for keyword in [
        "zipper", "hood", "waterproof", "breathable", "logo",
        "oversized", "eco-friendly", "premium", "soft"
    ]:
        if keyword in desc:
            features.append(keyword)

    if "waterproof" in desc:
        recommended_materials = ["tpu", "pu coating", "dwr", "nylon"]
    elif "hoodie" in product_name.lower() or "hoodie" in desc:
        recommended_materials = ["cotton", "fleece", "cotton blend"]
    elif "activewear" in desc:
        recommended_materials = ["polyester", "spandex", "cotton blend"]
    elif material:
        recommended_materials = [material.lower()]
    else:
        recommended_materials = ["cotton"]

    manufacturing_notes = []
    if quantity < 100:
        manufacturing_notes.append("Low order quantity may reduce supplier availability.")
    if quantity > 10000:
        manufacturing_notes.append("High order quantity favors large-capacity manufacturers.")
    if target_price <= 8:
        manufacturing_notes.append("Aggressive target pricing may limit premium supplier options.")
    if "premium" in desc:
        manufacturing_notes.append("Premium finish may justify a higher unit cost.")
    if "logo" in desc:
        manufacturing_notes.append("Custom branding may require sampling or print setup.")

    return {
        "product_name": product_name,
        "category": category.lower().strip(),
        "description": description,
        "quantity": quantity,
        "target_price": target_price,
        "material": material.lower().strip() if material else "",
        "features": features,
        "recommended_materials": recommended_materials,
        "manufacturing_notes": manufacturing_notes,
    }


def ai_generate_spec(
    product_name: str,
    category: str,
    description: str,
    quantity: int,
    target_price: float,
    material: str,
) -> Dict[str, Any]:
    api_key = get_openai_api_key()

    if not api_key or OpenAI is None:
        return rule_based_spec(
            product_name=product_name,
            category=category,
            description=description,
            quantity=quantity,
            target_price=target_price,
            material=material,
        )

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are an AI sourcing assistant.

Convert the following product request into a structured sourcing brief.

Return ONLY valid JSON with exactly these keys:
product_name, category, description, quantity, target_price, material, features, recommended_materials, manufacturing_notes

Rules:
- "features" must be a JSON array of short strings
- "recommended_materials" must be a JSON array of short strings
- "manufacturing_notes" must be a JSON array of short strings
- Keep the output practical for manufacturing/sourcing
- Do not include markdown
- Do not include any explanation outside JSON

User input:
Product Name: {product_name}
Category: {category}
Description: {description}
Quantity: {quantity}
Target Price: {target_price}
Preferred Material: {material}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise sourcing and manufacturing assistant that outputs strict JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        parsed["product_name"] = parsed.get("product_name", product_name)
        parsed["category"] = str(parsed.get("category", category)).lower().strip()
        parsed["description"] = parsed.get("description", description)
        parsed["quantity"] = int(parsed.get("quantity", quantity))
        parsed["target_price"] = float(parsed.get("target_price", target_price))
        parsed["material"] = str(parsed.get("material", material)).lower().strip() if parsed.get("material") else ""
        parsed["features"] = parsed.get("features", [])
        parsed["recommended_materials"] = parsed.get("recommended_materials", [])
        parsed["manufacturing_notes"] = parsed.get("manufacturing_notes", [])

        return parsed

    except Exception:
        return rule_based_spec(
            product_name=product_name,
            category=category,
            description=description,
            quantity=quantity,
            target_price=target_price,
            material=material,
        )


def filter_suppliers(spec: Dict[str, Any], suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    filtered = []

    for supplier in suppliers:
        if supplier["category"] != spec["category"]:
            continue

        qty = spec["quantity"]
        qty_ok = qty >= supplier["min_order_qty"] * 0.75 and qty <= supplier["max_order_qty"] * 1.10
        if not qty_ok:
            continue

        preferred_material = spec.get("material", "").lower()
        recommended_materials = [m.lower() for m in spec.get("recommended_materials", [])]
        supplier_materials = [m.lower() for m in supplier.get("materials", [])]

        material_match = False
        if preferred_material and preferred_material in supplier_materials:
            material_match = True
        elif any(m in supplier_materials for m in recommended_materials):
            material_match = True
        elif not preferred_material:
            material_match = True

        if material_match:
            filtered.append(supplier)

    return filtered


def score_supplier(spec: Dict[str, Any], supplier: Dict[str, Any]) -> float:
    score = 0.0

    if spec["category"] == supplier["category"]:
        score += 20

    preferred_material = spec.get("material", "").lower()
    recommended_materials = [m.lower() for m in spec.get("recommended_materials", [])]
    supplier_materials = [m.lower() for m in supplier.get("materials", [])]

    if preferred_material and preferred_material in supplier_materials:
        score += 20
    elif any(m in supplier_materials for m in recommended_materials):
        score += 14
    else:
        score += 4

    qty = spec["quantity"]
    min_qty = supplier["min_order_qty"]
    max_qty = supplier["max_order_qty"]

    if min_qty <= qty <= max_qty:
        score += 20
        mid_capacity = (min_qty + max_qty) / 2
        if abs(qty - mid_capacity) / max(mid_capacity, 1) < 0.5:
            score += 5
    else:
        score -= 15

    target_price = spec["target_price"]
    unit_price = supplier["unit_price"]
    if target_price > 0:
        diff_ratio = abs(unit_price - target_price) / target_price
        if diff_ratio <= 0.10:
            score += 18
        elif diff_ratio <= 0.20:
            score += 12
        elif diff_ratio <= 0.35:
            score += 7
        else:
            score += 2

    lead = supplier["lead_time_days"]
    if lead <= 14:
        score += 10
    elif lead <= 18:
        score += 8
    elif lead <= 24:
        score += 5
    else:
        score += 2

    score += supplier["quality_rating"] * 4
    return round(score, 2)


def enrich_and_rank(spec: Dict[str, Any], suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ranked = []
    for supplier in suppliers:
        item = dict(supplier)
        item["match_score"] = score_supplier(spec, supplier)
        ranked.append(item)
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    return ranked


def get_recommendation_buckets(ranked: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    if not ranked:
        return {}

    return {
        "Best overall": ranked[0],
        "Best value": min(ranked, key=lambda x: (x["unit_price"], -x["quality_rating"])),
        "Fastest delivery": min(ranked, key=lambda x: x["lead_time_days"]),
        "Premium quality": max(ranked, key=lambda x: (x["quality_rating"], -x["unit_price"])),
    }


def reason_for_supplier(supplier: Dict[str, Any], spec: Dict[str, Any]) -> str:
    reasons = []

    if supplier["unit_price"] <= spec["target_price"]:
        reasons.append("fits within your target price")
    else:
        reasons.append("is slightly above your target price but offers stronger quality or sourcing fit")

    if supplier["min_order_qty"] <= spec["quantity"] <= supplier["max_order_qty"]:
        reasons.append("supports your required order volume")

    reasons.append(f"offers a {supplier['lead_time_days']}-day lead time")
    reasons.append(f"has a quality rating of {supplier['quality_rating']}")
    return ", ".join(reasons).capitalize() + "."


def build_comparison_df(ranked: List[Dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "Manufacturer": s["name"],
            "Country": s["country"],
            "Match Score": s["match_score"],
            "Unit Price ($)": s["unit_price"],
            "MOQ": s["min_order_qty"],
            "Lead Time (days)": s["lead_time_days"],
            "Quality": s["quality_rating"],
        }
        for s in ranked
    ])


with st.sidebar:
    st.title("SpranAI")
    st.write("Mini AI sourcing copilot for structured product briefs and manufacturer discovery.")
    st.write("LLM-assisted spec generation with deterministic ranking logic.")
    st.markdown("### Workflow")
    st.write("1. Enter product requirements")
    st.write("2. Generate sourcing brief")
    st.write("3. Match manufacturers")
    st.write("4. Compare recommendations")
    st.markdown("### Demo request")
    st.write("Custom gym hoodie, 500 units, cotton, target price $10")

st.markdown("""
<div class="hero-card">
    <div class="hero-title">SpranAI</div>
    <div class="hero-subtitle">
        AI-powered sourcing copilot inspired by Cavela. Turn product ideas into structured sourcing briefs,
        discover matching manufacturers, and compare recommendations based on cost, fit, quality, and speed.
    </div>
    <div class="mini-chip-row">
        <div class="mini-chip">10 manufacturers</div>
        <div class="mini-chip">4 recommendation modes</div>
        <div class="mini-chip">AI-assisted brief generation</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Create a sourcing request</div>', unsafe_allow_html=True)
st.markdown('<div class="section-muted">Enter product details below to generate a sourcing brief and manufacturer recommendations.</div>', unsafe_allow_html=True)

with st.form("product_form"):
    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("Product name", "Custom gym hoodie")
        category = st.selectbox("Category", ["apparel", "packaging", "home goods"])
        quantity = st.number_input("Quantity", min_value=1, value=500)
        target_price = st.number_input("Target unit price ($)", min_value=0.0, value=10.0, step=0.5)

    with col2:
        material = st.text_input("Preferred material", "cotton")
        image_url = st.text_input("Optional image URL", "")
        description = st.text_area(
            "Product description",
            "Black oversized gym hoodie with zipper, logo print, soft fleece interior, breathable and premium quality."
        )

    submitted = st.form_submit_button("Find manufacturers")

if submitted:
    st.markdown('<div class="section-title">✨ AI Generated Product Spec</div>', unsafe_allow_html=True)

    with st.spinner("Generating AI-powered sourcing brief..."):
        spec = ai_generate_spec(
            product_name=product_name,
            category=category,
            description=description,
            quantity=int(quantity),
            target_price=float(target_price),
            material=material,
        )

    suppliers = load_suppliers()
    filtered = filter_suppliers(spec, suppliers)
    ranked = enrich_and_rank(spec, filtered)

    if get_openai_api_key():
        st.success("AI spec generated successfully.")
        st.caption("AI extraction enabled: sourcing brief generated with an LLM.")
    else:
        st.success("Sourcing request processed successfully.")
        st.caption("AI extraction unavailable: using rule-based fallback.")

    st.markdown("### ✨ AI Generated Output")
    
    st.write("**Features:**", ", ".join(spec.get("features", [])))
    st.write("**Recommended Materials:**", ", ".join(spec.get("recommended_materials", [])))
    
    if spec.get("manufacturing_notes"):
        st.write("**Notes:**")
        for note in spec["manufacturing_notes"]:
            st.write("-", note)

    st.markdown('<div class="section-title">Structured sourcing brief</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="custom-card">
            <div class="result-title">Request overview</div>
            <div class="result-meta">
                <b>Product:</b> {spec['product_name']}<br>
                <b>Category:</b> {spec['category'].title()}<br>
                <b>Quantity:</b> {spec['quantity']}<br>
                <b>Target Price:</b> ${spec['target_price']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="custom-card">
            <div class="result-title">Detected requirements</div>
            <div class="result-meta">
                <b>Preferred Material:</b> {spec['material'] or 'Not specified'}<br>
                <b>Detected Features:</b> {', '.join(spec['features']) if spec['features'] else 'None detected'}<br>
                <b>Recommended Materials:</b> {', '.join(spec['recommended_materials']) if spec['recommended_materials'] else 'None suggested'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if spec["manufacturing_notes"]:
        with st.expander("Manufacturing considerations"):
            for note in spec["manufacturing_notes"]:
                st.write(f"- {note}")

    if image_url:
        st.image(image_url, width=280)

    st.divider()

    if not ranked:
        st.error("No suitable manufacturers were found. Try adjusting quantity, material, or target price.")
    else:
        st.markdown('<div class="section-title">Recommendation buckets</div>', unsafe_allow_html=True)

        buckets = get_recommendation_buckets(ranked)
        b1, b2, b3, b4 = st.columns(4)

        with b1:
            st.markdown(f"""
            <div class="bucket-card">
                <div class="bucket-label">Best overall</div>
                <div class="bucket-value">{buckets['Best overall']['name']}</div>
            </div>
            """, unsafe_allow_html=True)

        with b2:
            st.markdown(f"""
            <div class="bucket-card">
                <div class="bucket-label">Best value</div>
                <div class="bucket-value">{buckets['Best value']['name']}</div>
            </div>
            """, unsafe_allow_html=True)

        with b3:
            st.markdown(f"""
            <div class="bucket-card">
                <div class="bucket-label">Fastest delivery</div>
                <div class="bucket-value">{buckets['Fastest delivery']['name']}</div>
            </div>
            """, unsafe_allow_html=True)

        with b4:
            st.markdown(f"""
            <div class="bucket-card">
                <div class="bucket-label">Premium quality</div>
                <div class="bucket-value">{buckets['Premium quality']['name']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Top manufacturer recommendations</div>', unsafe_allow_html=True)

        for idx, s in enumerate(ranked[:3], start=1):
            st.markdown(f"""
            <div class="custom-card">
                <div class="result-title">{idx}. {s['name']}</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Match Score", s["match_score"])
            c2.metric("Unit Price", f"${s['unit_price']}")
            c3.metric("MOQ", s["min_order_qty"])
            c4.metric("Lead Time", f"{s['lead_time_days']} days")
            c5.metric("Quality", s["quality_rating"])

            st.markdown(f"""
            <div class="custom-card">
                <div class="result-meta">
                    <b>Country:</b> {s['country']}<br>
                    <b>Supported Materials:</b> {', '.join(s['materials'])}<br>
                    <b>Why recommended:</b> {reason_for_supplier(s, spec)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Compare all matched manufacturers"):
            st.dataframe(build_comparison_df(ranked), use_container_width=True)

        st.markdown('<div class="section-title">Recommendation summary</div>', unsafe_allow_html=True)
        best = buckets["Best overall"]
        best_value = buckets["Best value"]
        fastest = buckets["Fastest delivery"]

        st.markdown(f"""
        <div class="summary-card">
            For <b>{spec['product_name']}</b>, the strongest overall recommendation is <b>{best['name']}</b>
            because it offers the best balance of fit, price alignment, quality, and delivery timeline.<br><br>
            For cost-sensitive sourcing, <b>{best_value['name']}</b> is the strongest value option.<br>
            For faster turnaround, <b>{fastest['name']}</b> is the best speed-focused option.
        </div>
        """, unsafe_allow_html=True)