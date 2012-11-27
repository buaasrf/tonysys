package com.tonysys.admin.service;

import com.tonysys.admin.model.Dormitory;
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
public interface DormitoryService {
    Dormitory getDormitoryByID(Integer id);
    int insert(Dormitory dormitory);
    int update(Dormitory dormitory);
    int deleteByID(Integer id);
    int deleteByIDs(List<Integer> IDs);
    List<Dormitory> search(Dormitory dormitory,int page,int pageSize,String order,boolean isAll);
    PageIterator<Dormitory> pageSearch(Dormitory dormitory,int page,int pageSize,String order);
    List<UserBean> getUserByDormitoryID(Integer id);
    int count(String whereStr);
}
