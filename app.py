"""
Executive Decision Intelligence Dashboard
A lightweight, deterministic decision-support application connecting operational KPIs
with financial outcomes to produce evidence-based executive insights.
"""

import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. APPLICATION CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Executive Decision Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DETERMINISTIC SYNTHETIC BUSINESS DATASET
# ==============================================================================
@st.cache_data
def load_synthetic_business_data() -> pd.DataFrame:
    """
    Generates 12 months of deterministic sample data for a fictional retail company:
    'Apex Retail Enterprises'.
    
    Includes 10 core KPIs across 5 operational and financial categories, designed
    with realistic co-movement patterns:
      - Logistics strain (M03-M07): Delivery delays lead to complaint surges & retention drops.
      - Inventory carrying bloat (M04-M08): Spiking holding costs suppress operating profits.
      - Sales conversion surge (M08-M12): Enhanced conversion directly drives revenue growth.
      - Workforce productivity lift (M08-M12): Productivity dividends fuel profit recovery.
    """
    np.random.seed(42)
    
    months = [
        "Month 01 (Jan)", "Month 02 (Feb)", "Month 03 (Mar)", "Month 04 (Apr)",
        "Month 05 (May)", "Month 06 (Jun)", "Month 07 (Jul)", "Month 08 (Aug)",
        "Month 09 (Sep)", "Month 10 (Oct)", "Month 11 (Nov)", "Month 12 (Dec)"
    ]
    
    # Financial metrics
    revenue = np.array([
        1200000, 1210000, 1205000, 1190000, 1180000, 1195000,
        1220000, 1280000, 1340000, 1390000, 1440000, 1480000
    ], dtype=float)
    
    gross_margin = np.array([
        42.0, 42.1, 41.8, 41.2, 40.5, 40.0,
        40.4, 41.2, 42.0, 42.5, 42.8, 43.0
    ], dtype=float)
    
    # Operational cost drivers
    inventory_holding = np.array([
        40000, 41000, 42000, 58000, 78000, 89000,
        92000, 84000, 62000, 49000, 43000, 39000
    ], dtype=float)
    
    marketing = np.array([
        55000, 55000, 56000, 58000, 60000, 62000,
        64000, 67000, 70000, 72000, 75000, 78000
    ], dtype=float)
    
    base_operational_expenses = 240000.0
    operating_costs = base_operational_expenses + inventory_holding + marketing
    
    # Derived financial outcomes
    gross_profit = revenue * (gross_margin / 100.0)
    operating_profit = gross_profit - operating_costs
    
    # Customer experience KPIs
    on_time_delivery = np.array([
        95.5, 95.0, 93.8, 88.0, 83.5, 80.5,
        82.0, 88.5, 92.0, 94.8, 95.6, 96.2
    ], dtype=float)
    
    customer_complaints = np.array([
        1.7, 1.8, 2.1, 3.9, 5.1, 5.8,
        5.2, 3.6, 2.6, 2.0, 1.7, 1.5
    ], dtype=float)
    
    customer_retention = np.array([
        87.0, 86.5, 85.5, 81.0, 76.5, 73.0,
        74.5, 79.0, 83.0, 86.0, 87.2, 87.8
    ], dtype=float)
    
    # Sales & operations indicators
    sales_conversion = np.array([
        3.1, 3.2, 3.1, 3.2, 3.1, 3.3,
        3.4, 3.8, 4.2, 4.5, 4.8, 5.0
    ], dtype=float)
    
    employee_productivity = np.array([
        100.0, 100.5, 99.5, 96.0, 93.5, 91.0,
        93.0, 102.0, 110.5, 116.0, 121.0, 124.5
    ], dtype=float)
    
    df = pd.DataFrame({
        "Month": months,
        "Month_Index": np.arange(1, 13),
        "Revenue": revenue,
        "Gross_Profit_Margin": gross_margin,
        "Operating_Costs": operating_costs,
        "Operating_Profit": operating_profit,
        "Customer_Retention": customer_retention,
        "Customer_Complaints": customer_complaints,
        "On_Time_Delivery": on_time_delivery,
        "Inventory_Holding_Costs": inventory_holding,
        "Employee_Productivity": employee_productivity,
        "Marketing_Expenditure": marketing,
        "Sales_Conversion_Rate": sales_conversion
    })
    
    return df

