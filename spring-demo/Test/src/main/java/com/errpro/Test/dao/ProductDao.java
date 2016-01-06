package com.errpro.Test.dao;

import com.errpro.Test.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by zhangpan05 on 2016/1/5.
 */
@Service
public class ProductDao {

    static Map<Long, Product> productMap = new HashMap<Long, Product>();

    public List<Product> findAll() {
        return new ArrayList<Product>(productMap.values());
    }
    public Page<Product> findAll(Pageable pageable) {
        return null;
    }

    public void save(Product product) {
        productMap.put(product.getId(), product);
    }

    public Product findById(Long id) {
        return productMap.get(id);
    }

    public void delete(long id) {
        productMap.remove(id);
    }
}
