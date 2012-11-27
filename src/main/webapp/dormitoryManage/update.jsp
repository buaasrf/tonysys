<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!-- Modal -->
<div id="addDormitory" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">修改寝室信息</h3>
    </div>
    <div class="modal-body">
        <div class="row-fluid">
            <div class="span6">
                <input type="hidden" name="id" value="${dormitory.id}">
                <span class="span6">楼编号：</span>
                <input class="span6" name="building" value="${dormitory.building}"/>
            </div>
            <div class="span6">
                <span class="span6">房间号：</span>
                <input class="span6" name="room" value="${dormitory.room}"/>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span6">
                <span class="span6">门编号：</span>
                <input class="span6" name="door" value="${dormitory.door}"/>
            </div>
            <div class="span6">
                <span class="span6">床位数：</span>
                <input class="span6" name="bednumber" value="${dormitory.bednumber}"/>
            </div>
        </div>
        <div class="row-fluid">
            <span class="span2">寝室电话：</span>
            <input class="span6" name="tel"  value="${dormitory.tel}"/>
        </div>
    </div>
    <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">关闭</button>
        <button class="btn btn-primary" onclick="updateDormitory();return false;">保存信息</button>
    </div>
</div>