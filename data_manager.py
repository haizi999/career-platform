"""
워크넷 및 커리어넷 API 연동 모듈
신산업 직업 정보를 수집하고 가공하는 기능 제공
"""

import requests
import pandas as pd
import json
from typing import List, Dict, Optional
import time

class WorkNetAPI:
    """워크넷 Open API 연동 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        워크넷 API 초기화
        
        Args:
            api_key: 워크넷 API 인증키 (없으면 샘플 데이터 사용)
        """
        self.api_key = api_key
        self.base_url = "http://openapi.work.go.kr/opi/opi/opia"
        
    def get_job_info(self, job_code: str) -> Dict:
        """
        직업 상세 정보 조회
        
        Args:
            job_code: 직업 코드
            
        Returns:
            직업 정보 딕셔너리
        """
        if not self.api_key:
            return self._get_sample_job_data(job_code)
        
        # 실제 API 호출 로직
        endpoint = f"{self.base_url}/jobInfoSrch.do"
        params = {
            'authKey': self.api_key,
            'returnType': 'JSON',
            'svcCode': job_code
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API 호출 오류: {e}")
            return self._get_sample_job_data(job_code)
    
    def search_jobs(self, keyword: str, field: Optional[str] = None) -> List[Dict]:
        """
        키워드로 직업 검색
        
        Args:
            keyword: 검색 키워드
            field: 신산업 분야 (선택)
            
        Returns:
            직업 목록
        """
        if not self.api_key:
            return self._get_sample_jobs_by_keyword(keyword, field)
        
        # 실제 API 호출 로직
        endpoint = f"{self.base_url}/jobSrch.do"
        params = {
            'authKey': self.api_key,
            'returnType': 'JSON',
            'keyword': keyword
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('jobs', [])
        except Exception as e:
            print(f"API 호출 오류: {e}")
            return self._get_sample_jobs_by_keyword(keyword, field)
    
    def get_major_info(self, major_code: str) -> Dict:
        """
        학과 정보 조회
        
        Args:
            major_code: 학과 코드
            
        Returns:
            학과 정보 딕셔너리
        """
        if not self.api_key:
            return self._get_sample_major_data(major_code)
        
        # 실제 API 호출 로직 (학과정보 API)
        return self._get_sample_major_data(major_code)
    
    def _get_sample_job_data(self, job_code: str) -> Dict:
        """샘플 직업 데이터 반환"""
        sample_jobs = {
            "AI001": {
                "job_code": "AI001",
                "job_name": "AI 엔지니어",
                "field": "AI/빅데이터",
                "description": "인공지능 알고리즘을 개발하고 AI 시스템을 구축하는 전문가",
                "main_tasks": [
                    "머신러닝 모델 개발 및 최적화",
                    "딥러닝 알고리즘 연구 및 구현",
                    "AI 시스템 설계 및 구축",
                    "데이터 전처리 및 분석"
                ],
                "required_education": "학사 이상 (컴퓨터공학, 인공지능, 데이터사이언스 등)",
                "required_skills": [
                    "Python, TensorFlow, PyTorch",
                    "머신러닝/딥러닝 이론",
                    "수학(선형대수, 확률통계)",
                    "데이터 분석 능력"
                ],
                "certifications": ["정보처리기사", "빅데이터분석기사", "AI 관련 자격증"],
                "salary_range": "4,000만원 ~ 8,000만원",
                "outlook": "매우 높음",
                "growth_rate": "25%",
                "employment_rate": "95%",
                "related_majors": ["컴퓨터공학", "인공지능학", "데이터사이언스", "통계학", "수학"],
                "high_school_subjects": ["수학", "정보", "과학(물리)", "영어"],
                "career_path": "대학 전공 → 석사(선택) → AI 엔지니어 → 시니어 AI 엔지니어 → AI 연구원/리더"
            },
            "BIZ001": {
                "job_code": "BIZ001",
                "job_name": "경영 컨설턴트",
                "field": "경영/컨설팅",
                "description": "기업의 경영 문제를 분석하고 개선 방안을 제시하는 전문가",
                "main_tasks": [
                    "기업 현황 분석 및 진단",
                    "경영 전략 수립 및 제안",
                    "프로젝트 관리 및 실행",
                    "성과 측정 및 개선"
                ],
                "required_education": "학사 이상 (경영학, 경제학 등)",
                "required_skills": [
                    "전략적 사고력",
                    "데이터 분석 능력",
                    "프레젠테이션 스킬",
                    "커뮤니케이션 능력"
                ],
                "certifications": ["경영지도사", "CPA", "CFA"],
                "salary_range": "3,500만원 ~ 8,000만원",
                "outlook": "높음",
                "growth_rate": "15%",
                "employment_rate": "85%",
                "related_majors": ["경영학", "경제학", "산업공학", "통계학"],
                "high_school_subjects": ["수학", "사회", "영어", "경제"],
                "career_path": "대학 전공 → 컨설팅 펌 입사 → 주니어 컨설턴트 → 시니어 컨설턴트 → 매니저 → 파트너"
            },
            "PSY001": {
                "job_code": "PSY001",
                "job_name": "임상심리사",
                "field": "심리/상담",
                "description": "심리적 문제를 진단하고 치료하는 전문가",
                "main_tasks": [
                    "심리 평가 및 진단",
                    "심리 치료 및 상담",
                    "치료 계획 수립",
                    "사례 관리 및 기록"
                ],
                "required_education": "석사 이상 (심리학)",
                "required_skills": [
                    "심리학 이론 지식",
                    "상담 기법",
                    "공감 능력",
                    "윤리적 판단력"
                ],
                "certifications": ["임상심리사 1급", "임상심리사 2급"],
                "salary_range": "3,000만원 ~ 6,000만원",
                "outlook": "높음",
                "growth_rate": "12%",
                "employment_rate": "80%",
                "related_majors": ["심리학", "상담학"],
                "high_school_subjects": ["사회", "생활과 윤리", "영어"],
                "career_path": "심리학 학사 → 석사 필수 → 임상심리사 자격증 → 병원/센터 근무 → 수련 → 전문가"
            },
            "ART001": {
                "job_code": "ART001",
                "job_name": "UX/UI 디자이너",
                "field": "예술/디자인",
                "description": "사용자 경험과 인터페이스를 디자인하는 전문가",
                "main_tasks": [
                    "사용자 조사 및 분석",
                    "와이어프레임 및 프로토타입 제작",
                    "UI 디자인 및 가이드 작성",
                    "사용성 테스트 진행"
                ],
                "required_education": "학사 이상 (디자인, 시각디자인 등)",
                "required_skills": [
                    "Figma, Sketch, Adobe XD",
                    "사용자 중심 디자인",
                    "프로토타이핑",
                    "디자인 시스템 구축"
                ],
                "certifications": ["시각디자인기사", "컴퓨터그래픽스운용기능사"],
                "salary_range": "3,500만원 ~ 7,000만원",
                "outlook": "매우 높음",
                "growth_rate": "20%",
                "employment_rate": "90%",
                "related_majors": ["시각디자인", "산업디자인", "디지털미디어디자인"],
                "high_school_subjects": ["미술", "정보", "영어"],
                "career_path": "대학 전공 → 주니어 디자이너 → UX/UI 디자이너 → 시니어 디자이너 → 디자인 리드"
            },
            "SPT002": {
                "job_code": "SPT002",
                "job_name": "스포츠 데이터 분석가",
                "field": "체육/스포츠",
                "description": "스포츠 경기 및 선수 데이터를 분석하여 전략을 제시하는 전문가",
                "main_tasks": [
                    "경기 데이터 수집 및 분석",
                    "선수 퍼포먼스 분석",
                    "전략 수립 지원",
                    "데이터 시각화 및 리포팅"
                ],
                "required_education": "학사 이상 (체육학, 통계학, 데이터사이언스 등)",
                "required_skills": [
                    "Python, R",
                    "통계 분석",
                    "스포츠 지식",
                    "데이터 시각화"
                ],
                "certifications": ["빅데이터분석기사", "생활스포츠지도사"],
                "salary_range": "3,000만원 ~ 6,000만원",
                "outlook": "높음",
                "growth_rate": "18%",
                "employment_rate": "75%",
                "related_majors": ["체육학", "스포츠과학", "통계학", "데이터사이언스"],
                "high_school_subjects": ["수학", "체육", "정보"],
                "career_path": "대학 전공 → 데이터 분석 실무 → 스포츠 팀 분석가 → 수석 분석가"
            },
            "EDU003": {
                "job_code": "EDU003",
                "job_name": "에듀테크 전문가",
                "field": "교육",
                "description": "교육과 기술을 융합한 학습 솔루션을 개발하는 전문가",
                "main_tasks": [
                    "교육용 앱/플랫폼 기획",
                    "학습 콘텐츠 설계",
                    "AI 기반 학습 시스템 개발",
                    "교육 효과 분석"
                ],
                "required_education": "학사 이상 (교육학, 컴퓨터공학 등)",
                "required_skills": [
                    "교육학 이론",
                    "프로그래밍 기초",
                    "UX/UI 디자인",
                    "프로젝트 관리"
                ],
                "certifications": ["교사 자격증", "정보처리기사"],
                "salary_range": "3,500만원 ~ 7,000만원",
                "outlook": "매우 높음",
                "growth_rate": "22%",
                "employment_rate": "85%",
                "related_majors": ["교육학", "교육공학", "컴퓨터공학"],
                "high_school_subjects": ["수학", "정보", "사회", "영어"],
                "career_path": "대학 전공 → 에듀테크 기업 입사 → 콘텐츠 개발자 → 프로덕트 매니저"
            },
            "MDA001": {
                "job_code": "MDA001",
                "job_name": "유튜버/크리에이터",
                "field": "미디어/콘텐츠",
                "description": "영상 콘텐츠를 기획, 제작, 유통하는 1인 미디어 전문가",
                "main_tasks": [
                    "콘텐츠 기획 및 제작",
                    "영상 촬영 및 편집",
                    "채널 운영 및 마케팅",
                    "시청자 소통 및 관리"
                ],
                "required_education": "학력 무관 (관련 학과 우대)",
                "required_skills": [
                    "영상 편집 (프리미어, 파이널컷)",
                    "기획력 및 창의성",
                    "커뮤니케이션 능력",
                    "SNS 마케팅"
                ],
                "certifications": ["방송편집기사(선택)"],
                "salary_range": "변동 큼 (월 100만원 ~ 수천만원)",
                "outlook": "높음",
                "growth_rate": "15%",
                "employment_rate": "자영업",
                "related_majors": ["방송영상학", "미디어커뮤니케이션", "영화학"],
                "high_school_subjects": ["국어", "영어", "미술"],
                "career_path": "콘텐츠 제작 시작 → 구독자 확보 → 수익화 → 전문 크리에이터 → MCN 계약/개인 브랜드"
            }
        }
            "BIO001": {
                "job_code": "BIO001",
                "job_name": "바이오인포매틱스 연구원",
                "field": "바이오헬스",
                "description": "생물학 데이터를 컴퓨터로 분석하여 생명현상을 연구하는 전문가",
                "main_tasks": [
                    "유전체 데이터 분석",
                    "바이오 빅데이터 처리",
                    "생물정보 알고리즘 개발",
                    "신약 개발 지원"
                ],
                "required_education": "석사 이상 (생명과학, 생물정보학, 컴퓨터공학 등)",
                "required_skills": [
                    "Python, R 프로그래밍",
                    "생물학 지식",
                    "통계분석",
                    "데이터베이스 관리"
                ],
                "certifications": ["생물공학기사", "생명공학기사"],
                "salary_range": "3,500만원 ~ 7,000만원",
                "outlook": "높음",
                "growth_rate": "18%",
                "employment_rate": "88%",
                "related_majors": ["생명과학", "생물정보학", "바이오공학", "컴퓨터공학"],
                "high_school_subjects": ["생명과학", "화학", "수학", "정보"],
                "career_path": "대학 전공 → 석사 필수 → 연구원 → 선임연구원 → 책임연구원"
            },
            "ECO001": {
                "job_code": "ECO001",
                "job_name": "신재생에너지 엔지니어",
                "field": "친환경에너지",
                "description": "태양광, 풍력 등 신재생에너지 시스템을 설계하고 관리하는 전문가",
                "main_tasks": [
                    "신재생에너지 시스템 설계",
                    "발전소 운영 및 관리",
                    "에너지 효율 분석",
                    "환경영향 평가"
                ],
                "required_education": "학사 이상 (전기공학, 기계공학, 에너지공학 등)",
                "required_skills": [
                    "전기/전자 지식",
                    "에너지 시스템 이해",
                    "CAD 설계",
                    "환경공학 기초"
                ],
                "certifications": ["전기기사", "에너지관리기사", "신재생에너지발전설비기사"],
                "salary_range": "3,000만원 ~ 6,000만원",
                "outlook": "매우 높음",
                "growth_rate": "22%",
                "employment_rate": "90%",
                "related_majors": ["전기공학", "에너지공학", "기계공학", "환경공학"],
                "high_school_subjects": ["물리학", "수학", "화학", "지구과학"],
                "career_path": "대학 전공 → 엔지니어 → 선임엔지니어 → 프로젝트 매니저"
            }
        }
        
        return sample_jobs.get(job_code, {})
    
    def _get_sample_jobs_by_keyword(self, keyword: str, field: Optional[str] = None) -> List[Dict]:
        """키워드 기반 샘플 직업 데이터 반환"""
        
        all_jobs = {
            "AI/빅데이터": [
                {"code": "AI001", "name": "AI 엔지니어", "growth": "매우 높음", "field": "AI/빅데이터"},
                {"code": "AI002", "name": "데이터 사이언티스트", "growth": "매우 높음", "field": "AI/빅데이터"},
                {"code": "AI003", "name": "머신러닝 엔지니어", "growth": "매우 높음", "field": "AI/빅데이터"},
                {"code": "AI004", "name": "AI 윤리 전문가", "growth": "높음", "field": "AI/빅데이터"},
                {"code": "AI005", "name": "자연어처리 전문가", "growth": "높음", "field": "AI/빅데이터"},
                {"code": "AI006", "name": "컴퓨터비전 엔지니어", "growth": "높음", "field": "AI/빅데이터"},
                {"code": "AI007", "name": "빅데이터 아키텍트", "growth": "높음", "field": "AI/빅데이터"},
                {"code": "AI008", "name": "데이터 엔지니어", "growth": "높음", "field": "AI/빅데이터"},
            ],
            "바이오헬스": [
                {"code": "BIO001", "name": "바이오인포매틱스 연구원", "growth": "높음", "field": "바이오헬스"},
                {"code": "BIO002", "name": "유전체 분석가", "growth": "높음", "field": "바이오헬스"},
                {"code": "BIO003", "name": "신약 개발 연구원", "growth": "중상", "field": "바이오헬스"},
                {"code": "BIO004", "name": "바이오 데이터 분석가", "growth": "높음", "field": "바이오헬스"},
                {"code": "BIO005", "name": "의료 AI 전문가", "growth": "매우 높음", "field": "바이오헬스"},
                {"code": "BIO006", "name": "재생의학 연구원", "growth": "중상", "field": "바이오헬스"},
            ],
            "친환경에너지": [
                {"code": "ECO001", "name": "신재생에너지 엔지니어", "growth": "매우 높음", "field": "친환경에너지"},
                {"code": "ECO002", "name": "탄소배출권 거래 전문가", "growth": "높음", "field": "친환경에너지"},
                {"code": "ECO003", "name": "수소에너지 연구원", "growth": "매우 높음", "field": "친환경에너지"},
                {"code": "ECO004", "name": "ESG 컨설턴트", "growth": "높음", "field": "친환경에너지"},
                {"code": "ECO005", "name": "친환경 건축 설계사", "growth": "중상", "field": "친환경에너지"},
            ],
            "메타버스/XR": [
                {"code": "META001", "name": "메타버스 플랫폼 개발자", "growth": "매우 높음", "field": "메타버스/XR"},
                {"code": "META002", "name": "XR 콘텐츠 디자이너", "growth": "높음", "field": "메타버스/XR"},
                {"code": "META003", "name": "3D 모델러", "growth": "높음", "field": "메타버스/XR"},
                {"code": "META004", "name": "가상세계 건축가", "growth": "중상", "field": "메타버스/XR"},
                {"code": "META005", "name": "NFT 아트 디렉터", "growth": "중상", "field": "메타버스/XR"},
            ],
            "자율주행/모빌리티": [
                {"code": "AUTO001", "name": "자율주행 엔지니어", "growth": "매우 높음", "field": "자율주행/모빌리티"},
                {"code": "AUTO002", "name": "모빌리티 데이터 분석가", "growth": "높음", "field": "자율주행/모빌리티"},
                {"code": "AUTO003", "name": "전기차 배터리 연구원", "growth": "매우 높음", "field": "자율주행/모빌리티"},
                {"code": "AUTO004", "name": "커넥티드카 보안 전문가", "growth": "높음", "field": "자율주행/모빌리티"},
            ],
            "로봇공학": [
                {"code": "ROB001", "name": "로봇 엔지니어", "growth": "높음", "field": "로봇공학"},
                {"code": "ROB002", "name": "협동로봇 전문가", "growth": "중상", "field": "로봇공학"},
                {"code": "ROB003", "name": "로봇 비전 개발자", "growth": "높음", "field": "로봇공학"},
                {"code": "ROB004", "name": "의료로봇 연구원", "growth": "중상", "field": "로봇공학"},
            ],
            "우주항공": [
                {"code": "SPACE001", "name": "위성 시스템 엔지니어", "growth": "중상", "field": "우주항공"},
                {"code": "SPACE002", "name": "우주탐사 연구원", "growth": "중", "field": "우주항공"},
                {"code": "SPACE003", "name": "항공우주 데이터 분석가", "growth": "중상", "field": "우주항공"},
            ],
            "스마트시티": [
                {"code": "CITY001", "name": "스마트시티 플래너", "growth": "중상", "field": "스마트시티"},
                {"code": "CITY002", "name": "IoT 솔루션 아키텍트", "growth": "높음", "field": "스마트시티"},
                {"code": "CITY003", "name": "도시데이터 분석가", "growth": "중상", "field": "스마트시티"},
                {"code": "CITY004", "name": "스마트빌딩 엔지니어", "growth": "중", "field": "스마트시티"},
            ],
            "경영/컨설팅": [
                {"code": "BIZ001", "name": "경영 컨설턴트", "growth": "높음", "field": "경영/컨설팅"},
                {"code": "BIZ002", "name": "전략 기획자", "growth": "중상", "field": "경영/컨설팅"},
                {"code": "BIZ003", "name": "마케팅 매니저", "growth": "중상", "field": "경영/컨설팅"},
                {"code": "BIZ004", "name": "브랜드 매니저", "growth": "중", "field": "경영/컨설팅"},
                {"code": "BIZ005", "name": "HR 전문가", "growth": "중", "field": "경영/컨설팅"},
                {"code": "BIZ006", "name": "재무 분석가", "growth": "중상", "field": "경영/컨설팅"},
                {"code": "BIZ007", "name": "회계사", "growth": "중", "field": "경영/컨설팅"},
                {"code": "BIZ008", "name": "세무사", "growth": "중", "field": "경영/컨설팅"},
            ],
            "심리/상담": [
                {"code": "PSY001", "name": "임상심리사", "growth": "높음", "field": "심리/상담"},
                {"code": "PSY002", "name": "상담심리사", "growth": "높음", "field": "심리/상담"},
                {"code": "PSY003", "name": "산업 및 조직심리사", "growth": "중상", "field": "심리/상담"},
                {"code": "PSY004", "name": "교육심리사", "growth": "중", "field": "심리/상담"},
                {"code": "PSY005", "name": "진로상담사", "growth": "중상", "field": "심리/상담"},
                {"code": "PSY006", "name": "놀이치료사", "growth": "중", "field": "심리/상담"},
            ],
            "예술/디자인": [
                {"code": "ART001", "name": "UX/UI 디자이너", "growth": "매우 높음", "field": "예술/디자인"},
                {"code": "ART002", "name": "그래픽 디자이너", "growth": "중", "field": "예술/디자인"},
                {"code": "ART003", "name": "영상 디자이너", "growth": "높음", "field": "예술/디자인"},
                {"code": "ART004", "name": "애니메이터", "growth": "중상", "field": "예술/디자인"},
                {"code": "ART005", "name": "게임 아트 디렉터", "growth": "높음", "field": "예술/디자인"},
                {"code": "ART006", "name": "웹툰 작가", "growth": "높음", "field": "예술/디자인"},
                {"code": "ART007", "name": "일러스트레이터", "growth": "중", "field": "예술/디자인"},
            ],
            "체육/스포츠": [
                {"code": "SPT001", "name": "스포츠 마케터", "growth": "중상", "field": "체육/스포츠"},
                {"code": "SPT002", "name": "스포츠 데이터 분석가", "growth": "높음", "field": "체육/스포츠"},
                {"code": "SPT003", "name": "운동처방사", "growth": "중", "field": "체육/스포츠"},
                {"code": "SPT004", "name": "퍼스널 트레이너", "growth": "중", "field": "체육/스포츠"},
                {"code": "SPT005", "name": "스포츠 에이전트", "growth": "중", "field": "체육/스포츠"},
            ],
            "교육": [
                {"code": "EDU001", "name": "교사", "growth": "중", "field": "교육"},
                {"code": "EDU002", "name": "교육 컨텐츠 개발자", "growth": "높음", "field": "교육"},
                {"code": "EDU003", "name": "에듀테크 전문가", "growth": "매우 높음", "field": "교육"},
                {"code": "EDU004", "name": "특수교사", "growth": "중상", "field": "교육"},
                {"code": "EDU005", "name": "교육 프로그램 기획자", "growth": "중", "field": "교육"},
            ],
            "법률/행정": [
                {"code": "LAW001", "name": "변호사", "growth": "중", "field": "법률/행정"},
                {"code": "LAW002", "name": "변리사", "growth": "중상", "field": "법률/행정"},
                {"code": "LAW003", "name": "법무사", "growth": "중", "field": "법률/행정"},
                {"code": "LAW004", "name": "공인중개사", "growth": "중", "field": "법률/행정"},
                {"code": "LAW005", "name": "행정사", "growth": "중", "field": "법률/행정"},
            ],
            "의료/보건": [
                {"code": "MED001", "name": "의사", "growth": "중", "field": "의료/보건"},
                {"code": "MED002", "name": "간호사", "growth": "중상", "field": "의료/보건"},
                {"code": "MED003", "name": "약사", "growth": "중", "field": "의료/보건"},
                {"code": "MED004", "name": "물리치료사", "growth": "중상", "field": "의료/보건"},
                {"code": "MED005", "name": "작업치료사", "growth": "중", "field": "의료/보건"},
                {"code": "MED006", "name": "임상병리사", "growth": "중", "field": "의료/보건"},
            ],
            "미디어/콘텐츠": [
                {"code": "MDA001", "name": "유튜버/크리에이터", "growth": "높음", "field": "미디어/콘텐츠"},
                {"code": "MDA002", "name": "PD", "growth": "중", "field": "미디어/콘텐츠"},
                {"code": "MDA003", "name": "방송작가", "growth": "중", "field": "미디어/콘텐츠"},
                {"code": "MDA004", "name": "카피라이터", "growth": "중", "field": "미디어/콘텐츠"},
                {"code": "MDA005", "name": "콘텐츠 기획자", "growth": "높음", "field": "미디어/콘텐츠"},
            ]
        }
        
        # 필드 필터링
        if field and field in all_jobs:
            jobs = all_jobs[field]
        else:
            jobs = []
            for field_jobs in all_jobs.values():
                jobs.extend(field_jobs)
        
        # 키워드 필터링
        if keyword:
            keyword_lower = keyword.lower()
            jobs = [job for job in jobs if keyword_lower in job['name'].lower()]
        
        return jobs
    
    def _get_sample_major_data(self, major_code: str) -> Dict:
        """샘플 학과 데이터 반환"""
        sample_majors = {
            "CS001": {
                "major_code": "CS001",
                "major_name": "컴퓨터공학",
                "field": "공학",
                "description": "컴퓨터 하드웨어와 소프트웨어의 이론과 응용을 연구하는 학문",
                "core_subjects": [
                    "자료구조", "알고리즘", "운영체제", "데이터베이스",
                    "컴퓨터네트워크", "인공지능", "소프트웨어공학"
                ],
                "related_jobs": [
                    "AI 엔지니어", "소프트웨어 개발자", "데이터 사이언티스트",
                    "시스템 엔지니어", "네트워크 관리자"
                ],
                "recommended_high_school_subjects": ["수학", "정보", "물리학"],
                "admission_info": {
                    "주요대학": ["서울대", "KAIST", "포항공대", "연세대", "고려대"],
                    "평균경쟁률": "15:1",
                    "필수전형요소": "수학(미적분), 영어, 과학탐구"
                }
            }
        }
        
        return sample_majors.get(major_code, {})


class CareerDataManager:
    """진로 데이터 통합 관리 클래스"""
    
    def __init__(self):
        self.worknet = WorkNetAPI()
        self._cache = {}
    
    def get_industry_jobs(self, industry: str) -> List[Dict]:
        """
        특정 신산업 분야의 모든 직업 조회
        
        Args:
            industry: 신산업 분야명
            
        Returns:
            직업 목록
        """
        if industry in self._cache:
            return self._cache[industry]
        
        jobs = self.worknet._get_sample_jobs_by_keyword("", industry)
        self._cache[industry] = jobs
        return jobs
    
    def get_job_details(self, job_code: str) -> Dict:
        """
        직업 상세 정보 조회
        
        Args:
            job_code: 직업 코드
            
        Returns:
            직업 상세 정보
        """
        return self.worknet.get_job_info(job_code)
    
    def search_jobs_by_keyword(self, keyword: str, field: Optional[str] = None) -> List[Dict]:
        """
        키워드로 직업 검색
        
        Args:
            keyword: 검색 키워드
            field: 신산업 분야 (선택)
            
        Returns:
            검색 결과 직업 목록
        """
        return self.worknet.search_jobs(keyword, field)
    
    def get_job_to_major_mapping(self, job_code: str) -> Dict:
        """
        직업과 연관된 학과 정보 조회
        
        Args:
            job_code: 직업 코드
            
        Returns:
            학과 연결 정보
        """
        job_info = self.get_job_details(job_code)
        
        if not job_info:
            return {}
        
        related_majors = job_info.get('related_majors', [])
        high_school_subjects = job_info.get('high_school_subjects', [])
        
        return {
            'job_name': job_info.get('job_name', ''),
            'related_majors': related_majors,
            'high_school_subjects': high_school_subjects,
            'career_path': job_info.get('career_path', ''),
            'required_education': job_info.get('required_education', '')
        }
    
    def compare_jobs(self, job_codes: List[str]) -> pd.DataFrame:
        """
        여러 직업 비교
        
        Args:
            job_codes: 비교할 직업 코드 리스트
            
        Returns:
            비교 데이터프레임
        """
        comparison_data = []
        
        for code in job_codes:
            job = self.get_job_details(code)
            if job:
                comparison_data.append({
                    '직업명': job.get('job_name', ''),
                    '분야': job.get('field', ''),
                    '학력요구': job.get('required_education', ''),
                    '연봉범위': job.get('salary_range', ''),
                    '전망': job.get('outlook', ''),
                    '성장률': job.get('growth_rate', ''),
                    '취업률': job.get('employment_rate', '')
                })
        
        return pd.DataFrame(comparison_data)
    
    def get_career_path_data(self, job_code: str) -> Dict:
        """
        진로 경로 데이터 생성
        
        Args:
            job_code: 직업 코드
            
        Returns:
            진로 경로 시각화용 데이터
        """
        job = self.get_job_details(job_code)
        
        if not job:
            return {}
        
        # 진로 경로를 단계별로 파싱
        path_str = job.get('career_path', '')
        steps = [step.strip() for step in path_str.split('→')]
        
        return {
            'job_name': job.get('job_name', ''),
            'steps': steps,
            'high_school_subjects': job.get('high_school_subjects', []),
            'related_majors': job.get('related_majors', []),
            'required_skills': job.get('required_skills', [])
        }


if __name__ == "__main__":
    # 테스트 코드
    manager = CareerDataManager()
    
    # AI 분야 직업 조회
    print("=== AI/빅데이터 분야 직업 ===")
    jobs = manager.get_industry_jobs("AI/빅데이터")
    for job in jobs[:3]:
        print(f"- {job['name']} ({job['growth']})")
    
    # AI 엔지니어 상세 정보
    print("\n=== AI 엔지니어 상세 정보 ===")
    detail = manager.get_job_details("AI001")
    print(f"직업명: {detail.get('job_name')}")
    print(f"설명: {detail.get('description')}")
    print(f"학력: {detail.get('required_education')}")
    
    # 직업 비교
    print("\n=== 직업 비교 ===")
    comparison = manager.compare_jobs(["AI001", "BIO001", "ECO001"])
    print(comparison)
