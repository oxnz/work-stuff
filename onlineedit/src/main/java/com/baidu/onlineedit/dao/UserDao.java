package com.baidu.onlineedit.dao;

import com.baidu.onlineedit.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Created by zpw on 15-11-25.
 */
@Repository
public interface UserDao extends JpaRepository<User, Long> {
}
