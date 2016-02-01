package com.errpro.Test.service;

import com.errpro.Test.dao.ProductDao;
import com.errpro.Test.entity.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Created by zhangpan05 on 2016/1/5.
 */
@Service
public class ProductService {

    @Autowired
    private ProductDao productDao;

    public List<Product> getProducts() {
        return productDao.findAll();
    }

    public Page<Product> getProducts(int page, int size) {
        Pageable pageable = new PageRequest(page, size);
        return getProducts(new PageRequest(page, size));
    }

    public Page<Product> getProducts(Pageable pageable) {
        return productDao.findAll(pageable);
    }

    public Product getProduct(long id) {
        return productDao.findById(id);
    }

    public void save(Product product) {
        productDao.save(product);
    }

    public void deleteProduct(long id) {
        productDao.delete(id);
    }
}
