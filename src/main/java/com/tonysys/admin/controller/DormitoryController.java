package com.tonysys.admin.controller;

import com.alibaba.fastjson.JSON;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.service.DormitoryService;
import com.tonysys.util.FastJsonHelper;
import com.tonysys.util.PageIterator;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:35
 * To change this template use File | Settings | File Templates.
 */
@Controller
@RequestMapping("/dormitory")
public class DormitoryController {
    @Resource
    DormitoryService dormitoryService;
    @RequestMapping(value = "/list")
    @ResponseBody
    public String search(Dormitory dormitory,Integer page,Integer pageSize){
        if(page==null||page<1){
            page=1;
        }
        if(pageSize==null || pageSize<0||pageSize==Integer.MAX_VALUE){
            pageSize=300;
        }
        PageIterator<Dormitory> pageIterator =null;
        pageIterator = dormitoryService.pageSearch(dormitory,page,pageSize,null);
        return JSON.toJSONString(pageIterator, FastJsonHelper.features);
    }
}
