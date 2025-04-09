from flask import Blueprint, render_template, request, redirect, url_for
from core.node_manager import NodeManager

bp = Blueprint('main', __name__)
node_manager = NodeManager()

@bp.route('/')
def dashboard():
    return render_template('dashboard.html', nodes=node_manager.nodes)

@bp.route('/add_node', methods=['POST'])
def add_node():
    cpu_cores = int(request.form.get('cpu_cores', 1))
    node_manager.add_node(cpu_cores)
    return redirect(url_for('main.dashboard'))