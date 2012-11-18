package com.tonysys.admin.controller;

import com.tonysys.context.UserContext;
import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

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
    @RequestMapping(value = "/{userName}/{password}")
    public ModelAndView userLogin(HttpServletRequest request,@PathVariable String userName,@PathVariable String password){
        String error="";
        int flag=1;
        ModelAndView modelAndView = new ModelAndView();

        if(StringUtils.isBlank(userName)){
            flag=0;
            error="用户名为空";
        }
        if(StringUtils.isBlank(password)){
            flag=0;
            error="密码为空";
        }
        Map<String,Object> resultMap = new HashMap<String, Object>();
        resultMap.put("flag",flag);
        resultMap.put("error",error);
        if(flag==0){
            resultMap.put("redirect","/login.jsp");
        }
        else {
            resultMap.put("redirect","/index.jsp");
        }
        modelAndView.addAllObjects(resultMap);
        request.getSession().setAttribute(UserContext.USER_NAME,userName);
        return modelAndView;
    }
}
