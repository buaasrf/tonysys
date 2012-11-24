package com.tonysys.admin.controller;

import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.service.UserService;
import com.tonysys.context.UserContext;
import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-19
 * Time: 上午12:10
 * To change this template use File | Settings | File Templates.
 */
@Controller
@RequestMapping("/login")
public class LoginController {
    @Resource
    UserService userService;
    @RequestMapping(value = "/")
    public String userLogin(HttpServletRequest request,String number,String password,Model model){
        String error="";
        int flag=1;

        if(StringUtils.isBlank(number)){
            flag=0;
            error="学号为空";
        }
        else if(StringUtils.isBlank(password)){
            flag=0;
            error="密码为空";
        }
        else {
            UserBean userBean =userService.getUserByNumber(number);
            if(!userBean.getPassword().equals(password)){
                flag=0;
                error = "用户密码不正确";
            }
        }
        model.addAttribute("error", error);
        model.addAttribute("number", number);
        if(flag==0){
            return "/login";
        }
        return "redirect:/index.jsp";
    }
}
