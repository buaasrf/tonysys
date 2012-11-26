<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<div class="hero-unit">
    <h3>学生宿舍管理首页</h3>
    <div class="row-fluid">
        <form class="form-inline row-fluid">
            <input class="input-small span3" placeholder="楼编号" name="building" value="${building}"/>
            <input class="input-small span3" placeholder="房间号" name="room" value="${room}"/>
            <input class="input-small span3" placeholder="寝室门号" name="door" value="${door}"/>
            <button type="submit" class="btn span2">查询</button>
        </form>
        <div class="btn-group" style="padding-left: 20px;">
            <a href="#addDormitory"role="button" class="btn span1" data-toggle="modal">增加</a>
            <a class="btn span1">修改</a>
            <a class="btn span1">删除</a>
        </div>
        <div class="container-fluid">
            <table class="table table-bordered">
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

<!-- Modal -->
<div id="addDormitory" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">添加寝室信息</h3>
    </div>
    <div class="modal-body">
        <div class="row-fluid">
            <span class="span2">楼编号：</span>
            <input class="span3" name="building"/>
            <span class="span2">房间号：</span>
            <input class="span3" name="room"/>
        </div>
        <div class="row-fluid">
            <span class="span2">门编号：</span>
            <input class="span3" name="door"/>
            <span class="span2">床位数：</span>
            <input class="span3" name="bednumber"/>
        </div>
        <div class="row-fluid">
            <span class="span2">寝室电话：</span>
            <input class="span6" name="tel"/>
        </div>
    </div>
    <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>
        <button class="btn btn-primary">保存信息</button>
    </div>
</div>
<script type="text/javascript">
    $(document).ready(function(){
        $.ajax({
            url:"/admin/dormitory/list",
            dataType:"json",
            data:$(".form-inline").serialize(),
            type:"post"
        }).done(function(jsonData){
                    var arrayJson = jsonData["data"];
                    var dormitoryStr="";
                    for(var i=0;i<arrayJson.length;i++){
                        dormitoryStr+="<tr id='"+arrayJson[i]["id"]+"'><td>"+arrayJson[i]["building"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["room"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["door"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["bednumber"]+"</td>";
                        dormitoryStr+="<td>"+arrayJson[i]["tel"]+"</td>";
                        dormitoryStr+="<td> <a class='btn' onclick='deleteDormitory("+arrayJson[i]["id"]+")'> 删除</a> "+arrayJson[i]["tel"]+"</td></tr>";
                    }
                    $("#dormitoryTable").html(dormitoryStr);
                });
    });
</script>