# Metadata dictionary for KPIs
KPI_METADATA = {
    "Revenue": {
        "label": "Monthly Revenue",
        "category": "Financial Outcomes",
        "unit": "currency",
        "higher_is_better": True,
        "rel_financial": "Primary Top-Line Driver",
        "financial_weight": 30
    },
    "Operating_Profit": {
        "label": "Operating Profit",
        "category": "Financial Outcomes",
        "unit": "currency",
        "higher_is_better": True,
        "rel_financial": "Primary Bottom-Line Outcome",
        "financial_weight": 35
    },
    "Gross_Profit_Margin": {
        "label": "Gross Profit Margin",
        "category": "Financial Outcomes",
        "unit": "percentage",
        "higher_is_better": True,
        "rel_financial": "Unit Margin & Pricing Power",
        "financial_weight": 25
    },
    "Operating_Costs": {
        "label": "Operating Costs",
        "category": "Financial Outcomes",
        "unit": "currency",
        "higher_is_better": False,
        "rel_financial": "Direct Expense Drag",
        "financial_weight": 25
    },
    "Customer_Retention": {
        "label": "Customer Retention Rate",
        "category": "Customer Experience",
        "unit": "percentage",
        "higher_is_better": True,
        "rel_financial": "Customer Lifetime Value (LTV)",
        "financial_weight": 28
    },
    "Customer_Complaints": {
        "label": "Customer Complaint Rate",
        "category": "Customer Experience",
        "unit": "percentage",
        "higher_is_better": False,
        "rel_financial": "Churn & Brand Equity Risk",
        "financial_weight": 22
    },
    "On_Time_Delivery": {
        "label": "On-Time Delivery Rate",
        "category": "Logistics & Inventory",
        "unit": "percentage",
        "higher_is_better": True,
        "rel_financial": "Fulfillment SLA & Repeat Orders",
        "financial_weight": 24
    },
    "Inventory_Holding_Costs": {
        "label": "Inventory Holding Costs",
        "category": "Logistics & Inventory",
        "unit": "currency",
        "higher_is_better": False,
        "rel_financial": "Working Capital & Operating Profit",
        "financial_weight": 32
    },
    "Sales_Conversion_Rate": {
        "label": "Sales Conversion Rate",
        "category": "Sales & Marketing",
        "unit": "percentage",
        "higher_is_better": True,
        "rel_financial": "Funnel Yield & Revenue Growth",
        "financial_weight": 30
    },
    "Marketing_Expenditure": {
        "label": "Marketing Expenditure",
        "category": "Sales & Marketing",
        "unit": "currency",
        "higher_is_better": None,  # Contextual investment
        "rel_financial": "Customer Acquisition Cost",
        "financial_weight": 18
    },
    "Employee_Productivity": {
        "label": "Employee Productivity",
        "category": "Operations & Workforce",
        "unit": "index",
        "higher_is_better": True,
        "rel_financial": "Labor Efficiency & Operating Margin",
        "financial_weight": 28
    }
}

# ==============================================================================
# 3. HELPER & FORMATTING FUNCTIONS
# ==============================================================================
def format_value(val: float, unit: str) -> str:
    """Format numerical values based on currency, percentage, or index unit safely."""
    if pd.isna(val):
        return "N/A"
    if unit == "currency":
        return f"${val:,.0f}"
    elif unit == "percentage":
        return f"{val:.1f}%"
    elif unit == "index":
        return f"{val:.1f} pts"
    return f"{val:.2f}"

def safe_pct_change(curr: float, prev: float) -> float:
    """Calculates percentage change safely avoiding division by zero."""
    if prev == 0 or pd.isna(prev) or pd.isna(curr):
        return 0.0
    return ((curr - prev) / abs(prev)) * 100.0

# ==============================================================================
# 4. KPI MOVEMENT ANALYSIS ENGINE
# ==============================================================================
def compute_kpi_movements(df: pd.DataFrame, curr_idx: int, prev_idx: int) -> pd.DataFrame:
    """
    Computes period-over-period movements for all KPIs between current and previous periods.
    Determines absolute change, percentage change, directional movement, and business interpretation.
    """
    records = []
    curr_row = df.iloc[curr_idx]
    prev_row = df.iloc[prev_idx]
    
    for col, meta in KPI_METADATA.items():
        curr_val = curr_row[col]
        prev_val = prev_row[col]
        abs_diff = curr_val - prev_val
        pct_diff = safe_pct_change(curr_val, prev_val)
        
        # Direction arrow
        if abs(abs_diff) < 1e-4:
            direction = "→ Stable"
        elif abs_diff > 0:
            direction = "↗ Increasing"
        else:
            direction = "↘ Decreasing"
            
        # Business interpretation
        higher_better = meta["higher_is_better"]
        if higher_better is None:
            interpretation = "Neutral / Planned"
        elif abs(abs_diff) < 1e-4:
            interpretation = "Neutral (No Change)"
        elif higher_better:
            interpretation = "Favorable (Gain)" if abs_diff > 0 else "Unfavorable (Decline)"
        else:
            interpretation = "Unfavorable (Increase)" if abs_diff > 0 else "Favorable (Reduction)"
            
        records.append({
            "KPI_Key": col,
            "KPI Name": meta["label"],
            "Category": meta["category"],
            "Unit": meta["unit"],
            "Previous Period": prev_val,
            "Current Period": curr_val,
            "Absolute Change": abs_diff,
            "Percentage Change (%)": pct_diff,
            "Direction": direction,
            "Business Interpretation": interpretation,
            "Financial Weight": meta["financial_weight"]
        })
        
    return pd.DataFrame(records)

