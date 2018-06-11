---
title: Flask学习笔记一
date: 2018-06-11 10:12:47
categories: flask
tags: [flask]
---



### 关于flask

- 中文文档： http://docs.jinkan.org/docs/flask/index.html
- 概念： Flask是一个用 python 实现的用来开发 web 应用的微框架
- Flask 同样遵从与`MVC` 的架构理念即：models、views、controls 不过这里我们还是使用templates 即` MVT`



### 环境搭建以及项目的创建

1. #### 搭建环境。

    ```python
    pip install virtualenv
    virtualenv --no-site-packages <虚拟环境文件名>
    ```

    进入Script 文件夹激活虚拟环境。

    

2. #### 创建最小的项目。

   创建一个项目目录，添加虚拟环境， 写一个项目，最简单的 flask web 应用

    ```python
    from flask import Flask  # 导入flask模块
   
    app = Flask(__name__)  # 指定app
   
    @app.route('/')  # 指定路由
    def hello():
        return 'hello, world'
   
    if __name__ == '__main__':
        app.run()  
    ```
   代码解释 ：

   1. 首先，我们导入了 Flask 类。这个类的实例将会是我们的 WSGI 应用程序。
   2. 接下来，我们创建一个该类的实例，第一个参数是应用模块或者包的名称。 如果你使用单一的模块（如本例），你应该使用 `__name__` ，因为模块的名称将会因其作为单独应用启动还是作为模块导入而有不同（ 也即是 `'__main__'` 或实际的导入名）。这是必须的，这样 Flask 才知道到哪去找模板、静态文件等等。详情见 [`Flask`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask)的文档。
   3. 然后，我们使用 [`route()`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask.route) 装饰器告诉 Flask 什么样的URL 能触发我们的函数。
   4. 这个函数的名字也在生成 URL 时被特定的函数采用，这个函数返回我们想要显示在用户浏览器中的信息。
   5. 最后我们用 [`run()`](http://docs.jinkan.org/docs/flask/api.html#flask.Flask.run) 函数来让应用运行在本地服务器上。 其中 `if __name__ =='__main__':` 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候。

   创建好项目之后我们可以使用以下命令来直接运行

   ```python
   python app.py
   ```



3. #### 更改端口号，主机，以及 debug 模式。

   在 run 函数中添加参数即可，原码为 :

   ```python
   def run(self, host=None, port=None, debug=None,
               load_dotenv=True, **options):
   ```

   我们可以给这个函数指定参数，host(主机)、port(端口号)、debug(debug模式)。 例如：

   ```python
   app.run(host='0.0.0.0', port=8080, debug=True)
   ```

   这会让操作系统监听所有公网 IP， 指定端口号为8080，开启debug模式。



4. #### 可以直接返回一个页面。

   ```python
   from flask import Flask, render_template
   
   app = Flask(__name__)
   
   @app.route('/hello')
   def foo():
       return render_template('hello.html')
   
   if __name__ == '__main__':
       app.run()
   ```



### 拓展包

`Flask-Script`

```
pip install flask-script
```



```python
from flask_script import Manager

app = Flask(__name__)
manage = Manager(app=app)

@app.route('/')
def hello_word():
    # 3/0
    return 'GOOD'

if __name__ == '__main__':
    # app.run(port=8000, host='0.0.0.0', debug=False)
    manage.run()
```



可以使用命令来启动程序， 也可以自己配置，配置的时候可以指定端口和debug模式是否开启。



### 代码拆分

- 将一部分代码拆分出去，为了以后项目内容的干净以及协调好处理。

- 方便管理以及修改或者查找代码

  代码目录结构

  ![1](/Flask学习笔记一/1.png)

  1. `requirement` 目录存放着我们项目需要使用的必须的安装包，以后我们可以直接使用

     ```
     pip install -r re_install.txt
     ```

     来安装我们需要使用到的一些安装包

  2. `static` 是我们存放的一些静态目录。

  3. `templates` 是我们的模板文件目录

  4. `user` 相当于django中的app应用

     ![2](/Flask学习笔记一/2.png)

     `models.py` 存放我们关于user的一些model

     `user_views`存放我们关于user的一些views 视图方法

     ```python
     
     from flask import render_template, Blueprint, request, make_response, redirect, url_for
     
     user_blueprint = Blueprint('user', __name__) # 蓝图 用来管理我们的url
     
     
     @user_blueprint.route('/')  # 装饰器用来处理URL
     def hello_word():
         # 3/0
         return 'GOOD'    # 我们可以直接向页面返回一个字符串
     
     
     @user_blueprint.route('/hellohtml/')
     def hello_html():
         return render_template('hello.html')  # 也可以将我们自定义的页面返回注意											   # render_template函数的用法
     
     # 可以指定url参数，string 可以加也可以不加默认有string
     @user_blueprint.route('/helloname/<string:name>/')
     def hello_person(name):
         return render_template('hello.html', name=name)
     @user_blueprint.route('/hellopath/<path:path>/')  # 指定路径的路径格式
     @user_blueprint.route('/helloint/<int:id>/')    # 指定路径的参数为int
     @user_blueprint.route('/hellouuid/<uuid:uuid>')  # 指定路径的参数为uuid，这里的uuid是一个很长唯一的字符串，它指向唯一的一个标识或者页面
     
     # 判断request方式， 然后取值注意route中的第二个参数methods
     @user_blueprint.route('/login/', methods=['GET', 'POST'])
     def login():
         if request.method == 'GET':
             return render_template('hello.html')
         if request.method == 'POST':
             username = request.form.get('username')
             return username
     
     
     @user_blueprint.route('user_res', methods=['GET', 'POST'])
     def get_user_response():
         res = make_response('<h2>大大萌妹</h2>', 200)  # 获取响应， 这里可以res.set_COOKIE()
        
         return res
     
     
     # 重定向
     @user_blueprint.route('redirect')
     def user_redirect():
         # return redirect('/user/login/')   # 重定向到这个url
         return redirect(url_for('user.hello_word'))  # 重定向到指定的方法
     ```

     

     

  5. `utils` 是我们存放的一些工具

     在这个包中我们自定义两个文件 

     - `__init__.py`用来初始化 utils 包 使之可以被其他文件导入

     - `functions.py` 用来放我们自定义的一些方法和函数

       ```python
       import os
       
       from flask import Flask
       
       from user.stu_views import stu_blueprint
       from user.user_views import user_blueprint
       
       
       def create_app():
           # 指定静态目录和模板目录的文件位置
           BASE_DIR = os.path.dirname(os.path.dirname(__file__))
           static_dir = os.path.join(BASE_DIR, 'static')
           templates_dir = os.path.join(BASE_DIR, 'templates')
           # 在初始化对象的时候，可以在参数中添加一些指定
           app = Flask(__name__,
                       static_folder=static_dir,
                       template_folder=templates_dir)
           
           # 管理我们的url 第二个参数的意思是添加Url 前缀
           app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
           app.register_blueprint(blueprint=stu_blueprint, url_prefix='/stu')
       
           return app
       ```

       

  6. `manage.py` 是启动项目的文件

     ```python
     
     from flask_script import Manager
     
     from utils.functions import create_app
     
     app = create_app()  # 替代了 app = Flask(__name__) 来创建app对象
     manage = Manager(app=app)  # Manage类用来管理我们的app
     
     
     if __name__ == '__main__':
         manage.run()
     
     
     ```

     