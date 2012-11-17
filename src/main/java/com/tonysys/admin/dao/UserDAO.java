package com.tonysys.admin.dao;

import com.tonysys.admin.model.UserBean;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午12:47
 * To change this template use File | Settings | File Templates.
 */

public interface UserDAO {
    int update(UserBean userBean);
    PageIterator<UserBean> pageSearch(UserBean userBean,int page,int pageSize,String order);
    List<UserBean> search(UserBean userBean,int page,int pageSize,String order,boolean isall);
}
