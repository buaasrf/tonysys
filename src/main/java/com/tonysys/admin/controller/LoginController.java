package com.tonysys.admin.controller;

import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.service.UserService;
import com.tonysys.context.UserContext;
import com.tonysys.util.CookieUtil;
import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.view.RedirectView;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created with IntelliJ IDEA.
 * User: tony
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
    public String userLogin(HttpServletRequest request,HttpServletResponse response,String number,String password,Model model){
        String error="";
        int flag=1;

        UserBean userBean =null;
        if(StringUtils.isBlank(number)){
            flag=0;
            error="学号为空";
        }
        else if(StringUtils.isBlank(password)){
            flag=0;
            error="密码为空";
        }
        else {
            userBean =userService.getUserByNumber(number);
            if(userBean==null){
                flag=0;
                error="用户不存在";
            }
            else{
                if(!userBean.getPassword().equals(password)){
                    flag=0;
                    error = "用户密码不正确";
                }
            }
        }
        model.addAttribute("error",error).addAttribute("number",number);
        if(flag==0){
            return "redirect:/login.jsp";
        }
        String userToken = number+"_"+password;
        request.getSession().setAttribute(UserContext.USER_TOKEN,userBean);
        request.getSession().setAttribute(UserContext.USER_ID,userBean.getId());
        request.getSession().setAttribute(UserContext.USER_NUMBER,userBean.getNumber());
        request.getSession().setAttribute(UserContext.USER_NAME,userBean.getName());
        request.getSession().setAttribute(UserContext.LOGIN_TIME, new SimpleDateFormat("yyyy-MM-dd hh-mm-ss").format(new Date()));
        return "redirect:/index.jsp";
    }
}
