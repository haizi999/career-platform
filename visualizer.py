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
        
        for i, job_name in enumerate(job_names):
            fig.add_trace(go.Scatter(
                x=[min_salaries[i], max_salaries[i]],
                y=[job_name, job_name],
                mode='lines',
                line=dict(color='lightblue', width=10),
                showlegend=False,
                hoverinfo='skip'
            ))
        
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
        
        for i, step in enumerate(steps):
            G.add_node(i, label=step, level=i)
        
        for i in range(len(steps) - 1):
            G.add_edge(i, i + 1)
        
        pos = {}
        for i, step in enumerate(steps):
            pos[i] = (i, 0)
        
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
        
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(G.nodes[node]['label'])
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
