<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>关于我们</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="resource/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }
        .sidebar-nav {
            padding: 9px 0;
        }
    </style>
    <link href="resource/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
    <script src="resource/js/html5.js"></script>
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
                    <li><a href="/index.jsp">首页</a></li>
                    <li class="active"><a href="/about.jsp">关于</a></li>
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
                    <li class="nav-header">权限管理</li>
                    <li><a href="#">权限管理</a></li>
                    <li><a href="#">权限分配</a></li>
                </ul>
            </div><!--/.well -->
        </div><!--/span-->
        <div id="mainContener" class="span9">
            <div class="hero-unit">
                <h2>关于我们</h2>
                <p>我们的详细信息……</p>
                <p>我们的详细信息……</p>
                <p>我们的详细信息……</p>
            </div>
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
<script src="resource/js/bootstrap.min.js"></script>
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

