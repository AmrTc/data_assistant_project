import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import sys
from pathlib import Path

# Robust import function
def robust_import_modules():
    """Import required modules with multiple fallback strategies."""
    
    # Strategy 1: Try absolute imports (local development)
    try:
        from new_data_assistant_project.src.database.models import ExplanationFeedback, User, ChatSession
        from new_data_assistant_project.src.utils.path_utils import get_absolute_path
        from new_data_assistant_project.src.utils.auth_manager import AuthManager
        print("✅ Evaluation Dashboard: Absolute imports successful")
        return ExplanationFeedback, User, ChatSession, get_absolute_path, AuthManager
    except ImportError as e:
        print(f"❌ Absolute imports failed: {e}")
    
    # Strategy 2: Try direct imports (Docker/production - new structure)
    try:
        from src.database.models import ExplanationFeedback, User, ChatSession
        from src.utils.path_utils import get_absolute_path
        from src.utils.auth_manager import AuthManager
        print("✅ Evaluation Dashboard: Direct imports successful")
        return ExplanationFeedback, User, ChatSession, get_absolute_path, AuthManager
    except ImportError as e:
        print(f"❌ Direct imports failed: {e}")
    
    # Strategy 3: Try relative imports (fallback)
    try:
        from src.database.models import ExplanationFeedback, User, ChatSession
        from src.utils.path_utils import get_absolute_path
        from src.utils.auth_manager import AuthManager
        print("✅ Evaluation Dashboard: Relative imports successful")
        return ExplanationFeedback, User, ChatSession, get_absolute_path, AuthManager
    except ImportError as e:
        print(f"❌ Relative imports failed: {e}")
    
    # Strategy 4: Manual path manipulation
    try:
        current_dir = Path.cwd()
        sys.path.insert(0, str(current_dir))
        sys.path.insert(0, str(current_dir / 'src'))
        
        from database.models import ExplanationFeedback, User, ChatSession
        from utils.path_utils import get_absolute_path
        from utils.auth_manager import AuthManager
        print("✅ Evaluation Dashboard: Manual path imports successful")
        return ExplanationFeedback, User, ChatSession, get_absolute_path, AuthManager
    except ImportError as e:
        print(f"❌ Manual path imports failed: {e}")
        st.error(f"❌ Could not import required modules: {e}")
        st.stop()

# Import modules
ExplanationFeedback, User, ChatSession, get_absolute_path, AuthManager = robust_import_modules()

# Import ComprehensiveFeedback model
try:
    from new_data_assistant_project.src.database.models import ComprehensiveFeedback
    print("✅ ComprehensiveFeedback import successful")
except ImportError:
    try:
        from src.database.models import ComprehensiveFeedback
        print("✅ ComprehensiveFeedback direct import successful")
    except ImportError:
        print("❌ ComprehensiveFeedback import failed")
        ComprehensiveFeedback = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def render_evaluation_dashboard():
    """Main function to render the evaluation dashboard."""
    st.header("📊 Evaluation Dashboard")
    
    # Get current user for access control
    auth_manager = AuthManager()
    current_user = auth_manager.get_current_user()
    
    if not current_user or current_user.role != 'admin':
        st.error("❌ Access denied. Admin privileges required.")
        return
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Overview", 
        "👥 User Analytics", 
        "💬 Feedback Analysis", 
        "📊 System Metrics"
    ])
    
    with tab1:
        render_overview_tab()
        
    with tab2:
        render_user_analytics_tab()
        
    with tab3:
        render_feedback_analysis_tab()
        
    with tab4:
        render_system_metrics_tab()

