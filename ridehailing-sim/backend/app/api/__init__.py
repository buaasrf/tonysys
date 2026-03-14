"""
API 蓝图注册
对应 MiroFish 的 api/__init__.py
"""

from flask import Blueprint

simulation_bp = Blueprint('simulation', __name__)
report_bp = Blueprint('report', __name__)

from . import simulation, report  # noqa: E402, F401
