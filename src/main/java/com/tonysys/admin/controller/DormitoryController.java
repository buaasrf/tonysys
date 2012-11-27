package com.tonysys.admin.controller;

import com.alibaba.fastjson.JSON;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.ResultMSG;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.service.DormitoryService;
import com.tonysys.util.FastJsonHelper;
import com.tonysys.util.PageIterator;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import javax.annotation.Resource;
import java.util.List;

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
    @RequestMapping(value = "/delete/{id}")
    @ResponseBody
    public String delete(@PathVariable Integer id){
        ResultMSG resultMSG = new ResultMSG();
        if(id==null||id<1){
            resultMSG.setError("要删除的寝室id为空");
        }else{
            try{
                resultMSG.setResult(dormitoryService.deleteByID(id));
                if(resultMSG.getResult()==0){
                    resultMSG.setError("数据库执行删除失败");
                }
            }
            catch (Exception e){
                e.printStackTrace();
                resultMSG.setError("删除失败"+e.getMessage());
            }
        }
        return JSON.toJSONString(resultMSG);
    }
    @RequestMapping(value = "/get/{id}")
    public ModelAndView get(@PathVariable Integer id){
        ModelAndView modelAndView = new ModelAndView("/dormitoryManage/update");
        Dormitory dormitory =null;
        try{
            dormitory=dormitoryService.getDormitoryByID(id);
        }
        catch (Exception e){
            e.printStackTrace();

        }
        modelAndView.addObject("dormitory",dormitory);
        return modelAndView;
    }
    @RequestMapping(value = "/insert")
    @ResponseBody
    public  String insert(Dormitory dormitory){
        ResultMSG resultMSG = new ResultMSG();
        if(dormitory==null){
            resultMSG.setError("插入的寝室信息为空");
        }else {
            try{
                resultMSG.setResult(dormitoryService.insert(dormitory));
                if(resultMSG.getResult()==0){
                    resultMSG.setError("数据库执行插入寝室信息失败");
                }
            }
            catch (Exception e){
                e.printStackTrace();
                resultMSG.setError(e.getMessage());
            }
        }
        return JSON.toJSONString(resultMSG);
    }
    @RequestMapping(value = "/update")
    @ResponseBody
    public String update(Dormitory dormitory){
        ResultMSG resultMSG = new ResultMSG();
        if(dormitory==null){
            resultMSG.setError("寝室信息为空无法完成更新");
        }else {
            try{
                resultMSG.setResult(dormitoryService.update(dormitory));
                if(resultMSG.getResult()==0){
                    resultMSG.setError("数据库执行更新失败");
                }
            }
            catch (Exception e){
                e.printStackTrace();
                resultMSG.setError(e.getMessage());
            }
        }
        return JSON.toJSONString(resultMSG);
    }
    @RequestMapping(value = "/viewstu/{id}")
    public ModelAndView viewDormitoryStudent(@PathVariable Integer id){
        ModelAndView modelAndView = new ModelAndView("/dormitoryManage/viewStudent");
        List<UserBean> userBeanList =null;
        if(id!=null&&id>0){
            try{
                userBeanList = dormitoryService.getUserByDormitoryID(id);
            }
            catch (Exception e){
                e.printStackTrace();
            }
        }
        modelAndView.addObject("userList",userBeanList);
        return modelAndView;
    }
}
