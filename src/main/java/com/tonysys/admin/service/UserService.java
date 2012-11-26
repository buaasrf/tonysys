package com.tonysys.admin.service;

import com.tonysys.admin.model.UserBean;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:30
 * To change this template use File | Settings | File Templates.
 */
public interface UserService {
    UserBean getUserByID(Integer id);
    UserBean getUserByNumber(String number);
    int updateUser(UserBean userBean);
    int deleteUserByID(Integer id);
    int deleteUserByNumber(String number);

    List<UserBean> search(UserBean userBean,String order);
    int count(String whereStr);
    PageIterator<UserBean> pageSearch(UserBean userBean,String order);
}
