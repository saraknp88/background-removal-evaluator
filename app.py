import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Page configuration
st.set_page_config(
    page_title="Sara's Enterprise Background Removal Evaluator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for React-like styling and vertical layout
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .criteria-list {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
    }
    .celebration {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 1rem;
        color: white;
        margin: 2rem 0;
    }
    
    /* React-like vertical radio buttons */
    .vertical-radio {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .radio-option {
        display: flex;
        align-items: flex-start;
        padding: 12px;
        margin-bottom: 8px;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: white;
    }
    
    .radio-option:hover {
        border-color: #d1d5db;
        background: #f9fafb;
    }
    
    .radio-option.selected-1 {
        border-color: #dc2626;
        background: #fef2f2;
        color: #7f1d1d;
    }
    
    .radio-option.selected-2 {
        border-color: #ea580c;
        background: #fff7ed;
        color: #9a3412;
    }
    
    .radio-option.selected-3 {
        border-color: #ca8a04;
        background: #fffbeb;
        color: #92400e;
    }
    
    .radio-option.selected-4 {
        border-color: #2563eb;
        background: #eff6ff;
        color: #1e40af;
    }
    
    .radio-option.selected-5 {
        border-color: #16a34a;
        background: #f0fdf4;
        color: #15803d;
    }
    
    .radio-content {
        margin-left: 8px;
        flex: 1;
    }
    
    .radio-label {
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .radio-description {
        font-size: 0.875rem;
        color: #6b7280;
        line-height: 1.4;
    }
    
    .view-mode-buttons {
        display: flex;
        gap: 8px;
        margin-bottom: 1rem;
    }
    
    .view-mode-btn {
        padding: 6px 12px;
        font-size: 0.75rem;
        border-radius: 4px;
        border: 1px solid #d1d5db;
        background: #f3f4f6;
        color: #374151;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .view-mode-btn.active {
        background: #dbeafe;
        color: #1d4ed8;
        border-color: #3b82f6;
    }
    
    .image-container {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .note-box {
        background: #fef3c7;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
        border: 1px solid #f59e0b;
    }
    
    /* Hide Streamlit radio button default styling */
    .stRadio > div {
        display: none !important;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #3b82f6;
    }
    
    /* Button styling */
    .stButton > button[kind="primary"] {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    
    .stButton > button[kind="secondary"] {
        background-color: #f3f4f6;
        border-color: #d1d5db;
        color: #374151;
    }
    
    /* Fireworks animation */
    @keyframes firework {
        0% { transform: scale(0) rotate(0deg); opacity: 1; }
        50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
        100% { transform: scale(0) rotate(360deg); opacity: 0; }
    }
    
    @keyframes float-up {
        0% { transform: translateY(0px); opacity: 1; }
        100% { transform: translateY(-100px); opacity: 0; }
    }
    
    .firework {
        position: fixed;
        font-size: 2rem;
        animation: firework 2s ease-out;
        pointer-events: none;
        z-index: 1000;
    }
    
    .floating-emoji {
        position: fixed;
        font-size: 1.5rem;
        animation: float-up 3s ease-out;
        pointer-events: none;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'evaluation_complete' not in st.session_state:
    st.session_state.evaluation_complete = False
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Side-by-Side"

# Image data with working URLs
images = [
    {
        "id": 1,
        "name": "Professional Portrait",
        "original": "https://i.imgur.com/YG29M6I.png",
        "processed": "https://i.imgur.com/xW3oobT.png"
    },
    {
        "id": 2,
        "name": "Business Attire",
        "original": "https://i.imgur.com/Mxyf5Tt.png",
        "processed": "https://i.imgur.com/bqx1bWu.png"
    },
    {
        "id": 3,
        "name": "Product - Smartphone",
        "original": "https://i.imgur.com/NKBdsXV.png",
        "processed": "https://i.imgur.com/NUTQwWT.png"
    },
    {
        "id": 4,
        "name": "Steak Dish",
        "original": "https://i.imgur.com/DLokTft.png",
        "processed": "https://i.imgur.com/FN6GcEf.png"
    },
    {
        "id": 5,
        "name": "Product - Coffee Cup",
        "original": "https://i.imgur.com/ad5dEgm.png",
        "processed": "https://i.imgur.com/wobxzdf.png"
    }
]

# Quality scale definitions with colors matching React version
quality_scales = [
    {"value": 1, "label": "Unusable", "description": "Major issues with structure, style, identity, or overall quality. Not suitable for use.", "color": "#dc2626"},
    {"value": 2, "label": "Partially Viable", "description": "Useful as a concept or direction, but not for final use. Significant fixes required.", "color": "#ea580c"},
    {"value": 3, "label": "Moderately Functional", "description": "Largely usable, with moderate fixes needed. More efficient than starting from scratch.", "color": "#ca8a04"},
    {"value": 4, "label": "Near Production Ready", "description": "Only minor adjustments needed, such as light cleanup or retouching.", "color": "#2563eb"},
    {"value": 5, "label": "Production Ready", "description": "No further edits needed. Ready for immediate use.", "color": "#16a34a"}
]

def create_celebration_animation():
    """Create animated celebration effect that runs for 3 seconds"""
    # Create celebration HTML with limited duration animations
    celebration_html = """
    <div class="celebration">
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🎉 Evaluation Complete! 🎉</h1>
        <h2 style="font-size: 1.5rem; margin-bottom: 1rem;">Thank you for your participation!</h2>
        <p style="font-size: 1.1rem;">Your responses have been recorded successfully.</p>
    </div>
    """
    
    st.markdown(celebration_html, unsafe_allow_html=True)
    
    # Show celebration emojis with limited animation
    emoji_cols = st.columns(8)
    celebration_emojis = ["🎊", "✨", "🎈", "🌟", "🎆", "🏆", "👏", "🥳"]
    for i, emoji in enumerate(celebration_emojis):
        with emoji_cols[i]:
            st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{emoji}</h1>", 
                       unsafe_allow_html=True)
    
    # Create a brief fireworks effect using Streamlit's built-in features
    if 'celebration_shown' not in st.session_state:
        st.session_state.celebration_shown = True
        
        # Show balloons for 3 seconds
        st.balloons()
        
        # Brief message
        with st.empty():
            for i in range(3):
                st.success(f"🎉 Celebration! Thank you for your evaluation! 🎉")
                time.sleep(1)
            st.empty()  # Clear the message

def custom_radio_buttons(current_rating):
    """Create custom vertical radio buttons matching React design"""
    st.markdown("### Rate the quality of the \"Background Removal Result\" image:")
    
    # Create vertical radio buttons using pure Streamlit approach
    selected_rating = None
    
    for scale in quality_scales:
        # Create container for each option
        container = st.container()
        
        with container:
            # Apply selected styling based on current rating
            if current_rating == scale['value']:
                bg_color = {
                    1: "#fef2f2", 2: "#fff7ed", 3: "#fffbeb", 4: "#eff6ff", 5: "#f0fdf4"
                }[scale['value']]
                border_color = scale['color']
                text_color = {
                    1: "#7f1d1d", 2: "#9a3412", 3: "#92400e", 4: "#1e40af", 5: "#15803d"
                }[scale['value']]
            else:
                bg_color = "#ffffff"
                border_color = "#e5e7eb"
                text_color = "#374151"
            
            # Custom styled container for each option
            st.markdown(f"""
            <div style="
                padding: 12px;
                margin-bottom: 8px;
                border: 2px solid {border_color};
                border-radius: 8px;
                background: {bg_color};
                color: {text_color};
                cursor: pointer;
                transition: all 0.2s ease;
            ">
                <div style="font-weight: 600; margin-bottom: 4px;">
                    {scale['value']} - {scale['label']}
                </div>
                <div style="font-size: 0.875rem; color: #6b7280; line-height: 1.4;">
                    {scale['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Invisible button to capture clicks
            if st.button(f"Select {scale['value']}", key=f"rating_{scale['value']}", 
                        help=f"Rate as {scale['label']}", 
                        label_visibility="collapsed"):
                selected_rating = scale['value']
    
    return selected_rating

def create_view_mode_buttons():
    """Create custom view mode buttons"""
    st.markdown('<div class="view-mode-buttons">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
    
    with col1:
        if st.button("Side-by-Side", key="side_by_side", 
                    type="primary" if st.session_state.view_mode == "Side-by-Side" else "secondary"):
            st.session_state.view_mode = "Side-by-Side"
            st.rerun()
    
    with col2:
        if st.button("Original Only", key="original_only",
                    type="primary" if st.session_state.view_mode == "Original Only" else "secondary"):
            st.session_state.view_mode = "Original Only"
            st.rerun()
    
    with col3:
        if st.button("Processed Only", key="processed_only",
                    type="primary" if st.session_state.view_mode == "Processed Only" else "secondary"):
            st.session_state.view_mode = "Processed Only"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_analysis():
    """Calculate comprehensive analysis of ratings"""
    if not st.session_state.ratings:
        return None
    
    scores = list(st.session_state.ratings.values())
    average = sum(scores) / len(scores)
    percentage = (average / 5) * 100
    
    # Calculate distribution
    distribution = {i: scores.count(i) for i in range(1, 6)}
    total = len(scores)
    distribution_percent = {i: (distribution[i] / total) * 100 if total > 0 else 0 for i in range(1, 6)}
    
    # Generate executive summary
    high_quality = distribution_percent[4] + distribution_percent[5]
    low_quality = distribution_percent[1] + distribution_percent[2]
    passes = average >= 4
    
    if passes and high_quality >= 80:
        summary = "The background removal system demonstrates excellent performance with the majority of results meeting production standards. This technology is ready for enterprise deployment with minimal quality concerns."
    elif passes and high_quality >= 60:
        summary = "The background removal system shows strong performance with most results approaching production readiness. Minor refinements could further improve consistency across diverse image types."
    elif average >= 3 and low_quality <= 30:
        summary = "The background removal system delivers moderately functional results that can accelerate production workflows. Additional development is recommended to achieve consistent enterprise-grade quality standards."
    elif low_quality >= 50:
        summary = "The background removal system shows significant limitations with many results requiring substantial manual correction. Major algorithmic improvements are needed before enterprise deployment."
    else:
        summary = "The background removal system produces mixed results with inconsistent quality across different image types. Further optimization is required to meet enterprise production standards."
    
    # Add threshold context
    threshold_text = " The system meets the production readiness threshold with scores exceeding the required 4.0 (80%) standard." if passes else " The system falls below the production readiness threshold, which requires an average score of at least 4.0 (80%)."
    
    performance_context = " A significant portion of results demonstrate moderate performance, indicating potential for improvement with targeted optimization." if distribution_percent[3] >= 50 else ""
    
    summary += threshold_text + performance_context
    
    return {
        'scores': scores,
        'average': average,
        'percentage': percentage,
        'passes': passes,
        'distribution': distribution,
        'distribution_percent': distribution_percent,
        'summary': summary,
        'total_images': len(images)
    }

def reset_evaluation():
    """Reset the evaluation to start over"""
    st.session_state.current_image = 0
    st.session_state.ratings = {}
    st.session_state.show_analysis = False
    st.session_state.evaluation_complete = False
    st.session_state.view_mode = "Side-by-Side"
    if 'celebration_shown' in st.session_state:
        del st.session_state.celebration_shown

# Main application logic
if st.session_state.show_analysis:
    # Analysis Page
    analysis = calculate_analysis()
    
    st.markdown('<h1 class="main-header">Background Removal Quality Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Performance evaluation dashboard</p>', unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown("### Executive Summary")
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-bottom: 1.5rem;">
        {analysis['summary']}
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Images Evaluated",
            value=analysis['total_images']
        )
    
    with col2:
        st.metric(
            label="Average Score",
            value=f"{analysis['average']:.2f}/5",
            delta=f"{analysis['percentage']:.1f}%"
        )
    
    with col3:
        status = "✅ Meets Standard" if analysis['passes'] else "❌ Below Standard"
        st.metric(
            label="Quality Status",
            value=status
        )
    
    # Rating Distribution Chart
    st.markdown("### Rating Distribution")
    
    # Create distribution chart with React colors
    rating_labels = [f"{i} - {quality_scales[i-1]['label']}" for i in range(1, 6)]
    distribution_values = [analysis['distribution'][i] for i in range(1, 6)]
    colors = [quality_scales[i-1]['color'] for i in range(1, 6)]
    
    fig = px.bar(
        x=rating_labels,
        y=distribution_values,
        title="Distribution of Quality Ratings",
        labels={'x': 'Rating Category', 'y': 'Number of Images'},
        color=rating_labels,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        title_x=0.5
    )
    
    # Add percentage annotations
    for i, v in enumerate(distribution_values):
        if v > 0:
            percentage = analysis['distribution_percent'][i+1]
            fig.add_annotation(
                x=i,
                y=v + 0.1,
                text=f"{percentage:.1f}%",
                showarrow=False,
                font=dict(size=12, color="black")
            )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Start New Evaluation", type="secondary"):
            reset_evaluation()
            st.rerun()
    
    with col2:
        if st.button("📊 Back to Results", type="secondary"):
            st.session_state.show_analysis = False
            st.rerun()

elif st.session_state.evaluation_complete:
    # Thank You Page with animated celebration
    create_celebration_animation()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 View Analysis", type="primary"):
            st.session_state.show_analysis = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Start New Evaluation", type="secondary"):
            reset_evaluation()
            st.rerun()

else:
    # Main Evaluation Page
    st.markdown('<h1 class="main-header">Sara\'s Enterprise Background Removal Evaluator</h1>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div class="criteria-list">
        <strong>Assess AI-generated background removal results for production readiness. Rate each image from 1 to 5 based on:</strong>
        <ul>
            <li><strong>Edge quality</strong></li>
            <li><strong>Artifact removal</strong></li>
            <li><strong>Professional appearance</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    current_img = st.session_state.current_image
    total_imgs = len(images)
    progress = (current_img + 1) / total_imgs
    
    st.progress(progress)
    st.markdown(f"**Image {current_img + 1} of {total_imgs}: {images[current_img]['name']}**")
    
    # View mode selection with custom buttons
    st.markdown("**View Mode:**")
    create_view_mode_buttons()
    
    # Display images in container
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    
    if st.session_state.view_mode == "Side-by-Side":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Image**")
            st.image(images[current_img]['original'], use_container_width=True)
        
        with col2:
            st.markdown("**Background Removal Result**")
            st.image(images[current_img]['processed'], use_container_width=True)
    
    elif st.session_state.view_mode == "Original Only":
        st.markdown("**Original Image**")
        st.image(images[current_img]['original'], use_container_width=True)
    
    else:  # Processed Only
        st.markdown("**Background Removal Result**")
        st.image(images[current_img]['processed'], use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rating section with custom vertical layout
    current_rating = st.session_state.ratings.get(current_img, 0)
    selected_rating = custom_radio_buttons(current_rating)
    
    if selected_rating:
        st.session_state.ratings[current_img] = selected_rating
        st.rerun()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_img > 0:
            if st.button("⬅️ Previous", type="secondary"):
                st.session_state.current_image -= 1
                st.rerun()
    
    with col3:
        if current_rating > 0:  # Only allow navigation if rated
            if current_img < total_imgs - 1:
                if st.button("Next ➡️", type="primary"):
                    st.session_state.current_image += 1
                    st.rerun()
            else:
                if st.button("🎯 Submit Evaluation", type="primary"):
                    st.session_state.evaluation_complete = True
                    st.rerun()
    
    # Note
    st.markdown("""
    <div class="note-box">
        <small><strong>Note:</strong> You are now evaluating real background removal results. Rate the quality of the processed images based on edge quality, artifact removal, and professional appearance.</small>
    </div>
    """, unsafe_allow_html=True)