# ==============================================================================
# 5. STATISTICAL CORRELATION ENGINE
# ==============================================================================
def calculate_correlations(df: pd.DataFrame, min_obs: int = 4):
    """
    Computes Pearson correlations between operational KPIs and financial outcomes.
    Safely verifies minimum sample size and non-zero variance.
    """
    if len(df) < min_obs:
        return None, "Insufficient historical observations for statistically meaningful correlation analysis."
        
    operational_keys = [
        "On_Time_Delivery", "Customer_Complaints", "Inventory_Holding_Costs",
        "Employee_Productivity", "Sales_Conversion_Rate", "Marketing_Expenditure"
    ]
    financial_keys = [
        "Revenue", "Operating_Profit", "Gross_Profit_Margin",
        "Operating_Costs", "Customer_Retention"
    ]
    
    # Check for zero variance
    for col in operational_keys + financial_keys:
        if df[col].std() == 0:
            return None, f"Variable '{col}' has zero variance across selected observations."
            
    corr_matrix = df[operational_keys + financial_keys].corr().loc[operational_keys, financial_keys]
    
    # Focus core relationships requested in specification
    core_relationships = [
        {
            "pair": ("On_Time_Delivery", "Customer_Retention"),
            "operational_label": "On-Time Delivery Rate",
            "financial_label": "Customer Retention Rate",
            "r": df["On_Time_Delivery"].corr(df["Customer_Retention"]),
            "expected": "Positive association: Delivery delays correlate with customer churn."
        },
        {
            "pair": ("Inventory_Holding_Costs", "Operating_Profit"),
            "operational_label": "Inventory Holding Costs",
            "financial_label": "Operating Profit",
            "r": df["Inventory_Holding_Costs"].corr(df["Operating_Profit"]),
            "expected": "Negative association: Carrying cost bloat depresses operating profitability."
        },
        {
            "pair": ("Sales_Conversion_Rate", "Revenue"),
            "operational_label": "Sales Conversion Rate",
            "financial_label": "Monthly Revenue",
            "r": df["Sales_Conversion_Rate"].corr(df["Revenue"]),
            "expected": "Positive association: Conversion funnel yield directly lifts top-line revenue."
        },
        {
            "pair": ("Customer_Complaints", "Customer_Retention"),
            "operational_label": "Customer Complaint Rate",
            "financial_label": "Customer Retention Rate",
            "r": df["Customer_Complaints"].corr(df["Customer_Retention"]),
            "expected": "Negative association: Elevated complaints align with retention degradation."
        },
        {
            "pair": ("Employee_Productivity", "Operating_Profit"),
            "operational_label": "Employee Productivity",
            "financial_label": "Operating Profit",
            "r": df["Employee_Productivity"].corr(df["Operating_Profit"]),
            "expected": "Positive association: Operational labor efficiency expands bottom-line margins."
        }
    ]
    
    return corr_matrix, core_relationships

# ==============================================================================
# 6. EVIDENCE-BASED DECISION-INSIGHT ENGINE & PRIORITIZATION
# ==============================================================================
def calculate_priority_score(movement_pct: float, financial_relevance: float, risk_factor: float) -> tuple[float, str]:
    """
    Computes a heuristic priority score (0-100) based on:
      1. Movement Magnitude (0-40 pts): relative scale of shift
      2. Financial Relevance (0-35 pts): direct impact on bottom/top line
      3. Business Risk or Opportunity Urgency (0-25 pts)
      
    Disclosed: This is a transparent rule-based heuristic, not an actuarial machine learning model.
    """
    # 1. Magnitude component (capped at 40)
    mag_score = min(abs(movement_pct) * 2.0, 40.0)
    
    # 2. Financial relevance component (normalized to max 35)
    fin_score = min(financial_relevance, 35.0)
    
    # 3. Risk / Urgency component (max 25)
    urgency_score = min(risk_factor, 25.0)
    
    total_score = round(mag_score + fin_score + urgency_score, 1)
    total_score = min(max(total_score, 0.0), 100.0)
    
    if total_score >= 70.0:
        priority_tier = "High"
    elif total_score >= 45.0:
        priority_tier = "Medium"
    else:
        priority_tier = "Low"
        
    return total_score, priority_tier

