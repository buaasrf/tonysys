package com.tonysys.admin.service.Impl;

import com.tonysys.admin.dao.UserDAO;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.service.UserService;
import com.tonysys.util.PageIterator;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:31
 * To change this template use File | Settings | File Templates.
 */
@Service("userService")
public class UserServiceImpl implements UserService {
    @Resource
    UserDAO userDAO;
    @Override
    public UserBean getUserByID(Integer id) {
        return userDAO.getUserByID(id);
    }

    @Override
    public int insert(UserBean userBean) {
        return userDAO.insert(userBean);
    }

    @Override
    public UserBean getUserByNumber(String number) {
        return userDAO.getUserByNumber(number);
    }

    @Override
    public int updateUser(UserBean userBean) {
        return userDAO.update(userBean);
    }

    @Override
    public int deleteUserByID(Integer id) {
        return 0;  
    }

    @Override
    public int deleteUserByNumber(String number) {
        return 0;  
    }

    @Override
    public List<UserBean> search(UserBean userBean, String order) {
        return null;  
    }

    @Override
    public int count(String whereStr) {
        return 0;  
    }

    @Override
    public PageIterator<UserBean> pageSearch(UserBean userBean, String order) {
        return null;  
    }
}
