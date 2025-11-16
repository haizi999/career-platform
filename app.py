import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import sys
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from data_manager import CareerDataManager
from visualizer import CareerVisualizer

# 페이지 설정
st.set_page_config(
    page_title="진로 탐색",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 심플한 CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 10px 0;
    }
    .main-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 관리자 및 시각화 객체 초기화
@st.cache_resource
def get_managers():
    return CareerDataManager(), CareerVisualizer()

data_manager, visualizer = get_managers()

# 세션 상태 초기화
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None
if 'selected_jobs_for_comparison' not in st.session_state:
    st.session_state.selected_jobs_for_comparison = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# 메인 타이틀
st.markdown('<p class="big-font">🎯 진로 탐색</p>', unsafe_allow_html=True)
st.markdown("### 미래 직업을 쉽고 빠르게 찾아보세요")

# 간단한 탭 메뉴
tab1, tab2, tab3, tab4 = st.tabs(["🔍 직업 찾기", "📊 비교하기", "🎓 진학 정보", "🗺️ 진로 경로"])

with tab1:
with tab1:
    st.markdown("## 어떤 직업을 찾고 계신가요?")
    
    # 큰 검색창
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "직업 이름을 입력하세요",
            placeholder="예: AI 엔지니어, 데이터 사이언티스트",
            label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("🔍 검색", use_container_width=True)
    
    # 인기 직업 빠른 버튼
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
            if st.button(job_name, key=f"pop_{job_code}", use_container_width=True):
                st.session_state.selected_job_code = job_code
    
    # 검색 결과 표시
    if search_query or search_button:
        results = data_manager.search_jobs_by_keyword(search_query)
        
        if results:
            st.success(f"✅ {len(results)}개의 직업을 찾았습니다!")
            
            for job in results[:6]:  # 상위 6개만
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"### {job['name']}")
                        st.caption(f"분야: {job.get('field', '신산업')} | 전망: {job.get('growth', '높음')}")
                    with col2:
                        if st.button("📖 자세히", key=f"detail_{job['code']}", use_container_width=True):
                            st.session_state.selected_job_code = job['code']
                    with col3:
                        if st.button("➕ 비교", key=f"add_{job['code']}", use_container_width=True):
                            if job['code'] not in st.session_state.selected_jobs_for_comparison:
                                st.session_state.selected_jobs_for_comparison.append(job['code'])
                                st.success("비교 목록에 추가!")
                    st.divider()
        else:
            st.warning("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")
    
    # 선택된 직업 상세 정보
    if 'selected_job_code' in st.session_state and st.session_state.selected_job_code:
        job_data = data_manager.get_job_details(st.session_state.selected_job_code)
        
        if job_data:
            st.markdown("---")
            st.markdown(f"# {job_data['job_name']}")
            
            # 핵심 정보를 카드로
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
            
            # 심플한 정보 표시
            st.markdown("### 📝 이 직업은요")
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

