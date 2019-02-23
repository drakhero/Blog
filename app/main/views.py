#处理与博客相关的路由和视图
import os

from . import main
from flask import render_template, session, request, redirect
from ..models import *
from .. import db

@main.route('/')
def main_index():
    #查询Category中的所有分类信息
    categories = Category.query.all()
    #查询Topic中的前五条数据
    topics = Topic.query.all()
    #判断session中是否有id和loginname的值
    if 'id' in session and 'loginname' in session:
        #已经登录过，从数据库中获取登录信息
        id = session['id']
        user = User.query.filter_by(id=id).first()

    return render_template('index.html',params=locals())

@main.route('/release',methods=['GET','POST'])
def release_views():
    if request.method == 'GET':
        #权限验证，判断是否有用户登录以及登录者的身份是否为作者，如果没有权限的话则从哪来回哪去
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(id=id).first()
            if user.is_author:
                #查询Category的信息
                categories = Category.query.all()
                return render_template('release.html',params=locals())
        url = request.headers.get('Referer','/')
        return redirect(url)
    else:
        #post请求处理发表博客的相关操作
        #1.创建Topic对象 - topic
        topic = Topic()
        #2.接收前端传递过来的值并赋值给topic
        topic.title = request.form['author']
        topic.blogtype_id = request.form['list']
        topic.category_id = request.form['category']
        topic.user_id = session['id']
        topic.content = request.form['content']
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #判断是否有文件上传，如果有的话则将文件保存至static/upload,并将文件路径名赋值给topic.images
        if request.files:
            #获取上传文件
            f = request.files['image']
            #处理文件名：时间.扩展名
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename = ftime + '.' + ext
            #处理上传路径:upload/xxx.xx
            #将文件路径赋值给topic.images:upload/xxx.xx
            topic.images = "upload/"+filename
            #将文件保存到指定目录下
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir,'static/upload',filename)
            f.save(upload_path)
            pass
        db.session.add(topic)
        db.session.commit()
        return redirect('/')