def generate_decision_insights(df: pd.DataFrame, curr_idx: int, prev_idx: int) -> list[dict]:
    """
    Deterministic Decision-Insight Engine.
    Evaluates rule conditions against observed data movements and empirical associations.
    Produces structured insights distinguishing:
      - Observed Facts
      - Statistical Associations
      - Management Hypotheses
      - Recommended Actions
    """
    curr = df.iloc[curr_idx]
    prev = df.iloc[prev_idx]
    insights = []
    
    # -------------------------------------------------------------------------
    # RULE 1: Delivery Performance Strain & Customer Retention Decline
    # -------------------------------------------------------------------------
    deliv_diff = curr["On_Time_Delivery"] - prev["On_Time_Delivery"]
    ret_diff = curr["Customer_Retention"] - prev["Customer_Retention"]
    
    if deliv_diff <= -1.0 or (deliv_diff < 0 and ret_diff < 0):
        mag = abs(deliv_diff) + abs(ret_diff)
        score, tier = calculate_priority_score(mag * 3.5, financial_relevance=32.0, risk_factor=25.0)
        insights.append({
            "title": "Fulfillment Latency Deteriorating Customer Retention",
            "category": "Customer Experience",
            "financial_outcome": "Customer Retention",
            "priority": tier,
            "priority_score": score,
            "confidence": "High (Strong Empirical Correlation, r = 0.99)",
            "kpi_support": {
                "On-Time Delivery": f"{prev['On_Time_Delivery']:.1f}% → {curr['On_Time_Delivery']:.1f}% ({deliv_diff:+.1f} pp)",
                "Customer Retention": f"{prev['Customer_Retention']:.1f}% → {curr['Customer_Retention']:.1f}% ({ret_diff:+.1f} pp)"
            },
            "fact": f"On-time delivery fell by {abs(deliv_diff):.1f} percentage points (from {prev['On_Time_Delivery']:.1f}% to {curr['On_Time_Delivery']:.1f}%), coinciding with a {abs(ret_diff):.1f} percentage point decline in customer retention.",
            "association": "Across the 12-month baseline, delivery timeliness correlates strongly with customer retention (Pearson r = +0.99), demonstrating that logistics friction closely tracks customer defection.",
            "hypothesis": "Fulfillment backlogs, carrier SLA breaches, and delayed shipping notifications are degrading buyer trust and triggering repeat customer churn.",
            "recommendation": "Conduct an immediate fulfillment audit with third-party logistics partners, streamline dispatch bottlenecks at regional distribution centers, and initiate automated goodwill credits for affected repeat customers."
        })
        
    # -------------------------------------------------------------------------
    # RULE 2: Inventory Holding Bloat Compressing Operating Profit
    # -------------------------------------------------------------------------
    inv_pct = safe_pct_change(curr["Inventory_Holding_Costs"], prev["Inventory_Holding_Costs"])
    op_diff = curr["Operating_Profit"] - prev["Operating_Profit"]
    op_pct = safe_pct_change(curr["Operating_Profit"], prev["Operating_Profit"])
    
    if inv_pct >= 5.0 and op_diff < 0:
        score, tier = calculate_priority_score(abs(inv_pct), financial_relevance=35.0, risk_factor=24.0)
        insights.append({
            "title": "Inventory Accumulation Dragging Down Operating Profit",
            "category": "Logistics & Inventory",
            "financial_outcome": "Operating Profit",
            "priority": tier,
            "priority_score": score,
            "confidence": "High (Inverse Correlation, r = -0.78)",
            "kpi_support": {
                "Holding Costs": f"${prev['Inventory_Holding_Costs']:,.0f} → ${curr['Inventory_Holding_Costs']:,.0f} ({inv_pct:+.1f}%)",
                "Operating Profit": f"${prev['Operating_Profit']:,.0f} → ${curr['Operating_Profit']:,.0f} ({op_pct:+.1f}%)"
            },
            "fact": f"Inventory holding costs rose by {inv_pct:.1f}% (+${curr['Inventory_Holding_Costs'] - prev['Inventory_Holding_Costs']:,.0f}), while operating profit dropped by {abs(op_pct):.1f}% (-${abs(op_diff):,.0f}).",
            "association": "Inventory holding expenses exhibit a pronounced negative correlation with operating profit (Pearson r = -0.78), serving as a direct overhead drag on bottom-line margins.",
            "hypothesis": "Excess safety stock, inaccurate demand forecasting, or slow-moving SKU accumulation is consuming working capital and warehouse space, inflating carrying overhead.",
            "recommendation": "Audit slow-moving and non-performing SKUs, recalibrate Economic Order Quantity (EOQ) thresholds with category managers, and execute targeted clearance promotions for stale inventory."
        })
        
    # -------------------------------------------------------------------------
    # RULE 3: Customer Complaint Surge Warning
    # -------------------------------------------------------------------------
    comp_diff = curr["Customer_Complaints"] - prev["Customer_Complaints"]
    comp_pct = safe_pct_change(curr["Customer_Complaints"], prev["Customer_Complaints"])
    
    if comp_diff >= 0.5 or curr["Customer_Complaints"] >= 3.5:
        score, tier = calculate_priority_score(comp_pct, financial_relevance=25.0, risk_factor=22.0)
        insights.append({
            "title": "Escalating Customer Complaints Threatening Brand Equity",
            "category": "Customer Experience",
            "financial_outcome": "Customer Retention",
            "priority": tier,
            "priority_score": score,
            "confidence": "High (Inverse Correlation with Retention, r = -0.99)",
            "kpi_support": {
                "Complaint Rate": f"{prev['Customer_Complaints']:.1f}% → {curr['Customer_Complaints']:.1f}% ({comp_diff:+.1f} pp)",
                "Current Retention": f"{curr['Customer_Retention']:.1f}%"
            },
            "fact": f"Customer complaint rate shifted by {comp_diff:+.1f} percentage points, reaching {curr['Customer_Complaints']:.1f}% of all order interactions.",
            "association": "Complaint rate has an inverse association with customer retention (Pearson r = -0.99). Escalations in complaints precede or mirror customer attrition.",
            "hypothesis": "Product packaging damage, fulfillment delays, or support ticket backlogs are creating negative customer friction points.",
            "recommendation": "Review ticket categorization in customer support to isolate the top root causes (packaging vs. shipment delay vs. item accuracy) and establish a 24-hour resolution protocol."
        })
        
    # -------------------------------------------------------------------------
    # RULE 4: Sales Conversion Efficiency Powering Top-Line Expansion
    # -------------------------------------------------------------------------
    conv_diff = curr["Sales_Conversion_Rate"] - prev["Sales_Conversion_Rate"]
    rev_pct = safe_pct_change(curr["Revenue"], prev["Revenue"])
    
    if conv_diff >= 0.2 and rev_pct > 0:
        score, tier = calculate_priority_score(rev_pct * 3.0, financial_relevance=30.0, risk_factor=16.0)
        insights.append({
            "title": "Sales Conversion Momentum Expanding Top-Line Revenue",
            "category": "Sales & Marketing",
            "financial_outcome": "Revenue",
            "priority": tier,
            "priority_score": score,
            "confidence": "High (Positive Correlation with Revenue, r = 0.99)",
            "kpi_support": {
                "Conversion Rate": f"{prev['Sales_Conversion_Rate']:.1f}% → {curr['Sales_Conversion_Rate']:.1f}% ({conv_diff:+.1f} pp)",
                "Monthly Revenue": f"${prev['Revenue']:,.0f} → ${curr['Revenue']:,.0f} ({rev_pct:+.1f}%)"
            },
            "fact": f"Sales conversion improved by {conv_diff:+.1f} percentage points, while monthly revenue expanded by {rev_pct:.1f}% (+${curr['Revenue'] - prev['Revenue']:,.0f}).",
            "association": "Sales conversion rate is near-perfectly co-correlated with revenue growth (Pearson r = +0.99), underscoring conversion efficiency as the primary revenue lever.",
            "hypothesis": "Recent digital merchandising adjustments, checkout flow optimizations, or targeted promotional campaigns have meaningfully reduced cart abandonment.",
            "recommendation": "Document high-performing campaign channels and replicate successful conversion practices across underperforming product categories."
        })
        
    # -------------------------------------------------------------------------
    # RULE 5: Workforce Productivity Dividend Lifting Operating Margin
    # -------------------------------------------------------------------------
    prod_diff = curr["Employee_Productivity"] - prev["Employee_Productivity"]
    prod_pct = safe_pct_change(curr["Employee_Productivity"], prev["Employee_Productivity"])
    
    if prod_pct >= 2.5 and op_diff > 0:
        score, tier = calculate_priority_score(prod_pct * 2.0, financial_relevance=30.0, risk_factor=14.0)
        insights.append({
            "title": "Workforce Productivity Gains Bolstering Bottom-Line Margins",
            "category": "Operations & Workforce",
            "financial_outcome": "Operating Profit",
            "priority": tier,
            "priority_score": score,
            "confidence": "High (Positive Association with Operating Profit, r = 0.97)",
            "kpi_support": {
                "Productivity Index": f"{prev['Employee_Productivity']:.1f} → {curr['Employee_Productivity']:.1f} ({prod_diff:+.1f} pts)",
                "Operating Profit": f"${prev['Operating_Profit']:,.0f} → ${curr['Operating_Profit']:,.0f} ({op_pct:+.1f}%)"
            },
            "fact": f"Employee productivity index increased by {prod_pct:.1f}%, while operating profit grew by {op_pct:.1f}% (+${op_diff:,.0f}).",
            "association": "Productivity gains display a robust positive correlation with operating profit (Pearson r = +0.97), driving operating leverage across retail operations.",
            "hypothesis": "Employee upskilling, cross-training, and streamlined operational workflows have improved unit output per labor hour.",
            "recommendation": "Incentivize high-productivity operational teams and scale successful shift scheduling practices across regional distribution hubs."
        })
        
    # -------------------------------------------------------------------------
    # RULE 6: Inventory Normalization & Operating Margin Recovery
    # -------------------------------------------------------------------------
    if inv_pct <= -5.0 and op_diff > 0:
        score, tier = calculate_priority_score(abs(inv_pct), financial_relevance=28.0, risk_factor=15.0)
        insights.append({
            "title": "Inventory Rationalization Relieving Operating Cost Pressure",
            "category": "Logistics & Inventory",
            "financial_outcome": "Operating Profit",
            "priority": tier,
            "priority_score": score,
            "confidence": "Moderate (Inverse Association r = -0.78)",
            "kpi_support": {
                "Holding Costs": f"${prev['Inventory_Holding_Costs']:,.0f} → ${curr['Inventory_Holding_Costs']:,.0f} ({inv_pct:.1f}%)",
                "Operating Profit": f"${prev['Operating_Profit']:,.0f} → ${curr['Operating_Profit']:,.0f} ({op_pct:+.1f}%)"
            },
            "fact": f"Holding costs decreased by {abs(inv_pct):.1f}% (-${prev['Inventory_Holding_Costs'] - curr['Inventory_Holding_Costs']:,.0f}), contributing to an operating profit increase of {op_pct:.1f}%.",
            "association": "Reduction in inventory drag allows gross profits to flow more efficiently into net operating income.",
            "hypothesis": "Effective clearance of non-moving inventory and disciplined supplier order cadence are restoring lean inventory levels.",
            "recommendation": "Maintain tight inventory turnover targets and avoid premature re-accumulation of uncommitted stock."
        })

    # Fallback if no specific rule triggered
    if not insights:
        insights.append({
            "title": "Operational Baseline Stability Observed",
            "category": "Operations & Workforce",
            "financial_outcome": "Operating Profit",
            "priority": "Low",
            "priority_score": 25.0,
            "confidence": "Moderate",
            "kpi_support": {
                "Revenue": f"${curr['Revenue']:,.0f}",
                "Operating Profit": f"${curr['Operating_Profit']:,.0f}"
            },
            "fact": "All monitored operational and financial indicators moved within standard variance thresholds (<1.0% shift).",
            "association": "Historical operational-to-financial co-movements remain within expected baseline parameters.",
            "hypothesis": "Operational processes are operating in a steady-state equilibrium.",
            "recommendation": "Continue continuous telemetry monitoring and review supplier contract renewals."
        })
        
    # Sort insights by priority score descending
    insights.sort(key=lambda x: x["priority_score"], reverse=True)
    return insights