with tab2:
    
    # 주요 기능 소개
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("신산업 분야", "8개 분야")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("등록 직업", "500+ 개")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("연계 학과", "300+ 개")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("데이터 갱신", "실시간")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 시작하기 가이드
    st.markdown('<div class="sub-header">🎯 어떻게 시작할까요?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**🔍 신산업 분야별 탐색**")
        st.markdown("""
        - AI, 바이오, 친환경 등 8대 신산업 분야별 직업 탐색
        - 각 분야의 트렌드와 전망 확인
        - 분야별 대표 직업 및 신생 직업 소개
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**💼 직업 검색**")
        st.markdown("""
        - 관심 있는 직업 직접 검색
        - 직업별 상세 정보 (하는 일, 되는 법, 전망)
        - 필요한 역량과 자격증 확인
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**🎓 학과 연결**")
        st.markdown("""
        - 직업별 필요한 대학 전공 확인
        - 고등학교 선택과목 추천
        - 진학 경로 시각화
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**📊 직업 비교**")
        st.markdown("""
        - 관심 직업 2-3개 선택하여 비교
        - 연봉, 전망, 필요 역량 등 다각도 비교
        - 나에게 맞는 직업 찾기
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 최근 업데이트
    st.markdown("---")
    st.markdown('<div class="sub-header">📢 최근 업데이트</div>', unsafe_allow_html=True)
    
    updates = [
        {"date": "2025-11-15", "content": "메타버스 XR 디자이너 직업 정보 추가"},
        {"date": "2025-11-10", "content": "AI 윤리 전문가 신규 등록"},
        {"date": "2025-11-05", "content": "친환경 에너지 분야 20개 직업 정보 갱신"}
    ]
    
    for update in updates:
        st.markdown(f"**{update['date']}** - {update['content']}")

elif menu == "🔍 신산업 분야별 탐색":
    st.markdown('<div class="main-header">🔍 신산업 분야별 직업 탐색</div>', unsafe_allow_html=True)
    
    # 신산업 분야 선택
    st.markdown('<div class="sub-header">신산업 분야를 선택하세요</div>', unsafe_allow_html=True)
    
    # 신산업 8대 분야
    industries = {
        "AI/빅데이터": {
            "icon": "🤖",
            "description": "인공지능, 머신러닝, 데이터 분석",
            "growth": "매우 높음",
            "jobs_count": 85
        },
        "바이오헬스": {
            "icon": "🧬",
            "description": "생명공학, 의료기술, 헬스케어",
            "growth": "높음",
            "jobs_count": 72
        },
        "친환경에너지": {
            "icon": "🌱",
            "description": "재생에너지, 탄소중립, 그린테크",
            "growth": "매우 높음",
            "jobs_count": 64
        },
        "메타버스/XR": {
            "icon": "🥽",
            "description": "가상현실, 증강현실, 메타버스",
            "growth": "높음",
            "jobs_count": 58
        },
        "자율주행/모빌리티": {
            "icon": "🚗",
            "description": "자율주행차, 미래 모빌리티",
            "growth": "높음",
            "jobs_count": 55
        },
        "로봇공학": {
            "icon": "🦾",
            "description": "산업용 로봇, 서비스 로봇",
            "growth": "중상",
            "jobs_count": 48
        },
        "우주항공": {
            "icon": "🚀",
            "description": "우주탐사, 위성, 항공기술",
            "growth": "중상",
            "jobs_count": 42
        },
        "스마트시티": {
            "icon": "🏙️",
            "description": "스마트빌딩, IoT, 도시계획",
            "growth": "중",
            "jobs_count": 51
        }
    }
    
    # 산업 개요 차트
    st.plotly_chart(
        visualizer.create_industry_overview(industries),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # 분야별 카드 표시
    cols = st.columns(4)
    for idx, (industry, info) in enumerate(industries.items()):
        with cols[idx % 4]:
            with st.container():
                st.markdown(f"""
                <div class="career-card">
                    <h3>{info['icon']} {industry}</h3>
                    <p>{info['description']}</p>
                    <p><strong>성장성:</strong> {info['growth']}</p>
                    <p><strong>관련 직업:</strong> {info['jobs_count']}개</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"자세히 보기", key=f"btn_{industry}"):
                    st.session_state.selected_industry = industry
    
    # 선택된 분야 상세 정보
    if st.session_state.selected_industry:
        st.markdown("---")
        selected = st.session_state.selected_industry
        st.markdown(f'<div class="sub-header">{industries[selected]["icon"]} {selected} 분야 상세</div>', unsafe_allow_html=True)
        
        # 해당 분야의 직업 데이터 가져오기
        jobs_in_industry = data_manager.get_industry_jobs(selected)
        
        # 탭으로 정보 구성
        tab1, tab2, tab3 = st.tabs(["📋 개요", "💼 주요 직업", "📈 전망 및 트렌드"])
        
        with tab1:
            st.markdown(f"**{industries[selected]['description']}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("관련 직업 수", f"{len(jobs_in_industry)}개")
            with col2:
                st.metric("분야 성장성", industries[selected]['growth'])
            with col3:
                avg_growth = "20%"  # 계산 가능
                st.metric("평균 성장률", avg_growth)
            
            st.markdown("#### 이 분야의 특징")
            industry_descriptions = {
                "AI/빅데이터": """
                - 4차 산업혁명의 핵심 기술 분야
                - 모든 산업에서 AI 도입이 가속화되고 있어 수요 급증
                - 데이터 기반 의사결정이 표준화되면서 관련 직업 다양화
                - 지속적인 기술 발전으로 새로운 직종 생성 중
                """,
                "바이오헬스": """
                - 고령화 사회와 맞춤형 의료 수요 증가
                - 유전자 분석, 바이오 신약 개발 등 첨단 기술 융합
                - COVID-19 이후 바이오 산업의 중요성 부각
                - 생명공학과 IT 기술의 융합으로 새로운 기회 창출
                """,
                "친환경에너지": """
                - 탄소중립 목표 달성을 위한 핵심 분야
                - 재생에너지 비중 확대 정책으로 시장 성장
                - ESG 경영 확산으로 기업 투자 증가
                - 수소경제, 전기차 배터리 등 신산업 창출
                """
            }
            st.markdown(industry_descriptions.get(selected, "신산업 분야로 빠르게 성장하고 있습니다."))
        
        with tab2:
            st.markdown("#### 이 분야의 대표 직업")
            
            # 직업 목록 표시
            for job in jobs_in_industry[:10]:  # 상위 10개만 표시
                with st.expander(f"**{job['name']}** ({job['growth']})"):
                    job_detail = data_manager.get_job_details(job['code'])
                    if job_detail:
                        st.markdown(f"**📝 설명:** {job_detail.get('description', '')}")
                        st.markdown(f"**🎓 학력:** {job_detail.get('required_education', '')}")
                        st.markdown(f"**💰 연봉:** {job_detail.get('salary_range', '')}")
                        
                        if st.button(f"상세 정보 보기", key=f"detail_{job['code']}"):
                            st.session_state.selected_job_code = job['code']
                            st.rerun()
            
            # 성장 전망 차트
            st.plotly_chart(
                visualizer.create_growth_comparison(jobs_in_industry[:8]),
                use_container_width=True
            )
        
        with tab3:
            st.markdown("#### 시장 전망 및 최신 트렌드")
            
            trend_info = {
                "AI/빅데이터": {
                    "market_size": "2025년 약 50조원 규모 (국내)",
                    "growth_forecast": "연평균 25% 성장 전망",
                    "trends": [
                        "생성형 AI의 급격한 발전 (ChatGPT, DALL-E 등)",
                        "AI 윤리 및 규제 강화",
                        "엣지 AI와 경량화 모델 개발",
                        "AutoML과 Low-code AI 플랫폼 확산"
                    ],
                    "opportunities": [
                        "AI 전문 인력 수요 지속 증가",
                        "산업별 AI 전문가 필요성 대두",
                        "AI 윤리 전문가 등 새로운 직종 출현"
                    ]
                },
                "바이오헬스": {
                    "market_size": "2025년 약 30조원 규모 (국내)",
                    "growth_forecast": "연평균 18% 성장 전망",
                    "trends": [
                        "정밀의료와 맞춤형 치료제 개발",
                        "디지털 헬스케어 급성장",
                        "바이오 빅데이터 활용 증가",
                        "mRNA 백신 등 신기술 상용화"
                    ],
                    "opportunities": [
                        "바이오인포매틱스 전문가 수요 증가",
                        "디지털 치료제 개발 인력 필요",
                        "임상시험 및 규제 전문가 부족"
                    ]
                }
            }
            
            if selected in trend_info:
                info = trend_info[selected]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**시장 규모:** {info['market_size']}")
                with col2:
                    st.success(f"**성장 전망:** {info['growth_forecast']}")
                
                st.markdown("**🔥 주요 트렌드**")
                for trend in info['trends']:
                    st.markdown(f"- {trend}")
                
                st.markdown("**💡 진로 기회**")
                for opp in info['opportunities']:
                    st.markdown(f"- {opp}")


elif menu == "💼 직업 검색":
    st.markdown('<div class="main-header">💼 직업 검색</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 직업명을 검색하세요", placeholder="예: 데이터 사이언티스트, AI 엔지니어")
    with col2:
        field_filter = st.selectbox("분야 필터", ["전체"] + list(industries.keys()) if 'industries' in locals() else ["전체"])
    
    if search_query:
        # 검색어를 세션에 저장
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.insert(0, search_query)
            st.session_state.search_history = st.session_state.search_history[:10]  # 최근 10개만 유지
        
        # 검색 실행
        field = None if field_filter == "전체" else field_filter
        search_results = data_manager.search_jobs_by_keyword(search_query, field)
        
        if search_results:
            st.success(f"'{search_query}' 검색 결과: {len(search_results)}개의 직업을 찾았습니다")
            
            # 결과를 카드 형식으로 표시
            for idx, job in enumerate(search_results):
                with st.expander(f"**{job['name']}** - {job.get('growth', '정보 없음')}"):
                    job_detail = data_manager.get_job_details(job['code'])
                    
                    if job_detail:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**📝 직업 설명**")
                            st.markdown(job_detail.get('description', ''))
                            
                            st.markdown(f"**🔧 주요 업무**")
                            for task in job_detail.get('main_tasks', []):
                                st.markdown(f"- {task}")
                        
                        with col2:
                            st.markdown(f"**📊 기본 정보**")
                            st.info(f"**분야:** {job_detail.get('field', '')}")
                            st.info(f"**연봉:** {job_detail.get('salary_range', '')}")
                            st.info(f"**전망:** {job_detail.get('outlook', '')}")
                            st.info(f"**성장률:** {job_detail.get('growth_rate', '')}")
                        
                        # 상세 정보 버튼
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button("📚 상세 정보", key=f"detail_btn_{job['code']}"):
                                st.session_state.selected_job_code = job['code']
                                st.rerun()
                        with col_b:
                            if st.button("🎓 학과 연결", key=f"major_btn_{job['code']}"):
                                st.session_state.job_for_major = job['code']
                                st.rerun()
                        with col_c:
                            # 비교 목록에 추가
                            if st.button("➕ 비교 추가", key=f"compare_btn_{job['code']}"):
                                if job['code'] not in st.session_state.selected_jobs_for_comparison:
                                    st.session_state.selected_jobs_for_comparison.append(job['code'])
                                    st.success(f"{job['name']}을(를) 비교 목록에 추가했습니다")
        else:
            st.warning(f"'{search_query}'에 대한 검색 결과가 없습니다")
    
    # 검색 기록
    if st.session_state.search_history:
        with st.sidebar:
            st.markdown("### 📜 최근 검색")
            for query in st.session_state.search_history[:5]:
                if st.button(query, key=f"history_{query}"):
                    search_query = query
                    st.rerun()
    
    # 선택된 직업 상세 정보
    if 'selected_job_code' in st.session_state and st.session_state.selected_job_code:
        st.markdown("---")
        job_code = st.session_state.selected_job_code
        job_data = data_manager.get_job_details(job_code)
        
        if job_data:
            st.markdown(f'<div class="sub-header">💼 {job_data["job_name"]} 상세 정보</div>', unsafe_allow_html=True)
            
            # 기본 정보 섹션
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("연봉 범위", job_data.get('salary_range', '정보 없음'))
            with col2:
                st.metric("전망", job_data.get('outlook', '정보 없음'))
            with col3:
                st.metric("성장률", job_data.get('growth_rate', '정보 없음'))
            with col4:
                st.metric("취업률", job_data.get('employment_rate', '정보 없음'))
            
            # 탭으로 상세 정보 구성
            tab1, tab2, tab3, tab4 = st.tabs(["📋 직업 소개", "🎓 진학 정보", "💪 필요 역량", "🗺️ 진로 경로"])
            
            with tab1:
                st.markdown("### 직업 설명")
                st.markdown(job_data.get('description', ''))
                
                st.markdown("### 주요 업무")
                for task in job_data.get('main_tasks', []):
                    st.markdown(f"- {task}")
                
                st.markdown("### 학력 요구")
                st.info(job_data.get('required_education', ''))
            
            with tab2:
                st.markdown("### 관련 대학 전공")
                majors = job_data.get('related_majors', [])
                cols = st.columns(min(len(majors), 3))
                for idx, major in enumerate(majors):
                    with cols[idx % 3]:
                        st.success(f"🎓 {major}")
                
                st.markdown("### 고등학교 권장 선택과목")
                subjects = job_data.get('high_school_subjects', [])
                cols = st.columns(min(len(subjects), 4))
                for idx, subject in enumerate(subjects):
                    with cols[idx % 4]:
                        st.info(f"📚 {subject}")
            
            with tab3:
                st.markdown("### 필요한 기술 및 역량")
                skills = job_data.get('required_skills', [])
                for skill in skills:
                    st.markdown(f"- {skill}")
                
                st.markdown("### 관련 자격증")
                certs = job_data.get('certifications', [])
                for cert in certs:
                    st.markdown(f"- {cert}")
                
                # 역량 차트
                st.plotly_chart(
                    visualizer.create_skill_requirement_chart(job_data),
                    use_container_width=True
                )
            
            with tab4:
                # 진로 경로 시각화
                path_data = data_manager.get_career_path_data(job_code)
                st.plotly_chart(
                    visualizer.create_career_path_network(path_data),
                    use_container_width=True
                )
                
                st.markdown("### 단계별 상세 설명")
                for idx, step in enumerate(path_data.get('steps', []), 1):
                    st.markdown(f"**{idx}단계:** {step}")
            
            # 닫기 버튼
            if st.button("← 검색 결과로 돌아가기"):
                st.session_state.selected_job_code = None
                st.rerun()

elif menu == "🎓 학과 연결":
    st.markdown('<div class="main-header">🎓 직업-학과 연결</div>', unsafe_allow_html=True)
    
    st.markdown("""
    이 기능은 특정 직업에 진출하기 위해 필요한 대학 전공과 고등학교 선택과목을 연결해줍니다.
    직업을 선택하거나 검색하여 관련 학과 정보를 확인하세요.
    """)
    
    # 직업 선택 방법
    selection_method = st.radio(
        "직업 선택 방법",
        ["직접 검색", "분야별 선택"],
        horizontal=True
    )
    
    selected_job_code = None
    
    if selection_method == "직접 검색":
        job_search = st.text_input("직업명 검색", placeholder="예: AI 엔지니어")
        if job_search:
            jobs = data_manager.search_jobs_by_keyword(job_search)
            if jobs:
                job_options = {f"{job['name']} ({job.get('growth', '')})": job['code'] for job in jobs}
                selected_job = st.selectbox("검색 결과에서 선택", list(job_options.keys()))
                selected_job_code = job_options[selected_job]
    else:
        # 분야별 선택
        industries_list = ["AI/빅데이터", "바이오헬스", "친환경에너지", "메타버스/XR", 
                          "자율주행/모빌리티", "로봇공학", "우주항공", "스마트시티"]
        selected_field = st.selectbox("신산업 분야 선택", industries_list)
        
        jobs_in_field = data_manager.get_industry_jobs(selected_field)
        if jobs_in_field:
            job_options = {job['name']: job['code'] for job in jobs_in_field}
            selected_job = st.selectbox("직업 선택", list(job_options.keys()))
            selected_job_code = job_options[selected_job]
    
    # 선택된 직업의 학과 연결 정보 표시
    if selected_job_code:
        st.markdown("---")
        mapping = data_manager.get_job_to_major_mapping(selected_job_code)
        
        if mapping:
            st.markdown(f'<div class="sub-header">🎯 {mapping["job_name"]} 진학 경로</div>', unsafe_allow_html=True)
            
            # 4단계 진로 경로 표시
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("### 1️⃣ 고등학교")
                st.markdown("**권장 선택과목**")
                for subject in mapping.get('high_school_subjects', []):
                    st.success(f"📚 {subject}")
            
            with col2:
                st.markdown("### 2️⃣ 대학 전공")
                st.markdown("**관련 학과**")
                for major in mapping.get('related_majors', [])[:5]:
                    st.info(f"🎓 {major}")
            
            with col3:
                st.markdown("### 3️⃣ 학력 요구")
                education = mapping.get('required_education', '')
                st.warning(f"📜 {education}")
            
            with col4:
                st.markdown("### 4️⃣ 취업")
                st.markdown("**진로 경로**")
                st.success("🎯 목표 직업 달성")
            
            # 상세 진로 경로
            st.markdown("---")
            st.markdown("### 📍 상세 진로 경로")
            career_path = mapping.get('career_path', '')
            if career_path:
                steps = career_path.split('→')
                for idx, step in enumerate(steps, 1):
                    st.markdown(f"**{idx}단계:** {step.strip()}")
            
            # 관련 학과 상세 정보
            st.markdown("---")
            st.markdown("### 🎓 관련 학과 상세 정보")
            
            majors = mapping.get('related_majors', [])
            for major in majors[:3]:  # 상위 3개 학과
                with st.expander(f"📖 {major}"):
                    st.markdown(f"""
                    **학과 소개**
                    - 이 학과는 {mapping['job_name']} 직업에 필요한 핵심 지식을 제공합니다
                    - 관련 자격증 취득 및 실무 역량 개발 기회 제공
                    
                    **주요 교육 내용**
                    - 전공 기초 이론 학습
                    - 실습 및 프로젝트 경험
                    - 산학협력 및 인턴십 기회
                    
                    **진출 분야**
                    - {mapping['job_name']} 및 관련 직종
                    """)

elif menu == "📊 직업 비교":
    st.markdown('<div class="main-header">📊 직업 비교 분석</div>', unsafe_allow_html=True)
    
    # 현재 비교 목록 표시
    if st.session_state.selected_jobs_for_comparison:
        st.info(f"현재 {len(st.session_state.selected_jobs_for_comparison)}개 직업이 비교 목록에 있습니다")
        
        # 비교 목록 관리
        cols = st.columns(len(st.session_state.selected_jobs_for_comparison))
        for idx, job_code in enumerate(st.session_state.selected_jobs_for_comparison):
            job = data_manager.get_job_details(job_code)
            with cols[idx]:
                st.markdown(f"**{job.get('job_name', '')}**")
                if st.button("❌ 제거", key=f"remove_{job_code}"):
                    st.session_state.selected_jobs_for_comparison.remove(job_code)
                    st.rerun()
    
    # 직업 추가
    st.markdown("### ➕ 비교할 직업 추가")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        add_job_search = st.text_input("직업명 검색", placeholder="비교할 직업을 검색하세요")
    with col2:
        field_filter_compare = st.selectbox("분야", ["전체", "AI/빅데이터", "바이오헬스", "친환경에너지"])
    
    if add_job_search:
        field = None if field_filter_compare == "전체" else field_filter_compare
        search_results = data_manager.search_jobs_by_keyword(add_job_search, field)
        
        if search_results:
            for job in search_results[:5]:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{job['name']}** - {job.get('growth', '')}")
                with col_b:
                    if st.button("추가", key=f"add_{job['code']}"):
                        if job['code'] not in st.session_state.selected_jobs_for_comparison:
                            if len(st.session_state.selected_jobs_for_comparison) < 5:
                                st.session_state.selected_jobs_for_comparison.append(job['code'])
                                st.rerun()
                            else:
                                st.warning("최대 5개까지만 비교 가능합니다")
    
    # 비교 분석 실행
    if len(st.session_state.selected_jobs_for_comparison) >= 2:
        st.markdown("---")
        st.markdown("### 📊 비교 분석 결과")
        
        # 비교 데이터 생성
        comparison_df = data_manager.compare_jobs(st.session_state.selected_jobs_for_comparison)
        
        # 표로 비교
        st.markdown("#### 기본 정보 비교")
        st.dataframe(comparison_df, use_container_width=True)
        
        # 레이더 차트
        st.markdown("#### 종합 비교 차트")
        st.plotly_chart(
            visualizer.create_job_comparison_radar(comparison_df),
            use_container_width=True
        )
        
        # 연봉 비교
        st.markdown("#### 연봉 범위 비교")
        job_details = [data_manager.get_job_details(code) for code in st.session_state.selected_jobs_for_comparison]
        st.plotly_chart(
            visualizer.create_salary_distribution(job_details),
            use_container_width=True
        )
        
        # 종합 분석 및 추천
        st.markdown("---")
        st.markdown("### 💡 AI 종합 분석 및 추천")
        
        with st.expander("📝 분석 보고서 보기"):
            st.markdown("""
            **비교 분석 요약**
            
            선택하신 직업들을 다각도로 분석한 결과입니다:
            
            1. **전망 및 성장성**: 모든 직업이 신산업 분야로 긍정적인 전망을 가지고 있습니다
            2. **연봉 수준**: 직업별로 차이가 있으나, 경력에 따라 상승 가능성이 높습니다
            3. **학력 요구**: 대부분 학사 이상의 학력이 필요하며, 일부는 석사 이상을 요구합니다
            4. **진입 장벽**: 전문 기술과 지식이 필요하여 체계적인 준비가 중요합니다
            
            **추천 사항**
            - 본인의 흥미와 적성을 가장 우선적으로 고려하세요
            - 학력 요구사항과 필요 역량을 확인하여 계획을 수립하세요
            - 고등학교 선택과목부터 전략적으로 준비하세요
            """)
        
        # 비교 목록 초기화
        if st.button("🔄 비교 목록 초기화"):
            st.session_state.selected_jobs_for_comparison = []
            st.rerun()
    
    elif st.session_state.selected_jobs_for_comparison:
        st.warning("비교하려면 최소 2개 이상의 직업을 선택해주세요")
    else:
        st.info("비교할 직업을 추가해주세요 (최대 5개)")

elif menu == "🗺️ 진로 경로":
    st.markdown('<div class="main-header">🗺️ 진로 경로 시각화</div>', unsafe_allow_html=True)
    
    st.markdown("""
    목표 직업까지의 진로 경로를 시각적으로 확인하고, 각 단계별로 필요한 준비사항을 파악하세요.
    """)
    
    # 직업 선택
    job_search_path = st.text_input("직업명 검색", placeholder="진로 경로를 확인할 직업 검색")
    
    if job_search_path:
        jobs = data_manager.search_jobs_by_keyword(job_search_path)
        if jobs:
            job_options = {job['name']: job['code'] for job in jobs}
            selected_job_name = st.selectbox("직업 선택", list(job_options.keys()))
            selected_job_code_path = job_options[selected_job_name]
            
            # 진로 경로 데이터 가져오기
            path_data = data_manager.get_career_path_data(selected_job_code_path)
            job_detail = data_manager.get_job_details(selected_job_code_path)
            
            if path_data and job_detail:
                # 진로 경로 네트워크 그래프
                st.plotly_chart(
                    visualizer.create_career_path_network(path_data),
                    use_container_width=True
                )
                
                # 단계별 상세 정보
                st.markdown("---")
                st.markdown("### 📋 단계별 준비사항")
                
                steps = path_data.get('steps', [])
                
                for idx, step in enumerate(steps, 1):
                    with st.expander(f"**{idx}단계: {step}**", expanded=(idx == 1)):
                        if idx == 1:  # 고등학교 단계
                            st.markdown("**🏫 고등학교 준비사항**")
                            st.markdown("권장 선택과목:")
                            for subject in path_data.get('high_school_subjects', []):
                                st.markdown(f"- {subject}")
                            st.markdown("""
                            - 관련 동아리 활동 참여
                            - 관심 분야 독서 및 탐구 활동
                            - 진로 관련 체험 활동 및 멘토링
                            """)
                        
                        elif "대학" in step or "전공" in step:  # 대학 단계
                            st.markdown("**🎓 대학 전공 선택**")
                            st.markdown("추천 학과:")
                            for major in path_data.get('related_majors', []):
                                st.markdown(f"- {major}")
                            st.markdown("""
                            - 전공 관련 심화 학습
                            - 프로젝트 및 공모전 참여
                            - 인턴십 및 실무 경험
                            - 관련 자격증 취득
                            """)
                        
                        elif "석사" in step or "박사" in step:  # 대학원 단계
                            st.markdown("**🎯 대학원 진학**")
                            st.markdown("""
                            - 연구 경험 쌓기
                            - 학술 논문 작성 및 발표
                            - 전문 분야 깊이 있는 학습
                            - 산학협력 프로젝트 참여
                            """)
                        
                        else:  # 취업 및 경력 단계
                            st.markdown("**💼 실무 경력 개발**")
                            st.markdown("""
                            - 지속적인 자기개발
                            - 최신 기술 및 트렌드 학습
                            - 네트워킹 및 커뮤니티 활동
                            - 프로젝트 리더십 경험
                            """)
                
                # 필요 역량 및 자격증
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💪 필요한 역량")
                    for skill in path_data.get('required_skills', []):
                        st.markdown(f"- {skill}")
                
                with col2:
                    st.markdown("### 📜 관련 자격증")
                    for cert in job_detail.get('certifications', []):
                        st.markdown(f"- {cert}")
                
                # 타임라인 예시
                st.markdown("---")
                st.markdown("### ⏱️ 예상 타임라인")
                
                timeline_data = {
                    "단계": steps,
                    "예상 기간": ["3년", "4년", "2년(선택)", "3-5년", "5년+"][:len(steps)],
                    "누적 기간": ["고1-고3", "19-22세", "23-24세", "25-30세", "30세+"][:len(steps)]
                }
                
                timeline_df = pd.DataFrame(timeline_data)
                st.table(timeline_df)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>💡 경기도교육청 진로전담교사 지원 시스템</p>
    <p>데이터 출처: 워크넷, 커리어넷, 한국고용정보원</p>
    <p style='font-size: 0.8rem;'>Last Updated: 2025-11-15</p>
</div>
""", unsafe_allow_html=True)
