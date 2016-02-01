package com.errpro.Test.web.controller;

import com.errpro.Test.entity.Product;
import com.errpro.Test.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

/**
 * Created by zhangpan05 on 2016/1/5.
 */
@Controller
@RequestMapping("/product")
public class ProductController {

    @Autowired
    private ProductService productService;

    @RequestMapping(value = {"", "/", "/list"})
    public String list(@RequestParam(value = "page", defaultValue = "0") int page,
                       @RequestParam(value = "size", defaultValue = "50") int size, Model model) {
        model.addAttribute("products", productService.getProducts());
        return "list";
    }

    @RequestMapping(value = {"/add", "/add/"})
    public String addForm(Model model) {
        Product product = new Product();
        model.addAttribute("product", product);
        return "form";
    }

    @RequestMapping(value = {"/del/{id}"}, method = RequestMethod.DELETE)
    public String delete(@PathVariable("id") long id, Model model) {
        productService.deleteProduct(id);
        return "redirect:list";
    }

    @RequestMapping(value = {"/edit/{id}"})
    public String updateForm(@PathVariable("id") Long id, Model model) {
        Product product = productService.getProduct(id);
        model.addAttribute("product", product);
        return "form";
    }

    @RequestMapping(value = {"/update"}, method = RequestMethod.POST)
    public String update(@ModelAttribute("product") Product product) {
        productService.save(product);
        return "redirect:list";
    }

}
