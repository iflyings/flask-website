import json
from flask import render_template, request, session, redirect
from .. import repository
from . import bapp

@bapp.route('/index', methods=['GET', 'POST'])
@bapp.route('/', methods=['GET', 'POST'])
def index():
    if 'ID' in session:
        print(session['ID'])
        return render_template('index.html')
    else:
        return redirect('/login')

@bapp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@bapp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@bapp.route('/image', methods=['GET', 'POST'])
def image_home():
    return image_page(1)

@bapp.route('/image/<int:page_id>/', methods=['GET', 'POST'])
def image_page(page_id):
    page_data = {
        'title': repository.get_image_name(str(page_id)),
        'id': page_id,
        'tree_data': repository.get_image_info(),
        'list_data': repository.get_image_list(str(page_id))
    }
    return render_template('image_page.html', **page_data)

@bapp.route('/cartoon', methods=['GET', 'POST'])
def cartoon_home():
    return cartoon_page(1, 1)

@bapp.route('/cartoon/<int:page_id>/<int:page_index>/', methods=['GET', 'POST'])
def cartoon_page(page_id, page_index):
    page_data = {
        'title': repository.get_cartoon_name(page_id),
        'id': page_id,
        'index': page_index,
        'total': int((repository.get_cartoon_count(page_id) - 1) / 10 + 1),
        'tree_data': repository.get_cartoon_info(),
        'list_data': repository.get_cartoon_list(page_id, (page_index - 1) * 10, 10)
    }
    return render_template('cartoon_page.html', **page_data)

@bapp.route('/download', methods=['GET', 'POST'])
def download_home():
    return render_template('download_page.html',)
"""
    restful 接口
"""
@bapp.route('/user_login', methods=['POST'])
def user_login():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    rep = dict()
    rep['status'] = 0
    rep['action'] = "login"
    rep['info'] = "success"
    session['ID'] = "123456789"
    return json.dumps(rep)

@bapp.route('/user_logout', methods=['GET', 'POST'])
def user_logout():
    if 'ID' in session:
        session.pop('username', None)
    rep = {
        'status': 0,
        'action': "logout",
        'info': "success"
    }
    return json.dumps(rep)

@bapp.route('/user_register', methods=['POST'])
def user_register():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    session['ID'] = "123456789"
    rep = dict()
    rep['status'] = 0
    rep['action'] = "register"
    rep['info'] = "success"
    rep['url'] = "/home"
    return json.dumps(rep)

@bapp.route('/image_list.json', methods=['POST'])
def image_folder_info():
    data = request.get_data()
    json_data = json.loads(bytes.decode(data))
    image_list = get_image_list(json_data["path"])
    return json.dumps(image_list)

@bapp.route('/cartoon_list.json', methods=['POST'])
def cartoon_folder_info():
    data = request.get_data()
    json_data = json.loads(bytes.decode(data))
    image_list = get_image_list(json_data["path"])
    return json.dumps(image_list)
