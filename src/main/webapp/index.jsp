<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>学生宿舍信息管理系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="/resource/css/bootstrap.css" rel="stylesheet">
    <!-- Le styles -->
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }
        .sidebar-nav {
            padding: 9px 0;
        }
    </style>
    <link href="/resource/css/bootstrap-responsive.min.css" rel="stylesheet">
    <link href="/resource/css/docs.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
    <script src="/resource/js/html5.js"></script>
    <![endif]-->
</head>

<body>

<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container-fluid">
            <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </a>
            <a class="brand" href="#">学生宿舍信息管理系统</a>
            <div class="nav-collapse collapse">
                <p class="navbar-text pull-right">
                    当前登录用户：<a href="#" class="navbar-link">用户名</a>
                </p>
                <ul class="nav">
                    <li class="active"><a href="/index.jsp">首页</a></li>
                    <li><a href="/about.jsp">关于</a></li>
                    <li><a href="/contactUs.jsp">联系我们</a></li>
                </ul>
            </div><!--/.nav-collapse -->
        </div>
    </div>
</div>

<div class="container-fluid">
    <div class="row">
        <div class="span3">
            <div class="well sidebar-nav nav-stacked">
                <ul class="nav nav-pills nav-stacked">
                    <li class="nav-header">学生宿舍信息管理</li>
                    <li class="active" name="/userManage/index.jsp"><a href="#">学生信息管理</a></li>
                    <li name="/conductScoreManage/index.jsp"><a href="#">学生操行分管理</a></li>
                    <li name="/dormitoryManage/index.jsp"><a href="#">宿舍信息管理</a></li>
                    <%--<li class="nav-header">权限管理</li>--%>
                    <%--<li><a href="#">权限管理</a></li>--%>
                    <%--<li><a href="#">权限分配</a></li>--%>
                </ul>
            </div><!--/.well -->
        </div><!--/span-->
        <div id="mainContener" class="span9">
            <div class="hero-unit">
                <h1>学生宿舍管理系统</h1>
                <p>学生宿舍管理系统简介…………</p>
                <p>1：本系统使用j2ee 轻量级 mvc架构搭建</p>
                <p>2：前端页面和后台程序完全使用ajax的方式进行异步交互的，数据的传输的格式是使用json标准格式</p>
                <p>3：项目使用maven做为构建，脱离了平台了的依赖性，实现了在任意平台随意部署灵活性</p>
                <p>4：系统在开发过程使用了Git作为代码的版本管理控制工具，有效且灵活的控制各个版本的代码，可以多人同时协作开发</p>
                <p>5：后台数据库是使用优秀的开源数据库mysql，轻量，跨平台，易于管理和使用</p>
                <p><a class="btn btn-primary btn-large">了解更多 &raquo;</a></p>
            </div>
            <div class="row-fluid">
                <div class="span4">
                    <h2>j2ee mvc</h2>
                    <p>j2ee mvc 简介…… </p>
                    <p><a class="btn" href="#">查看详细 &raquo;</a></p>
                </div><!--/span-->
                <div class="span4">
                    <h2>ajax</h2>
                    <p>ajax 简介……</p>
                    <p><a class="btn" href="#">查看详细 &raquo;</a></p>
                </div><!--/span-->
                <div class="span4">
                    <h2>maven</h2>
                    <p>maven简介……</p>
                    <p><a class="btn" href="#">查看详细 &raquo;</a></p>
                </div><!--/span-->
            </div><!--/row-->

        </div><!--/span-->
    </div><!--/row-->
    <footer class="navbar  navbar-fixed-bottom brand navbar-inner">
        <p>&copy; ruifeng.sun 2012</p>
    </footer>

</div><!--/.fluid-container-->

<!-- Le javascript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="resource/js/jquery-1.8.2.min.js"></script>
<script src="resource/js/bootstrap.js"></script>
<script type="text/javascript">
    $(function(){
        $(".sidebar-nav li:has(a)").click(function(){
            $(".sidebar-nav li:has(a)").removeClass();
            $(this).addClass("active");
            $.ajax({
                url:$(this).attr("name"),
                contentType:"text/html",
                success:function(data){
                    $("#mainContener").html(data);
                },
                error:function(data){
                    $("#mainContener").html(data);
                }
            });
        });
    });

</script>
</body>
</html>
