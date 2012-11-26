package com.tonysys.admin.controller;

import com.alibaba.fastjson.JSON;
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
}