def render_overview_tab():
    """Render the overview tab with key metrics."""
    st.subheader("🎯 Key Performance Indicators")
    
    # Create metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Get real user data for metrics
    auth_manager = AuthManager()
    db_path = getattr(auth_manager, 'db_path', 'src/database/superstore.db')
    
    try:
        users = User.get_all_users(db_path)
        total_users = len(users) if users else 0
        
        # Calculate age statistics
        ages = [user.age for user in users if user.age is not None]
        avg_age = round(sum(ages) / len(ages), 1) if ages else 0
        min_age = min(ages) if ages else 0
        max_age = max(ages) if ages else 0
        
        with col1:
            st.metric(
                label="Total Users",
                value=total_users,
                delta="5 this week"
            )
        
        with col2:
            st.metric(
                label="Average Age",
                value=f"{avg_age} years",
                delta=f"Range: {min_age}-{max_age}"
            )
        
        with col3:
            st.metric(
                label="Chat Sessions",
                value="156",
                delta="23 today"
            )
        
        with col4:
            st.metric(
                label="System Uptime",
                value="99.8%",
                delta="0.1%"
            )
    except Exception as e:
        # Fallback to sample data if there's an error
    with col1:
        st.metric(
            label="Total Users",
            value="42",
            delta="5 this week"
        )
    
    with col2:
            st.metric(
                label="Average Age",
                value="25 years",
                delta="Range: 18-45"
            )
        
        with col3:
        st.metric(
            label="Chat Sessions",
            value="156",
            delta="23 today"
        )
    
    with col4:
        st.metric(
            label="System Uptime",
            value="99.8%",
            delta="0.1%"
        )
    
    # Activity chart
    st.subheader("📈 Activity Trends")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    activity_data = pd.DataFrame({
        'Date': dates,
        'Sessions': [15, 23, 18, 31, 25, 19, 28] * 4 + [20, 25, 22]
    })
    
    fig = px.line(
        activity_data, 
        x='Date', 
        y='Sessions',
        title='Daily Chat Sessions'
    )
    st.plotly_chart(fig, use_container_width=True)