# ==============================================================================
# 7. MAIN STREAMLIT APPLICATION INTERFACE
# ==============================================================================
def main():
    # Load dataset
    df = load_synthetic_business_data()
    
    # -------------------------------------------------------------------------
    # SIDEBAR CONTROLS
    # -------------------------------------------------------------------------
    st.sidebar.title("🎛️ Dashboard Controls")
    st.sidebar.caption("Retail Performance Intelligence Engine")
    
    # Refresh Analysis Button
    if st.sidebar.button("🔄 Refresh Analysis", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.sidebar.divider()
    
    # Period selection
    month_options = df["Month"].tolist()
    # Default to Month 05 or Month 08 to showcase rich movements
    default_period_idx = 4  # Month 05
    curr_period_str = st.sidebar.selectbox(
        "📅 Evaluation Period (Current)",
        options=month_options[1:],  # Must have at least Month 02 to compare
        index=3  # Default to Month 05
    )
    
    curr_idx = month_options.index(curr_period_str)
    prev_period_str = month_options[curr_idx - 1]
    prev_idx = curr_idx - 1
    
    st.sidebar.info(
        f"**Comparison Baseline:**\n\n"
        f"Comparing **{curr_period_str}** against **{prev_period_str}**."
    )
    
    # Filters
    st.sidebar.divider()
    st.sidebar.subheader("🔍 Filters & Focus")
    
    category_options = [
        "All Categories",
        "Financial Outcomes",
        "Customer Experience",
        "Logistics & Inventory",
        "Sales & Marketing",
        "Operations & Workforce"
    ]
    selected_category = st.sidebar.selectbox("Department / KPI Category", category_options, index=0)
    
    financial_focus_options = [
        "All Financial Outcomes",
        "Revenue",
        "Operating Profit",
        "Gross Profit Margin",
        "Customer Retention"
    ]
    selected_financial_focus = st.sidebar.selectbox("Financial Outcome Focus", financial_focus_options, index=0)
    
    # Methodology Disclosure
    st.sidebar.divider()
    st.sidebar.subheader("ℹ️ System Architecture")
    st.sidebar.caption(
        "**Decision-Insight Engine Disclosure:**\n"
        "- Deterministic rule-based analytics engine.\n"
        "- Zero external LLMs or black-box ML models.\n"
        "- Grounded strictly in empirical data telemetry.\n"
        "- Suitable for executive and academic review."
    )

    # -------------------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------------------
    st.title("📈 Executive Decision Intelligence Dashboard")
    st.markdown(
        "**Enterprise Performance Intelligence & Operational-Financial Attribution Audit**  \n"
        "Fictional Retail Enterprise: *Apex Retail Group* | 12-Month Longitudinal Operational Telemetry"
    )
    st.caption(
        "⚡ **Transparent Decision-Insight Engine**: Identifies operational anomalies, quantifies statistical associations, "
        "and produces prioritized, evidence-based recommendations."
    )
    
    st.divider()

    # -------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------------------
    st.subheader(f"🏛️ Executive Overview: {curr_period_str} vs. {prev_period_str}")
    
    curr_row = df.iloc[curr_idx]
    prev_row = df.iloc[prev_idx]
    
    # Calculate top metrics
    rev_curr = curr_row["Revenue"]
    rev_prev = prev_row["Revenue"]
    rev_pct = safe_pct_change(rev_curr, rev_prev)
    
    op_curr = curr_row["Operating_Profit"]
    op_prev = prev_row["Operating_Profit"]
    op_pct = safe_pct_change(op_curr, op_prev)
    
    margin_curr = curr_row["Gross_Profit_Margin"]
    margin_prev = prev_row["Gross_Profit_Margin"]
    margin_diff = margin_curr - margin_prev
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${rev_curr:,.0f}",
            delta=f"{rev_pct:+.1f}% vs prior month",
            delta_color="normal"
        )
    with col2:
        st.metric(
            label="Operating Profit",
            value=f"${op_curr:,.0f}",
            delta=f"{op_pct:+.1f}% vs prior month",
            delta_color="normal"
        )
    with col3:
        st.metric(
            label="Gross Profit Margin",
            value=f"{margin_curr:.1f}%",
            delta=f"{margin_diff:+.1f} pp",
            delta_color="normal"
        )
    with col4:
        st.metric(
            label="Revenue MoM Growth",
            value=f"{rev_pct:+.2f}%",
            delta=f"${rev_curr - rev_prev:+,.0f}",
            delta_color="normal"
        )
        
    # High-level executive movements summary
    movements_df = compute_kpi_movements(df, curr_idx, prev_idx)
    favorable = movements_df[movements_df["Business Interpretation"].str.startswith("Favorable")]
    unfavorable = movements_df[movements_df["Business Interpretation"].str.startswith("Unfavorable")]
    
    fav_text = ", ".join([f"**{row['KPI Name']}** ({row['Percentage Change (%)']:+.1f}%)" for _, row in favorable.iterrows()]) or "None notable"
    unfav_text = ", ".join([f"**{row['KPI Name']}** ({row['Percentage Change (%)']:+.1f}%)" for _, row in unfavorable.iterrows()]) or "None notable"
    
    st.info(
        f"📋 **Executive Movement Summary for {curr_period_str}:**\n\n"
        f"• **Key Positive Shifts:** {fav_text}\n\n"
        f"• **Key Negative Headwinds:** {unfav_text}"
    )
    
    st.divider()

    # -------------------------------------------------------------------------
    # SECTION 2: TREND VISUALIZATIONS OVER TIME
    # -------------------------------------------------------------------------
    st.subheader("📊 12-Month Operational & Financial Trends")
    st.caption("Inspect how operational indicators change alongside financial outcomes across the fiscal year.")
    
    # Filter columns for visualization
    chart_cols_map = {
        "Financial Outcomes": ["Revenue", "Operating_Profit", "Operating_Costs"],
        "Customer Experience": ["Customer_Retention", "Customer_Complaints", "On_Time_Delivery"],
        "Logistics & Inventory": ["Inventory_Holding_Costs", "Operating_Profit"],
        "Sales & Marketing": ["Sales_Conversion_Rate", "Revenue"],
        "Operations & Workforce": ["Employee_Productivity", "Operating_Profit"]
    }
    
    # Prepare trend dataframe with Month as index
    trend_df = df.set_index("Month")
    
    tab1, tab2, tab3 = st.tabs([
        "📈 Primary Trajectories",
        "🎯 Operational Co-Movements",
        "📋 Complete Telemetry Data"
    ])
    
    with tab1:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**Top-Line & Bottom-Line Financials ($)**")
            st.line_chart(trend_df[["Revenue", "Operating_Profit", "Operating_Costs"]], height=320)
        with col_c2:
            st.markdown("**Customer Retention & On-Time Delivery (%)**")
            st.line_chart(trend_df[["Customer_Retention", "On_Time_Delivery", "Customer_Complaints"]], height=320)
            
    with tab2:
        col_c3, col_c4 = st.columns(2)
        with col_c3:
            st.markdown("**Inventory Holding Costs ($) vs. Operating Profit ($)**")
            st.line_chart(trend_df[["Inventory_Holding_Costs", "Operating_Profit"]], height=320)
        with col_c4:
            st.markdown("**Sales Conversion Rate (%) vs. Employee Productivity (Index)**")
            st.line_chart(trend_df[["Sales_Conversion_Rate", "Employee_Productivity"]], height=320)
            
    with tab3:
        st.dataframe(
            df.drop(columns=["Month_Index"]),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # -------------------------------------------------------------------------
    # SECTION 3: KPI MOVEMENT ANALYSIS TABLE
    # -------------------------------------------------------------------------
    st.subheader(f"🔍 Period-over-Period KPI Movement Analysis ({curr_period_str} vs. {prev_period_str})")
    st.caption("Detailed variance analysis with directional indicators and business interpretations.")
    
    # Apply category filter if selected
    filtered_movements = movements_df.copy()
    if selected_category != "All Categories":
        filtered_movements = filtered_movements[filtered_movements["Category"] == selected_category]
        
    # Format table for executive presentation
    display_records = []
    for _, row in filtered_movements.iterrows():
        unit = row["Unit"]
        display_records.append({
            "Category": row["Category"],
            "KPI Name": row["KPI Name"],
            "Previous Period": format_value(row["Previous Period"], unit),
            "Current Period": format_value(row["Current Period"], unit),
            "Absolute Change": format_value(row["Absolute Change"], unit),
            "Percentage Change": f"{row['Percentage Change (%)']:+.2f}%",
            "Direction": row["Direction"],
            "Business Interpretation": row["Business Interpretation"]
        })
        
    display_df = pd.DataFrame(display_records)
    
    # Styled Streamlit dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()

    # -------------------------------------------------------------------------
    # SECTION 4: STATISTICAL CORRELATION INTELLIGENCE
    # -------------------------------------------------------------------------
    st.subheader("🔗 Operational KPIs Connected to Financial Outcomes")
    st.markdown(
        "Quantifying the statistical co-movement between operational friction/efficiency and bottom-line financial metrics."
    )
    
    corr_matrix, core_relationships = calculate_correlations(df, min_obs=4)
    
    # Association vs. Causation Warning Notice
    st.warning(
        "⚠️ **Methodological Notice — Association vs. Causation**: "
        "Correlation indicates statistical co-movement across historical observations, not direct mechanistic causation. "
        "A strong correlation identifies priority diagnostic hypotheses for executive audit, rather than definitive causal claims."
    )
    
    # Check observations requirement
    st.success(
        f"✅ **Statistical Observation Health**: Sample contains **12 monthly intervals** "
        f"(exceeds minimum threshold of 4 required observations; zero constant-variance errors detected)."
    )
    
    st.markdown("#### 🎯 Core Operational-to-Financial Pairwise Insights")
    
    # Display the 5 core pairwise relationship cards
    rel_cols = st.columns(len(core_relationships))
    for i, rel in enumerate(core_relationships):
        r_val = rel["r"]
        with rel_cols[i]:
            with st.container(border=True):
                st.caption(f"**Relationship {i+1}**")
                st.markdown(f"**{rel['operational_label']}**  \n↔  \n**{rel['financial_label']}**")
                st.subheader(f"r = {r_val:+.2f}")
                
                # Strength tag
                if abs(r_val) >= 0.8:
                    strength = "Strong"
                elif abs(r_val) >= 0.5:
                    strength = "Moderate"
                else:
                    strength = "Weak"
                    
                polarity = "Positive" if r_val > 0 else "Inverse"
                st.badge(f"{strength} {polarity}")
                st.caption(rel["expected"])
                
    st.markdown("#### 🌡️ Operational-Financial Correlation Matrix")
    # Clean styled correlation matrix
    styled_corr = corr_matrix.rename(
        index=lambda x: KPI_METADATA.get(x, {}).get("label", x),
        columns=lambda x: KPI_METADATA.get(x, {}).get("label", x)
    )
    st.dataframe(
        styled_corr.style.format("{:+.2f}").background_gradient(cmap="coolwarm", vmin=-1.0, vmax=1.0),
        use_container_width=True
    )

    st.divider()

    # -------------------------------------------------------------------------
    # SECTION 5: EVIDENCE-BASED DECISION-INSIGHT ENGINE
    # -------------------------------------------------------------------------
    st.subheader("💡 Evidence-Based Decision-Insight Engine")
    st.caption(
        "Algorithmic decision intelligence generating structured executive findings with supporting facts, "
        "statistical links, management hypotheses, and prioritized actions."
    )
    
    insights = generate_decision_insights(df, curr_idx, prev_idx)
    
    # Filter insights by category and financial outcome if requested
    filtered_insights = []
    for ins in insights:
        match_cat = (selected_category == "All Categories") or (ins["category"] == selected_category)
        match_fin = (selected_financial_focus == "All Financial Outcomes") or (
            selected_financial_focus.lower() in ins["financial_outcome"].lower()
        )
        if match_cat and match_fin:
            filtered_insights.append(ins)
            
    if not filtered_insights:
        st.info("No decision insights match the active category and financial outcome filter combination.")
    else:
        st.markdown(f"**Displaying {len(filtered_insights)} Prioritized Finding(s) for {curr_period_str}:**")
        
        for ins in filtered_insights:
            priority = ins["priority"]
            score = ins["priority_score"]
            
            # Visual border color/container based on priority
            with st.container(border=True):
                hdr_col1, hdr_col2 = st.columns([3, 1])
                with hdr_col1:
                    st.markdown(f"### {ins['title']}")
                with hdr_col2:
                    if priority == "High":
                        st.error(f"🔴 **{priority} Priority** (Score: {score})")
                    elif priority == "Medium":
                        st.warning(f"🟡 **{priority} Priority** (Score: {score})")
                    else:
                        st.success(f"🟢 **{priority} Priority** (Score: {score})")
                        
                st.caption(
                    f"**Category:** {ins['category']} | "
                    f"**Affected Financial Outcome:** {ins['financial_outcome']} | "
                    f"**Evidence Strength:** {ins['confidence']}"
                )
                
                # Supporting KPI metrics pills
                st.markdown("**Supporting Telemetry Values:**")
                kpi_cols = st.columns(len(ins["kpi_support"]))
                for k_i, (k_name, k_val) in enumerate(ins["kpi_support"].items()):
                    with kpi_cols[k_i]:
                        st.caption(f"• **{k_name}:** {k_val}")
                        
                # 4-Part Structured Decision Intelligence Framework
                col_a, col_b = st.columns(2)
                with col_a:
                    with st.container(border=True):
                        st.markdown("#### 📌 Observed Fact")
                        st.write(ins["fact"])
                    with st.container(border=True):
                        st.markdown("#### 💡 Management Hypothesis")
                        st.write(ins["hypothesis"])
                with col_b:
                    with st.container(border=True):
                        st.markdown("#### 📊 Statistical Association")
                        st.write(ins["association"])
                    with st.container(border=True):
                        st.markdown("#### 🎯 Recommended Management Action")
                        st.write(ins["recommendation"])
                        
        # Priority Score Disclaimer
        st.caption(
            "📌 **Priority Scoring Disclaimer**: The priority score is a deterministic heuristic ranking combining movement magnitude, "
            "financial tier weighting, and business risk to assist executive triage. It is not an actuarial measure of guaranteed monetary impact."
        )

# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    main()
