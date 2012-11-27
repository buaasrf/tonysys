<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<div class="hero-unit">
    <h3>学生信息管理首页</h3>
    <div class="row-fluid ">
        <div class="btn-group-vertical">
            <button class="btn">新增/修改</button>
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
                <input class="span7" id="gender" name="gender">
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
                <input class="grade" id="grade" name="dept">
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
            <input class="span2" readonly="true"  placeholder="栋">栋
            <input class="span2" readonly="true"  placeholder="房">房
            <input class="span2" readonly="true"  placeholder="间">间
            <input class="span2" readonly="true">宿舍号
        </div>
        <div class="row-fluid">
            宿舍电话：<input class="span3" name="tel" id="tel">
            床位号：<input class="span3" name="bednumber" id="bednumber">
            <button class="btn-info">检查床位是否被占用</button>
        </div>
    </div>
</div>