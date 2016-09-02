package com.baidu.onlineedit.service;

import com.baidu.onlineedit.dao.UserDao;
import com.baidu.onlineedit.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Created by zpw on 16-2-20.
 */
@Service
public class UserService {

    @Autowired
    private UserDao userDao;

    public List<User> findAll() {
        return userDao.findAll();
    }
}
