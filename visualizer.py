"""
진로 데이터 시각화 모듈
직업 정보, 진로 경로, 비교 분석 등을 시각화
"""

import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
from typing import List, Dict
import numpy as np


class CareerVisualizer:
    """진로 데이터 시각화 클래스"""
    
    def __init__(self):
        self.colors = {
            "AI/빅데이터": "#1f77b4",
            "바이오헬스": "#2ca02c",
            "친환경에너지": "#90EE90",
            "메타버스/XR": "#9467bd",
            "자율주행/모빌리티": "#8c564b",
            "로봇공학": "#e377c2",
            "우주항공": "#17becf",
            "스마트시티": "#bcbd22"
        }
    
    def create_industry_overview(self, industries_data: Dict) -> go.Figure:
        """
        신산업 분야 개요 차트 생성
        
        Args:
            industries_data: 산업별 데이터 딕셔너리
            
        Returns:
            Plotly Figure 객체
        """
        industries = list(industries_data.keys())
        job_counts = [data['jobs_count'] for data in industries_data.values()]
        
        fig = go.Figure(data=[
            go.Bar(
                x=industries,
                y=job_counts,
                marker=dict(
                    color=[self.colors.get(ind, '#gray') for ind in industries],
                    line=dict(color='white', width=2)
                ),
                text=job_counts,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>관련 직업: %{y}개<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '신산업 분야별 등록 직업 수',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#2c3e50'}
            },
            xaxis_title='신산업 분야',
            yaxis_title='직업 수',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False,
            font=dict(size=12),
            hovermode='x'
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')
        
        return fig
    
    def create_growth_comparison(self, jobs_data: List[Dict]) -> go.Figure:
        """
        직업별 성장 전망 비교 차트
        
        Args:
            jobs_data: 직업 데이터 리스트
            
        Returns:
            Plotly Figure 객체
        """
        growth_mapping = {
            "매우 높음": 5,
            "높음": 4,
            "중상": 3,
            "중": 2,
            "낮음": 1
        }
        
        job_names = [job['name'] for job in jobs_data]
        growth_values = [growth_mapping.get(job['growth'], 0) for job in jobs_data]
        growth_labels = [job['growth'] for job in jobs_data]
        
        fig = go.Figure(data=[
            go.Scatter(
                x=job_names,
                y=growth_values,
                mode='markers+lines',
                marker=dict(
                    size=15,
                    color=growth_values,
                    colorscale='RdYlGn',
                    showscale=False,
                    line=dict(width=2, color='white')
                ),
                line=dict(color='#1f77b4', width=2),
                text=growth_labels,
                hovertemplate='<b>%{x}</b><br>성장 전망: %{text}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '직업별 성장 전망',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis_title='직업',
            yaxis_title='성장 전망 지수',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['낮음', '중', '중상', '높음', '매우 높음']
            )
        )
        
        return fig
    
    def create_job_comparison_radar(self, comparison_df: pd.DataFrame) -> go.Figure:
        """
        직업 비교 레이더 차트
        
        Args:
            comparison_df: 비교 데이터프레임
            
        Returns:
            Plotly Figure 객체
        """
        # 점수 매핑
        outlook_scores = {"매우 높음": 5, "높음": 4, "중상": 3, "중": 2, "낮음": 1}
        
        categories = ['전망', '성장률', '취업률', '연봉', '학력요구']
        
        fig = go.Figure()
        
        for idx, row in comparison_df.iterrows():
            # 각 항목을 점수화
            outlook = outlook_scores.get(row.get('전망', '중'), 3)
            growth = float(row.get('성장률', '10%').rstrip('%')) / 5  # 정규화
            employment = float(row.get('취업률', '50%').rstrip('%')) / 20  # 정규화
            
            # 연봉 중간값 추출
            salary_str = row.get('연봉범위', '3,000만원 ~ 5,000만원')
            try:
                salaries = [int(s.replace('만원', '').replace(',', '').strip()) 
                           for s in salary_str.split('~')]
                salary_score = (sum(salaries) / len(salaries)) / 1500  # 정규화
            except:
                salary_score = 3
            
            # 학력 요구도 (높을수록 점수 낮음)
            education = 5 if '고졸' in row.get('학력요구', '') else \
                       4 if '학사' in row.get('학력요구', '') else 3
            
            values = [outlook, growth, employment, salary_score, education]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=row['직업명']
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=True,
            title={
                'text': '직업 비교 분석',
                'x': 0.5,
                'xanchor': 'center'
            },
            height=500
        )
        
        return fig
    
    def create_career_path_network(self, path_data: Dict) -> go.Figure:
        """
        진로 경로 네트워크 그래프
        
        Args:
            path_data: 진로 경로 데이터
            
        Returns:
            Plotly Figure 객체
        """
        G = nx.DiGraph()
        
        steps = path_data.get('steps', [])
        
        # 노드 추가
        for i, step in enumerate(steps):
            G.add_node(i, label=step, level=i)
        
        # 엣지 추가
        for i in range(len(steps) - 1):
            G.add_edge(i, i + 1)
        
        # 위치 계산 (계층적 레이아웃)
        pos = {}
        for i, step in enumerate(steps):
            pos[i] = (i, 0)
        
        # 엣지 좌표
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=3, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        
        # 노드 좌표
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(G.nodes[node]['label'])
            # 시작은 초록, 끝은 빨강, 중간은 파랑
            if node == 0:
                node_colors.append('#2ecc71')
            elif node == len(steps) - 1:
                node_colors.append('#e74c3c')
            else:
                node_colors.append('#3498db')
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=30,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # 화살표 추가
        annotations = []
        for i in range(len(steps) - 1):
            x0, y0 = pos[i]
            x1, y1 = pos[i + 1]
            annotations.append(
                dict(
                    x=x1, y=y1,
                    ax=x0, ay=y0,
                    xref='x', yref='y',
                    axref='x', ayref='y',
                    showarrow=True,
                    arrowhead=3,
                    arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor='#888'
                )
            )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        
        fig.update_layout(
            title={
                'text': f"{path_data.get('job_name', '직업')} 진로 경로",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            showlegend=False,
            hovermode='closest',
            height=300,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=annotations,
            margin=dict(t=80, b=20, l=20, r=20)
        )
        
        return fig
    
    def create_salary_distribution(self, jobs_data: List[Dict]) -> go.Figure:
        """
        직업별 연봉 분포 차트
        
        Args:
            jobs_data: 직업 상세 정보 리스트
            
        Returns:
            Plotly Figure 객체
        """
        job_names = []
        min_salaries = []
        max_salaries = []
        avg_salaries = []
        
        for job in jobs_data:
            salary_range = job.get('salary_range', '3,000만원 ~ 5,000만원')
            try:
                parts = salary_range.split('~')
                min_sal = int(parts[0].replace('만원', '').replace(',', '').strip())
                max_sal = int(parts[1].replace('만원', '').replace(',', '').strip())
                
                job_names.append(job.get('job_name', ''))
                min_salaries.append(min_sal)
                max_salaries.append(max_sal)
                avg_salaries.append((min_sal + max_sal) / 2)
            except:
                continue
        
        fig = go.Figure()
        
        # 범위 표시
        for i, job_name in enumerate(job_names):
            fig.add_trace(go.Scatter(
                x=[min_salaries[i], max_salaries[i]],
                y=[job_name, job_name],
                mode='lines',
                line=dict(color='lightblue', width=10),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # 평균 표시
        fig.add_trace(go.Scatter(
            x=avg_salaries,
            y=job_names,
            mode='markers',
            marker=dict(
                size=12,
                color='#1f77b4',
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            name='평균 연봉',
            hovertemplate='<b>%{y}</b><br>평균 연봉: %{x:,.0f}만원<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': '직업별 연봉 분포',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis_title='연봉 (만원)',
            yaxis_title='',
            height=max(400, len(job_names) * 50),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='closest'
        )
        
        fig.update_xaxis(showgrid=True, gridcolor='lightgray')
        
        return fig
    
    def create_skill_requirement_chart(self, job_data: Dict) -> go.Figure:
        """
        직업별 필요 역량 차트
        
        Args:
            job_data: 직업 상세 정보
            
        Returns:
            Plotly Figure 객체
        """
        skills = job_data.get('required_skills', [])
        
        # 스킬을 카테고리로 분류
        skill_categories = {
            '프로그래밍': 0,
            '데이터분석': 0,
            '이론/학문': 0,
            '도구/툴': 0,
            '소프트스킬': 0
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(lang in skill_lower for lang in ['python', 'java', 'c++', '프로그래밍']):
                skill_categories['프로그래밍'] += 1
            elif any(term in skill_lower for term in ['데이터', 'data', '분석', 'analysis']):
                skill_categories['데이터분석'] += 1
            elif any(term in skill_lower for term in ['이론', '수학', '통계', '물리', '화학']):
                skill_categories['이론/학문'] += 1
            elif any(term in skill_lower for term in ['cad', 'tool', '툴', 'tensorflow', 'pytorch']):
                skill_categories['도구/툴'] += 1
            else:
                skill_categories['소프트스킬'] += 1
        
        categories = list(skill_categories.keys())
        values = list(skill_categories.values())
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker=dict(color='#1f77b4'),
                line=dict(color='#1f77b4', width=2)
            )
        ])
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) + 1] if max(values) > 0 else [0, 5]
                )
            ),
            showlegend=False,
            title={
                'text': f"{job_data.get('job_name', '직업')} 필요 역량",
                'x': 0.5,
                'xanchor': 'center'
            },
            height=400
        )
        
        return fig


if __name__ == "__main__":
    # 테스트 코드
    visualizer = CareerVisualizer()
    
    # 산업 개요 차트 테스트
    industries_data = {
        "AI/빅데이터": {"jobs_count": 85},
        "바이오헬스": {"jobs_count": 72},
        "친환경에너지": {"jobs_count": 64}
    }
    
    fig = visualizer.create_industry_overview(industries_data)
    print("산업 개요 차트 생성 완료")
