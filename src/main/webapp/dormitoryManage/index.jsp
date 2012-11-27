<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<div class="row-fluid" style="padding: 10px;">
    <h3>学生宿舍管理首页</h3>
    <p class="alert-error">说明：寝室数据项背景为红色表示该宿舍存在违纪的学生，背景为黄色表示该宿舍有留级的学生，背景为蓝色表示该宿舍有其他情况的学生，背景为绿色表示该宿舍学生都为良好</p>
    </div>
<div class="row-fluid">
    <div class="row-fluid">
        <form class="form-inline row-fluid">
            <input class="input-small span3" placeholder="楼编号" name="building" value="${building}"/>
            <input class="input-small span3" placeholder="房间号" name="room" value="${room}"/>
            <input class="input-small span3" placeholder="寝室门号" name="door" value="${door}"/>
            <button type="submit" class="btn span2" onclick="fillTable();return false;">查询</button>
        </form>
        <div class="btn-group row-fluid">
            <a href="#addDormitory"role="button" class="btn span1" data-toggle="modal" onclick="preInsertDormitory()">增加</a>
            <a class="btn span1">修改</a>
            <a class="btn span1">删除</a>
        </div>
        <div class="bs-docs-container">
            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                    <td>楼编号</td>
                    <td>房间编号</td>
                    <td>寝室门号</td>
                    <td>床位数</td>
                    <td>电话</td>
                    <td>操作</td>
                    </tr>
                </thead>
                <tbody id="dormitoryTable" >

                </tbody>
            </table>
        </div>
    </div>
</div>
<form id="dormitoryModal">
    <!-- Modal -->
    <div id="addDormitory" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="myModalLabel">添加寝室信息</h3>
        </div>
        <div class="modal-body">
            <div class="row-fluid">
                <div class="span6">
                    <span class="span6">楼编号：</span>
                    <input class="span6" name="building"/>
                </div>
                <div class="span6">
                    <span class="span6">房间号：</span>
                    <input class="span6" name="room"/>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span6">
                    <span class="span6">门编号：</span>
                    <input class="span6" name="door"/>
                </div>
                <div class="span6">
                    <span class="span6">床位数：</span>
                    <input class="span6" name="bednumber"/>
                </div>
            </div>
            <div class="row-fluid">
                <span class="span2">寝室电话：</span>
                <input class="span6" name="tel"/>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>
            <button class="btn btn-primary" onclick="insertDormitory();return false;">保存信息</button>
        </div>
    </div>
</form>
<script type="text/javascript">
    $(document).ready(function(){
        fillTable();
    });
    function fillTable(){
        $.ajax({
            url:"/admin/dormitory/list",
            dataType:"json",
            data:$(".form-inline").serialize(),
            type:"post"
        }).done(function(jsonData){
                    var arrayJson = jsonData["data"];
                    var dormitoryStr="";
                    for(var i=0;i<arrayJson.length;i++){
                        dormitoryStr+="<tr class=\""+arrayJson[i]["state"]+"\" id=\""+arrayJson[i]["id"]+"\"><td>"+arrayJson[i]["building"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["room"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["door"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["bednumber"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["tel"]+"</td>";
                        dormitoryStr+="<td> <a class='btn' onclick='deleteDormitory("+arrayJson[i]["id"]+")'> 删除</a><a class='btn' onclick='preUpdateDormitory("+arrayJson[i]["id"]+")'> 修改</a> <a class='btn' onclick='viewUsers("+arrayJson[i]["id"]+")'> 查看学生信息</a></td></tr>";
                    }
                    $("#dormitoryTable").html(dormitoryStr);
                });
    }
    function deleteDormitory(id){
        if(window.confirm("确定删除吗？")){
            $.ajax({
               url:"/admin/dormitory/delete/"+id,
               type:"post",
               dataType:"json"
            }).done(function(jsonData){
                        if(jsonData["result"]==0){
                            alert(jsonData["error"]);
                        }
                        else{
                            fillTable();
                        }
                    });
        }
    }
    function viewUsers(id){
        $.ajax({
            url:"/admin/dormitory/viewstu/"+id,
            dataType:"html",
            type:"get"
        }).done(function(htmlData){
                    $("#dormitoryModal").html(htmlData);
                    $("#addDormitory").modal("show");
                });
    }
    function preInsertDormitory(){
        $("#dormitoryModal input").val("");
    }
    function insertDormitory(){
        $.ajax({
            url:"/admin/dormitory/insert",
            type:"post",
            dataType:"json",
            data:$("#dormitoryModal").serialize()
        }).done(function(jsonData){
                    if(jsonData["result"]==0){
                        alert(jsonData["error"]);
                    }
                    else{
                        alert("保存成功");
                        fillTable();
                        $("#addDormitory").modal("hide");
                    }
                });
    }
    function preUpdateDormitory(id){
        $.ajax({
            url:"/admin/dormitory/get/"+id,
            type:"get",
            dataType:"html"
        }).done(function(htmlData){
                    $("#dormitoryModal").html(htmlData);
                    $("#addDormitory").modal("show");
                });
    }
    function updateDormitory(){
        $.ajax({
            url:"/admin/dormitory/update",
            type:"post",
            dataType:"json",
            data:$("#dormitoryModal input").serialize()
        }).done(function(jsonData){
                    if(jsonData["result"]==0){
                        alert(jsonData["error"]);
                    }
                    else{
                        alert("更新成功");
                        $("#addDormitory").modal("hide");
                        fillTable();
                    }
                });
    }
</script>