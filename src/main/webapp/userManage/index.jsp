<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<div id="userInsertForm" class="hero-unit">
    <h3>学生信息管理首页</h3>
    <div class="row-fluid ">
        <div class="btn-group">
            <button class="btn" onclick="insertUser();return false;">新增/修改</button>
            <button class="btn" onclick="reset();return false;">清空</button>
        </div>
    </div>
    <hr>
    <h4>学生基本信息:</h4>
    <div id="userInfo" class="row-fluid">
        <input type="hidden" id="userid" name="id">
        <div class="row-fluid">
            <div class="span4">
                <span class="span5">姓名：</span>
                <input id="name" name="name" class="span5"><button class="btn span1">选</button>
            </div>
            <div class="span4">
                <span class="span5">学号：</span>
                <input class="span7" id="number" name="number">
            </div>
            <div class="span4">
                <span class="span5">性别：</span>
                <select class="span7" id="gender" name="gender">
                    <option value="男">男</option>
                    <option value="女">女</option>
                </select>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span4">
                <span class="span5">出生年月：</span>
                <input id="birth" name="birth" class="span7">
            </div>
            <div class="span4">
                <span class="span5">身份证号：</span>
                <input class="span7" id="idNumber" name="idNumber">
            </div>
            <div class="span4">
                <span class="span5">籍贯：</span>
                <input class="span7" id="province" name="province">
            </div>
        </div>
        <div class="row-fluid">
            <div class="span6">
                <span class="span4">所在系：</span>
                <input class="span8" id="dept" name="dept">
            </div>
            <div class="span6">
                <span class="span4">培养层次：</span>
                <input id="trainingLevel" name="trainingLevel" class="span8">
            </div>

        </div>
        <div class="row-fluid">
            <div class="span6">
                <span class="span4">专业：</span>
                <input id="subject" name="subject" class="span8">
            </div>
            <div class="span6">
                <span class="span4">班级：</span>
                <input class="span8" id="grade" name="grade">
            </div>

        </div>
        <div class="row-fluid">
            <div class="span6">
                <span class="span4">家庭电话：</span>
                <input id="homePhone" name="homePhone" class="span8">
            </div>
            <div class="span6">
                <span class="span4">个人电话：</span>
                <input class="span8" id="phone" name="phone">
            </div>

        </div>

    </div>
    <hr>
    <h4>宿舍情况：</h4>
    <div id="dormitoryInfo" class="row-fluid">
        <div class="row-fluid">
            <button class="btn span2" >》选择宿舍</button>
            <input class="span2" readonly="true" name="dormitory.building"  placeholder="栋">栋
            <input class="span2" readonly="true" name="dormitory.room"  placeholder="房">房
            <input class="span2" readonly="true" name="dormitory.door" placeholder="间">间
            <input class="span2" readonly="true" name="dormitory.id">宿舍号
        </div>
        <div class="row-fluid">
            <input type="hidden" id="bedid" name="bed.id">
            宿舍电话：<input class="span3" name="tel" id="dormitory.tel">
            床位号：<input class="span3" name="bednumber" id="bed.number">
            <button class="btn-info">检查床位是否被占用</button>
        </div>
    </div>
</div>
<script type="text/javascript">
    function insertUser(){
        $.ajax({
           url:"/admin/user/insert",
            type:"post",
            dataType:"json",
            data:$("#userInsertForm input").serialize()
        }).done(function(jsonData){
                     if(jsonData["resulte"]==0){
                         alert(jsonData["error"]);
                     }
                    else{
                         alert("添加成功");
                     }
                });
    }
    function reset(){
        $("#userInsertForm input").val("");
    }

</script>