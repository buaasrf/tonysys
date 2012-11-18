<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>登录 &middot;</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="resource/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 40px;
            padding-bottom: 40px;
            background-color: #f5f5f5;
        }

        .form-signin {
            max-width: 300px;
            padding: 19px 29px 29px;
            margin: 0 auto 20px;
            background-color: #fff;
            border: 1px solid #e5e5e5;
            -webkit-border-radius: 5px;
            -moz-border-radius: 5px;
            border-radius: 5px;
            -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.05);
            -moz-box-shadow: 0 1px 2px rgba(0,0,0,.05);
            box-shadow: 0 1px 2px rgba(0,0,0,.05);
        }
        .form-signin .form-signin-heading,
        .form-signin .checkbox {
            margin-bottom: 10px;
        }
        .form-signin input[type="text"],
        .form-signin input[type="password"] {
            font-size: 16px;
            height: auto;
            margin-bottom: 15px;
            padding: 7px 9px;
        }

    </style>
    <link href="resource/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
    <script src="resource/js/html5.js"></script>
    <![endif]-->

</head>

<body>

<div class="container">

    <form class="form-signin">
        <h2 class="form-signin-heading">学生宿舍管理系统</h2>
        <input type="text" id="userName"  class="input-block-level" placeholder="用户名">
        <input type="password" id="password"  class="input-block-level" placeholder="密码">
        <label class="checkbox">
            <input type="checkbox" value="remember-me"> 记住我
        </label>
        <button class="btn btn-large btn-primary" type="button" onclick="login()">登录</button>
    </form>

</div> <!-- /container -->

<!-- Le javascript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="resource/js/jquery-1.8.2.min.js"></script>
<script src="resource/js/bootstrap.min.js"></script>
 <script type="text/javascript">
     function login(){
         $.ajax({
             url:"/admin/login/"+$("#userName").val()+"/"+$("#password").val(),
             success:function(data){
                 if(data["responseText"]["flag"]==0){
                    alert(data["responseText"]["error"]);
                 }
                 if(data["flag"]==1){
                     top.window.location.href=data["responseText"]["redirect"];
                 }
             },
             error:function(data){
                 if(data["responseText"]["flag"]==0){
                     alert(data["responseText"]["error"]);
                 }
                 if(data["responseText"]["flag"]==1){
                     top.window.location.href=data["responseText"]["redirect"];
                 }
             }
         });
     }
 </script>
</body>
</html>