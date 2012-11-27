<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
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