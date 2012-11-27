package com.tonysys.admin.controller;

import com.alibaba.fastjson.JSON;
import com.tonysys.admin.model.Bed;
import com.tonysys.admin.model.ResultMSG;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.service.UserService;
import com.tonysys.util.FastJsonHelper;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import javax.xml.ws.RequestWrapper;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:34
 * To change this template use File | Settings | File Templates.
 */
@Controller
@RequestMapping("/user")
public class UserController {
    @Resource
    UserService userService;
    @RequestMapping(value = "/get/{number}")
    @ResponseBody
    public String getUserByNumber(@PathVariable String number){
        return JSON.toJSONString(userService.getUserByNumber(number), FastJsonHelper.features);
    }
    @RequestMapping(value = "/insert")
    @ResponseBody
    public String insert(UserBean userBean,Bed bed){
        ResultMSG resultMSG = new ResultMSG();
        if(userBean==null){
            resultMSG.setError("学生信息为空，不能完成添加");
        }
        else {
            if(bed!=null&&bed.getId()!=null&&bed.getId()>0){
                userBean.setBed(bed);
            }
            try{
                resultMSG.setResult(userService.insert(userBean));
                if(resultMSG.getResult()==0){
                    resultMSG.setError("插入数据库失败");
                }
            }
            catch (Exception e)
            {
                e.printStackTrace();
                resultMSG.setError(e.getMessage());
            }
        }
        return JSON.toJSONString(resultMSG);
    }
}
