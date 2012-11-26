package com.tonysys.admin.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-25
 * Time: 下午1:47
 * To change this template use File | Settings | File Templates.
 */
@Controller
@RequestMapping("/")
public class IndexController {
    @RequestMapping(value = "/index")
    public String index() {
        return "redirect:/index.jsp";
    }

}
