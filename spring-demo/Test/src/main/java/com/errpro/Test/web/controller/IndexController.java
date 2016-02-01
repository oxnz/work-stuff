package com.errpro.Test.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * Created by zhangpan05 on 2016/1/5.
 */
@Controller
public class IndexController {

    @RequestMapping(value = {"/"})
    public String index() {
        return "index";
    }
}
