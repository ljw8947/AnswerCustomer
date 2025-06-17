from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.category import Category

bp = Blueprint('engineer', __name__, url_prefix='/engineer')

# Helper function to check if current user is an engineer or admin
def engineer_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (current_user.role != 'engineer' and current_user.role != 'admin'):
            flash('您没有权限访问此页面。', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@engineer_required
def dashboard():
    return render_template('engineer/dashboard.html', title='工程师仪表盘')

@bp.route('/issues')
@engineer_required
def issues():
    issue_manager = current_app.issue_manager
    category_manager = current_app.category_manager
    all_issues = issue_manager.read_all()
    
    # 获取所有Category数据用于下拉列表
    all_categories = category_manager.read_all()
    
    # 获取唯一的Function Domain和Specific Function选项
    function_domains = sorted(list(set([cat.function_domain for cat in all_categories if cat.function_domain])))
    specific_functions = sorted(list(set([cat.specific_function for cat in all_categories if cat.specific_function])))
    
    # 应用筛选条件
    filtered_issues = all_issues
    
    # 状态筛选
    status_filter = request.args.get('status')
    if status_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.status == status_filter]
    
    # 车型筛选
    carline_filter = request.args.get('carline')
    if carline_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.carline == carline_filter]
    
    # 功能域筛选
    function_domain_filter = request.args.get('function_domain')
    if function_domain_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.function_domain == function_domain_filter]
    
    # 具体功能筛选
    specific_function_filter = request.args.get('specific_function')
    if specific_function_filter:
        filtered_issues = [issue for issue in filtered_issues if issue.specific_function == specific_function_filter]
    
    # 数据倒序显示（按创建时间倒序）
    filtered_issues.sort(key=lambda x: x.create_time or '', reverse=True)
    
    # 分页处理 - 固定每页20条记录
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 固定每页显示20条记录
    
    total_issues = len(filtered_issues)
    total_pages = (total_issues + per_page - 1) // per_page
    
    # 确保page在有效范围内
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # 计算分页切片
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_issues = filtered_issues[start_idx:end_idx]

    return render_template('engineer/issues.html', 
                         title='问题列表', 
                         issues=paginated_issues,
                         function_domains=function_domains,
                         specific_functions=specific_functions,
                         page=page,
                         per_page=per_page,
                         total_pages=total_pages,
                         total_issues=total_issues)

@bp.route('/issues/<issue_id>')
@engineer_required
def issue_detail_engineer(issue_id):
    issue_manager = current_app.issue_manager
    comment_manager = current_app.comment_manager
    
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('engineer.issues'))

    # 获取该问题的所有评论
    all_comments = comment_manager.read_all()
    comments = [comment for comment in all_comments if comment.issue_id == issue_id]
    # 按创建时间排序，最新的在前
    comments.sort(key=lambda x: x.created_at, reverse=True)

    return render_template('engineer/issue_detail.html', title='问题详情', issue=issue, comments=comments)

@bp.route('/issues/<issue_id>/comment', methods=['POST'])
@engineer_required
def add_comment(issue_id):
    issue_manager = current_app.issue_manager
    comment_manager = current_app.comment_manager
    
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')
    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('engineer.issues'))

    content = request.form.get('content', '').strip()
    if not content:
        flash('评论内容不能为空。', 'danger')
        return redirect(url_for('engineer.issue_detail_engineer', issue_id=issue_id))

    # 创建新评论
    new_comment = Comment(
        issue_id=issue_id,
        user_id=current_user.get_id(),
        username=current_user.username,
        content=content
    )
    
    comment_manager.add_item(new_comment)
    flash('评论已添加！', 'success')
    return redirect(url_for('engineer.issue_detail_engineer', issue_id=issue_id))

@bp.route('/issues/<issue_id>/process', methods=['GET', 'POST'])
@engineer_required
def process_issue(issue_id):
    issue_manager = current_app.issue_manager
    comment_manager = current_app.comment_manager
    issue = issue_manager.get_item_by_id(issue_id, 'issue_id')

    if not issue:
        flash('问题未找到。', 'danger')
        return redirect(url_for('engineer.issues'))

    if request.method == 'POST':
        old_status = issue.status
        old_assigned_to = issue.assigned_to_user_id
        old_extra_info = issue.extra_info
        
        new_status = request.form.get('status')
        extra_info = request.form.get('extra_info')
        assign_to_me = request.form.get('assign_to_me')

        # 记录变化
        changes = []
        
        if new_status and new_status != old_status:
            issue.status = new_status
            changes.append(f"状态: {old_status} → {new_status}")
        
        if assign_to_me == 'on' and old_assigned_to != current_user.get_id():
            issue.assigned_to_user_id = current_user.get_id()
            issue.status = 'Assigned'  # Automatically set to Assigned if assigned
            changes.append(f"操作人: 指派给 {current_user.username}")
            if new_status != 'Assigned':
                changes.append(f"状态: {old_status} → Assigned")
        elif assign_to_me != 'on' and old_assigned_to == current_user.get_id():
            issue.assigned_to_user_id = None
            changes.append(f"操作人: 取消指派")
        
        if extra_info != old_extra_info:
            issue.extra_info = extra_info
            if extra_info:
                changes.append(f"额外信息: {extra_info}")
            else:
                changes.append("额外信息: 已清空")

        # 更新问题
        issue_manager.update_item(issue.issue_id, issue, 'issue_id')
        
        # 如果有变化，添加状态变化记录到评论
        if changes:
            status_change_content = f"【状态更新】\n操作人: {current_user.username}\n"
            status_change_content += "\n".join(changes)
            
            # 创建状态变化评论
            status_comment = Comment(
                issue_id=issue_id,
                user_id=current_user.get_id(),
                username=current_user.username,
                content=status_change_content
            )
            
            comment_manager.add_item(status_comment)
            flash('问题处理信息已更新，状态变化已记录！', 'success')
        else:
            flash('问题处理信息已更新！', 'success')
            
        return redirect(url_for('engineer.issue_detail_engineer', issue_id=issue.issue_id))

    return render_template('engineer/issue_process.html', title='处理问题', issue=issue) 