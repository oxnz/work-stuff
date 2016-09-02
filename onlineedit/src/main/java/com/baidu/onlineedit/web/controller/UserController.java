/**
 * Copyright (C) 2015 Baidu, Inc. All Rights Reserved.
 */
package com.baidu.onlineedit.web.controller;

import com.baidu.onlineedit.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * 
 * @author huangdong01
 */
@RequestMapping("/user")
@Controller
public class UserController {

    @Autowired
    private UserService userService;

    @RequestMapping("/list")
    public String list(Model model) {
        model.addAttribute("users", userService.findAll());
        return "list";
    }

}
