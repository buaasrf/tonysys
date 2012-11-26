package com.tonysys.admin.dao;

import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.UserBean;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午3:12
 * To change this template use File | Settings | File Templates.
 */
public interface DormitoryDAO {
    Dormitory getDormitoryByID(Integer id);
    List<UserBean> getUserByDormitoryID(Integer id);
    int insert(Dormitory dormitory );
    int update(Dormitory dormitory);
    int count(String whereStr);
    List<Dormitory> search(Dormitory dormitory,int page,int pageSize,String order,boolean isall);
    PageIterator<Dormitory> pageSearch(Dormitory dormitory,int page,int pageSize,String order);
    int deleteByID(Integer id);
    int deleteByIDs(List<Integer> IDs);
}