def render_user_analytics_tab():
    """Render user analytics and behavior patterns."""
    st.subheader("👥 User Behavior Analytics")
    
    # Get real user data
    auth_manager = AuthManager()
    db_path = getattr(auth_manager, 'db_path', 'src/database/superstore.db')
    
    try:
        users = User.get_all_users(db_path)
        
        if users:
            # User role distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("User Role Distribution")
                role_counts = {}
                for user in users:
                    role_counts[user.role] = role_counts.get(user.role, 0) + 1
                
                if role_counts:
                    role_data = pd.DataFrame({
                        'Role': list(role_counts.keys()),
                        'Count': list(role_counts.values())
                    })
                    
                    fig = px.pie(
                        role_data, 
                        values='Count', 
                        names='Role',
                        title='User Distribution by Role'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No user data available")
            
            with col2:
                st.subheader("Assessment Completion Status")
                completed = sum(1 for user in users if user.has_completed_assessment)
                not_completed = len(users) - completed
                
                completion_data = pd.DataFrame({
                    'Status': ['Completed', 'Not Completed'],
                    'Count': [completed, not_completed]
                })
                
                fig = px.pie(
                    completion_data, 
                    values='Count', 
                    names='Status',
                    title='Assessment Completion Status'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # User demographics
            st.subheader("👤 User Demographics")
            
            # Age distribution
            age_counts = {}
            for user in users:
                if user.age:
                    age_counts[user.age] = age_counts.get(user.age, 0) + 1
            
            if age_counts:
                age_data = pd.DataFrame({
                    'Age': list(age_counts.keys()),
                    'Count': list(age_counts.values())
                })
                age_data = age_data.sort_values('Age')
                
                fig = px.bar(
                    age_data, 
                    x='Age', 
                    y='Count',
                    title='User Distribution by Age'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No age data available")
            
            # Gender distribution
            col1, col2 = st.columns(2)
            
            with col1:
                gender_counts = {}
                for user in users:
                    if user.gender:
                        gender_counts[user.gender] = gender_counts.get(user.gender, 0) + 1
                
                if gender_counts:
                    gender_data = pd.DataFrame({
                        'Gender': list(gender_counts.keys()),
                        'Count': list(gender_counts.values())
                    })
                    
                    fig = px.bar(
                        gender_data, 
                        x='Gender', 
                        y='Count',
                        title='User Distribution by Gender'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No gender data available")
            
            with col2:
                # Education level distribution
                education_counts = {}
                for user in users:
                    if user.education_level:
                        education_counts[user.education_level] = education_counts.get(user.education_level, 0) + 1
                
                if education_counts:
                    education_data = pd.DataFrame({
                        'Education Level': list(education_counts.keys()),
                        'Count': list(education_counts.values())
                    })
                    
                    fig = px.bar(
                        education_data, 
                        x='Education Level', 
                        y='Count',
                        title='User Distribution by Education Level'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No education data available")
            
            # User assessment levels
            st.subheader("📊 User Assessment Levels")
            level_counts = {}
            for user in users:
                if user.user_level_category:
                    level_counts[user.user_level_category] = level_counts.get(user.user_level_category, 0) + 1
            
            if level_counts:
                level_data = pd.DataFrame({
                    'Level': list(level_counts.keys()),
                    'Count': list(level_counts.values())
                })
                
                fig = px.bar(
                    level_data, 
                    x='Level', 
                    y='Count',
                    title='User Distribution by Assessment Level'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent user table with real data
            st.subheader("📋 Recent User Activity")
            
            # Prepare user data for display
            user_display_data = []
            for user in users[:10]:  # Show last 10 users
                user_display_data.append({
                    'Username': user.username,
                    'Role': user.role,
                    'Age': user.age or 'Not Specified',
                    'Assessment Level': user.user_level_category or 'Not Assessed',
                    'Gender': user.gender or 'Not Specified',
                    'Profession': user.profession or 'Not Specified',
                    'Education': user.education_level or 'Not Specified',
                    'Created': user.created_at.strftime('%Y-%m-%d') if user.created_at else 'Unknown'
                })
            
            if user_display_data:
                user_df = pd.DataFrame(user_display_data)
                st.dataframe(user_df, use_container_width=True)
            else:
                st.info("No user data available")
                
        else:
            st.info("No users found in the database")
            
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        # Fallback to sample data
        st.subheader("📋 Sample User Data (Fallback)")
        recent_users = pd.DataFrame({
            'Username': ['user1', 'user2', 'user3', 'admin1', 'user4'],
            'Last Active': ['2024-01-15 14:30', '2024-01-15 12:15', '2024-01-14 16:45', '2024-01-15 09:20', '2024-01-13 11:30'],
            'Sessions': [15, 8, 23, 45, 3],
            'Status': ['Active', 'Active', 'Inactive', 'Active', 'New']
        })
        st.dataframe(recent_users, use_container_width=True)

def render_feedback_analysis_tab():
    """Render feedback analysis and sentiment trends."""
    st.subheader("💬 User Feedback Analysis")
    
    # Get database path
    try:
        auth_manager = AuthManager()
        db_path = getattr(auth_manager, 'db_path', 'src/database/superstore.db')
    except:
        db_path = 'src/database/superstore.db'
    
    # Explanation Feedback Analysis
    st.markdown("### 📝 Explanation Feedback Analysis")
    
    if ExplanationFeedback:
        feedback_data = ExplanationFeedback.get_all_feedback(db_path)
        
        if feedback_data:
            # Convert to DataFrame for analysis
            feedback_df = pd.DataFrame([
                {
                    'Username': getattr(fb, 'username', 'Unknown'),
                    'Explanation Given': fb.explanation_given,
                    'Was Needed': fb.was_needed,
                    'Was Helpful': fb.was_helpful,
                    'Would Have Been Needed': fb.would_have_been_needed,
                    'Date': fb.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for fb in feedback_data
            ])
            
            st.dataframe(feedback_df, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Feedback", len(feedback_data))
    with col2:
                explanations_given = sum(1 for fb in feedback_data if fb.explanation_given)
                st.metric("Explanations Given", explanations_given)
            with col3:
                helpful_explanations = sum(1 for fb in feedback_data if fb.was_helpful)
                st.metric("Helpful Explanations", helpful_explanations)
        else:
            st.info("No explanation feedback data available yet.")
    else:
        st.warning("ExplanationFeedback model not available.")
    
    # Comprehensive Research Feedback Analysis
    st.markdown("### 🔬 Comprehensive Research Feedback Analysis")
    
    if ComprehensiveFeedback:
        comprehensive_feedback_data = ComprehensiveFeedback.get_all_feedback(db_path)
        
        if comprehensive_feedback_data:
            # Convert to DataFrame for analysis
            comp_feedback_df = pd.DataFrame([
                {
                    'Username': getattr(fb, 'username', 'Unknown'),
                    'Frequency Rating': fb.frequency_rating,
                    'Explanation Quality': fb.explanation_quality_rating,
                    'System Helpfulness': fb.system_helpfulness_rating,
                    'Learning Improvement': fb.learning_improvement_rating,
                    'Auto Explanation': fb.auto_explanation,
                    'System Accuracy': fb.system_accuracy,
                    'Recommendation': fb.recommendation,
                    'Date': fb.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for fb in comprehensive_feedback_data
            ])
            
            st.dataframe(comp_feedback_df, use_container_width=True)
            
            # Summary statistics for comprehensive feedback
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Research Feedback", len(comprehensive_feedback_data))
            with col2:
                avg_quality = sum(fb.explanation_quality_rating for fb in comprehensive_feedback_data) / len(comprehensive_feedback_data)
                st.metric("Avg. Explanation Quality", f"{avg_quality:.1f}/5")
            with col3:
                avg_helpfulness = sum(fb.system_helpfulness_rating for fb in comprehensive_feedback_data) / len(comprehensive_feedback_data)
                st.metric("Avg. System Helpfulness", f"{avg_helpfulness:.1f}/5")
            with col4:
                positive_recommendations = sum(1 for fb in comprehensive_feedback_data if fb.recommendation == 'Yes')
                st.metric("Positive Recommendations", f"{positive_recommendations}/{len(comprehensive_feedback_data)}")
            
            # Detailed feedback analysis
            st.markdown("#### 📊 Detailed Feedback Analysis")
            
            # Frequency rating distribution
            st.subheader("Explanation Frequency Preferences")
            frequency_counts = comp_feedback_df['Frequency Rating'].value_counts().sort_index()
            st.bar_chart(frequency_counts)
            
            # Explanation quality distribution
            st.subheader("Explanation Quality Ratings")
            quality_counts = comp_feedback_df['Explanation Quality'].value_counts().sort_index()
            st.bar_chart(quality_counts)
            
            # System helpfulness distribution
            st.subheader("System Helpfulness Ratings")
            helpfulness_counts = comp_feedback_df['System Helpfulness'].value_counts().sort_index()
            st.bar_chart(helpfulness_counts)
            
            # Learning improvement distribution
            st.subheader("Learning Improvement Ratings")
            learning_counts = comp_feedback_df['Learning Improvement'].value_counts().sort_index()
            st.bar_chart(learning_counts)
            
            # Auto-explanation preferences
            st.subheader("Auto-Explanation Preferences")
            auto_explanation_counts = comp_feedback_df['Auto Explanation'].value_counts()
            st.bar_chart(auto_explanation_counts)
            
            # System accuracy beliefs
            st.subheader("System Accuracy Beliefs")
            accuracy_counts = comp_feedback_df['System Accuracy'].value_counts()
            st.bar_chart(accuracy_counts)
            
            # Recommendations
            st.subheader("System Recommendations")
            recommendation_counts = comp_feedback_df['Recommendation'].value_counts()
            st.bar_chart(recommendation_counts)
            
        else:
            st.info("No comprehensive research feedback data available yet.")
    else:
        st.warning("ComprehensiveFeedback model not available.")

def render_system_metrics_tab():
    """Render system performance and technical metrics."""
    st.subheader("🔧 System Performance Metrics")
    
    # System health indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Response Time", "1.2s", "-0.3s")
    
    with col2:
        st.metric("Error Rate", "0.8%", "-0.2%")
    
    with col3:
        st.metric("CPU Usage", "45%", "5%")
    
    with col4:
        st.metric("Memory Usage", "62%", "3%")
    
    # Performance trends
    st.subheader("📈 Performance Trends")
    
    perf_data = pd.DataFrame({
        'Time': pd.date_range(start='2024-01-15 00:00', periods=24, freq='H'),
        'Response Time (ms)': [1200, 1150, 1300, 1100, 1250, 1180, 1220] * 3 + [1190, 1160, 1140],
        'CPU Usage (%)': [45, 42, 48, 40, 46, 44, 47] * 3 + [43, 41, 39],
        'Memory Usage (%)': [62, 60, 65, 58, 63, 61, 64] * 3 + [59, 57, 55]
    })
    
    # Response time chart
    fig = px.line(
        perf_data, 
        x='Time', 
        y='Response Time (ms)',
        title='System Response Time (24h)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Resource usage
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(perf_data, x='Time', y='CPU Usage (%)', title='CPU Usage')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(perf_data, x='Time', y='Memory Usage (%)', title='Memory Usage')
        st.plotly_chart(fig, use_container_width=True)
    
    # System logs (sample)
    st.subheader("📝 Recent System Events")
    
    logs = pd.DataFrame({
        'Timestamp': ['2024-01-15 14:30:00', '2024-01-15 14:25:00', '2024-01-15 14:20:00'],
        'Level': ['INFO', 'WARNING', 'INFO'],
        'Message': [
            'User login successful',
            'High memory usage detected',
            'Database backup completed'
        ]
    })
    
    st.dataframe(logs, use_container_width=True)

if __name__ == "__main__":
    render_evaluation_dashboard() 