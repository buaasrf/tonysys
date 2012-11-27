<%@ taglib prefix="c" uri="http://java.sun.com/jstl/core_rt" %>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page import="com.tonysys.context.UserState" %>
<!-- Modal -->
<div id="addDormitory" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">寝室学生信息</h3>
    </div>
    <div class="modal-body">
        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <td>姓名</td>
                <td>类型</td>
                <td>学号</td>
                <td>院系</td>
                <td>专业</td>
                <td>班级</td>
                <td>性别</td>
                <td>状态</td>
                <td>民族</td>
                <td>电话</td>

            </tr>
            </thead>
            <tbody >
                <c:forEach var="user" items="${userList}">
                    <tr  class="${user.userState.color}">
                        <td>${user.name}</td>
                        <td>${user.userType.value}</td>
                        <td>${user.number}</td>
                        <td>${user.dept}</td>
                        <td>${user.subject}</td>
                        <td>${user.grade}</td>
                        <td>${user.gender}</td>
                        <td>${user.userState.value}</td>
                        <td>${user.nation}</td>
                        <td>${user.phone}</td>
                    </tr>
                </c:forEach>
            </tbody>
        </table>
    </div>
    <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>
    </div>
</div>