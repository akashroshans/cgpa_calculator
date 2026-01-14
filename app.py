import streamlit as st

def calculate_gpa(subjects):
    """Calculate GPA from list of subjects with grades and credits"""
    if not subjects:
        return 0.0
    
    total_grade_points = sum(subject['grade'] * subject['credit'] for subject in subjects)
    total_credits = sum(subject['credit'] for subject in subjects)
    
    if total_credits == 0:
        return 0.0
    
    return total_grade_points / total_credits

def calculate_cgpa(previous_cgpa, current_gpa, previous_credits, current_credits):
    """Calculate CGPA using previous CGPA and current semester GPA"""
    if previous_credits == 0:
        return current_gpa
    
    total_grade_points = (previous_cgpa * previous_credits) + (current_gpa * current_credits)
    total_credits = previous_credits + current_credits
    
    return total_grade_points / total_credits

def get_grade_classification(gpa):
    """Get grade classification based on GPA"""
    if gpa >= 10.0:
        return "O", "green"
    elif gpa >= 9.0:
        return "A+", "green"
    elif gpa >= 8.0:
        return "A", "blue"
    elif gpa >= 7.0:
        return "B+", "blue"
    elif gpa >= 6.0:
        return "B", "orange"
    elif gpa >= 5.0:
        return "C", "orange"
    elif gpa >= 4.0:
        return "D", "red"
    else:
        return "F", "red"

def main():
    st.set_page_config(
        page_title="CGPA Calculator",
        page_icon="🎓",
        layout="wide"
    )
    
    # Basic CSS for mobile responsiveness
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column;
        }
        .main .block-container {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎓 CGPA Calculator")
    st.markdown("---")
    
    # Initialize session state for subjects
    if 'subjects' not in st.session_state:
        st.session_state.subjects = []
    
    # Initialize counter for clearing subject name only
    if 'subject_name_counter' not in st.session_state:
        st.session_state.subject_name_counter = 0
    
    # Initialize persistent values for grade and credit
    if 'last_grade' not in st.session_state:
        st.session_state.last_grade = 0
    
    if 'last_credit' not in st.session_state:
        st.session_state.last_credit = 1
    
    # Sidebar for previous CGPA input
    st.sidebar.header("Previous Academic Record")
    previous_cgpa = st.sidebar.number_input(
        "Previous CGPA", 
        min_value=0.0, 
        max_value=10.0, 
        value=0.0, 
        step=0.01,
        help="Enter your previous CGPA (0.0 if first semester)"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Grade Scale")
    st.sidebar.markdown("""
    - **O** = 10 points
    - **A+** = 9 points  
    - **A** = 8 points
    - **B+** = 7 points
    - **B** = 6 points
    - **C** = 5 points
    - **RA** = Below 5
    """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Current Semester Subjects")
        
        # Add new subject section - only subject name gets cleared
        with st.expander("➕ Add New Subject", expanded=True):
            # Only subject name uses counter for clearing
            new_subject_name = st.text_input("Subject Name", key=f"subject_name_{st.session_state.subject_name_counter}")
            
            col_grade, col_credit = st.columns(2)
            
            with col_grade:
                new_grade = st.number_input(
                    "Grade Point",
                    min_value=0,
                    max_value=10,
                    value=st.session_state.last_grade,
                    step=1,
                    help="Grade point (0-10 scale)"
                )
                # Update session state when value changes
                st.session_state.last_grade = new_grade
            
            with col_credit:
                new_credit = st.number_input(
                    "Credits",
                    min_value=1,
                    value=st.session_state.last_credit,
                    step=1,
                    help="Credits for this subject"
                )
                # Update session state when value changes
                st.session_state.last_credit = new_credit
            
            if st.button("Add Subject", type="primary"):
                if new_subject_name.strip():
                    st.session_state.subjects.append({
                        'name': new_subject_name.strip(),
                        'grade': new_grade,
                        'credit': new_credit
                    })
                    st.success(f"Added {new_subject_name}")
                    # Only increment subject name counter to clear subject name field
                    st.session_state.subject_name_counter += 1
                    st.rerun()
                else:
                    st.error("Please enter a subject name")
        
        # Display current subjects
        if st.session_state.subjects:
            st.subheader("Current Subjects")
            
            for i, subject in enumerate(st.session_state.subjects):
                with st.container():
                    col_name, col_grade, col_credit, col_action = st.columns([3, 1, 1, 1])
                    
                    with col_name:
                        st.write(f"**{subject['name']}**")
                    
                    with col_grade:
                        st.write(f"Grade: {subject['grade']}")
                    
                    with col_credit:
                        st.write(f"Credits: {subject['credit']}")
                    
                    with col_action:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete subject"):
                            st.session_state.subjects.pop(i)
                            st.rerun()
                
                st.markdown("---")
        
        # Clear all subjects button
        if st.session_state.subjects:
            if st.button("Clear All Subjects", type="secondary"):
                st.session_state.subjects = []
                st.rerun()
    
    with col2:
        st.header("Results")
        
        if st.session_state.subjects:
            # Calculate current semester GPA
            current_gpa = calculate_gpa(st.session_state.subjects)
            current_credits = sum(subject['credit'] for subject in st.session_state.subjects)
            
            # Display current semester results
            st.metric("Current Semester GPA", f"{current_gpa:.3f}")
            st.metric("Current Semester Credits", current_credits)
            
            # Calculate and display CGPA
            if previous_cgpa > 0:
                # Assume equal weight for previous and current if no previous credits specified
                # This is a simplified approach - you can adjust the weighting as needed
                total_previous_credits = current_credits  # Assuming equal weighting
                cgpa = calculate_cgpa(previous_cgpa, current_gpa, total_previous_credits, current_credits)
                
                st.markdown("---")
                st.metric("Overall CGPA", f"{cgpa:.3f}")
                
                # Grade classification for CGPA
                cgpa_grade, cgpa_color = get_grade_classification(cgpa)
                st.markdown(f"**CGPA Grade:** :{cgpa_color}[{cgpa_grade}]")
                
            else:
                st.markdown("---")
                st.metric("Overall CGPA", f"{current_gpa:.3f}")
                st.info("This appears to be your first semester")
            
            # Grade classification for current semester
            current_grade, current_color = get_grade_classification(current_gpa)
            st.markdown(f"**Current Semester Grade:** :{current_color}[{current_grade}]")
            
        else:
            st.info("Add subjects to calculate GPA")
    
    # Help section
    with st.expander("ℹ️ How to use this calculator"):
        st.markdown("""
        **Steps to calculate your CGPA:**
        1. Enter your previous CGPA in the sidebar (0.0 if first semester)
        2. Add your current semester subjects with their grade points and credits
        3. The calculator will automatically compute your current semester GPA and overall CGPA
        
        **Grade Point Scale:**
        - O = 10, A+ = 9, A = 8, B+ = 7, B = 6, C = 5, RA if below 5
        
        **Note:** If this is your first semester, leave previous CGPA as 0.
        """)

if __name__ == "__main__":
    main()
