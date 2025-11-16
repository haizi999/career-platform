import streamlit as st
import pandas as pd
from data_manager import CareerDataManager
from visualizer import CareerVisualizer

# 페이지 설정
st.set_page_config(
    page_title="진로 탐색",
    page_icon="🎯",
    layout="wide"
)

# 간단한 CSS
st.markdown("""
    <style>
    .big-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 관리자 초기화
@st.cache_resource
def get_managers():
    return CareerDataManager(), CareerVisualizer()

data_manager, visualizer = get_managers()

# 세션 상태 초기화
if 'selected_job_code' not in st.session_state:
    st.session_state.selected_job_code = None
if 'selected_jobs_for_comparison' not in st.session_state:
    st.session_state.selected_jobs_for_comparison = []

# 메인 타이틀
st.markdown('<p class="big-title">🎯 진로 탐색 플랫폼</p>', unsafe_allow_html=True)
st.markdown("### 미래 직업을 쉽고 빠르게 찾아보세요")
st.divider()

# 탭 메뉴
tab1, tab2, tab3, tab4 = st.tabs(["🔍 직업 찾기", "📊 비교하기", "🎓 진학 정보", "🗺️ 진로 경로"])

# 탭 1: 직업 찾기
with tab1:
    st.markdown("## 어떤 직업을 찾고 계신가요?")
    
    # 검색창
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "직업 검색",
            placeholder="예: AI 엔지니어, 경영 컨설턴트",
            label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("🔍 검색", use_container_width=True)
    
    # 인기 직업 버튼
    st.markdown("#### 또는 인기 직업 바로 보기")
    cols = st.columns(5)
    popular_jobs = [
        ("🤖 AI 엔지니어", "AI001"),
        ("💼 경영 컨설턴트", "BIZ001"),
        ("🧠 임상심리사", "PSY001"),
        ("🎨 UX/UI 디자이너", "ART001"),
        ("🎬 크리에이터", "MDA001")
    ]
    
    for idx, (job_name, job_code) in enumerate(popular_jobs):
        with cols[idx]:
            if st.button(job_name, key=f"pop_{job_code}"):
                st.session_state.selected_job_code = job_code
                st.rerun()
    
    # 검색 결과
    if search_query or search_button:
        results = data_manager.search_jobs_by_keyword(search_query)
        
        if results:
            st.success(f"✅ {len(results)}개의 직업을 찾았습니다!")
            
            for job in results[:10]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"### {job['name']}")
                    st.caption(f"분야: {job.get('field', '일반')} | 전망: {job.get('growth', '보통')}")
                with col2:
                    if st.button("📖 상세", key=f"detail_{job['code']}"):
                        st.session_state.selected_job_code = job['code']
                        st.rerun()
                with col3:
                    if st.button("➕ 비교", key=f"add_{job['code']}"):
                        if job['code'] not in st.session_state.selected_jobs_for_comparison:
                            st.session_state.selected_jobs_for_comparison.append(job['code'])
                            st.success("추가됨!")
                st.divider()
        else:
            st.warning("검색 결과가 없습니다")
    
    # 선택된 직업 상세
    if st.session_state.selected_job_code:
        job_data = data_manager.get_job_details(st.session_state.selected_job_code)
        
        if job_data:
            st.markdown("---")
            st.markdown(f"# {job_data['job_name']}")
            
            # 핵심 정보
            cols = st.columns(4)
            with cols[0]:
                st.metric("💰 연봉", job_data.get('salary_range', 'N/A'))
            with cols[1]:
                st.metric("📈 전망", job_data.get('outlook', 'N/A'))
            with cols[2]:
                st.metric("📊 성장률", job_data.get('growth_rate', 'N/A'))
            with cols[3]:
                st.metric("🎓 취업률", job_data.get('employment_rate', 'N/A'))
            
            st.markdown("---")
            
            # 상세 정보
            st.markdown("### 📝 직업 설명")
            st.info(job_data.get('description', ''))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔧 주요 업무")
                for task in job_data.get('main_tasks', []):
                    st.markdown(f"• {task}")
            
            with col2:
                st.markdown("### 💪 필요한 능력")
                for skill in job_data.get('required_skills', [])[:5]:
                    st.markdown(f"• {skill}")
            
            if st.button("← 검색으로 돌아가기"):
                st.session_state.selected_job_code = None
                st.rerun()

# 탭 2: 비교하기
with tab2:
    st.markdown("## 직업 비교하기")
    
    if st.session_state.selected_jobs_for_comparison:
        st.success(f"📋 {len(st.session_state.selected_jobs_for_comparison)}개 직업 선택됨")
        
        # 선택된 직업 표시
        cols = st.columns(len(st.session_state.selected_jobs_for_comparison))
        for idx, job_code in enumerate(st.session_state.selected_jobs_for_comparison):
            job = data_manager.get_job_details(job_code)
            with cols[idx]:
                st.markdown(f"**{job.get('job_name', '')}**")
                if st.button("❌", key=f"remove_{job_code}"):
                    st.session_state.selected_jobs_for_comparison.remove(job_code)
                    st.rerun()
        
        if len(st.session_state.selected_jobs_for_comparison) >= 2:
            st.markdown("---")
            
            # 비교 테이블
            comparison_df = data_manager.compare_jobs(st.session_state.selected_jobs_for_comparison)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            # 연봉 비교 차트
            job_details = [data_manager.get_job_details(code) for code in st.session_state.selected_jobs_for_comparison]
            st.plotly_chart(
                visualizer.create_salary_distribution(job_details),
                use_container_width=True
            )
            
            if st.button("🔄 초기화"):
                st.session_state.selected_jobs_for_comparison = []
                st.rerun()
        else:
            st.info("💡 최소 2개 이상의 직업을 선택하세요")
    else:
        st.info("💡 '직업 찾기' 탭에서 비교할 직업을 추가하세요")

# 탭 3: 진학 정보
with tab3:
    st.markdown("## 진학 정보")
    
    job_search = st.text_input("직업 검색", placeholder="예: AI 엔지니어", key="major_search")
    
    if job_search:
        jobs = data_manager.search_jobs_by_keyword(job_search)
        if jobs:
            job_options = {job['name']: job['code'] for job in jobs[:5]}
            selected_job = st.selectbox("직업 선택", list(job_options.keys()))
            
            if selected_job:
                mapping = data_manager.get_job_to_major_mapping(job_options[selected_job])
                
                st.markdown(f"### {selected_job} 진학 정보")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 🏫 고등학교")
                    st.markdown("**권장 선택과목**")
                    for subject in mapping.get('high_school_subjects', []):
                        st.success(subject)
                
                with col2:
                    st.markdown("#### 🎓 대학 전공")
                    for major in mapping.get('related_majors', [])[:5]:
                        st.info(major)
                
                with col3:
                    st.markdown("#### 📜 학력 요구")
                    st.warning(mapping.get('required_education', ''))

# 탭 4: 진로 경로
with tab4:
    st.markdown("## 진로 경로")
    
    job_search_path = st.text_input("직업 검색", placeholder="진로 경로를 볼 직업", key="path_search")
    
    if job_search_path:
        jobs = data_manager.search_jobs_by_keyword(job_search_path)
        if jobs:
            job_options = {job['name']: job['code'] for job in jobs[:5]}
            selected_job_name = st.selectbox("직업 선택", list(job_options.keys()), key="path_select")
            
            if selected_job_name:
                path_data = data_manager.get_career_path_data(job_options[selected_job_name])
                
                st.markdown(f"### {selected_job_name} 되는 법")
                
                # 경로 시각화
                st.plotly_chart(
                    visualizer.create_career_path_network(path_data),
                    use_container_width=True
                )
                
                # 단계별 설명
                st.markdown("### 📋 단계별 준비")
                for idx, step in enumerate(path_data.get('steps', []), 1):
                    with st.expander(f"**{idx}단계: {step}**"):
                        st.markdown("준비사항을 차근차근 진행하세요")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>💡 경기도 진로전담교사 지원 시스템</p>
</div>
""", unsafe_allow_html=True)
