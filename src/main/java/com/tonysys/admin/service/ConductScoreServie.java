package com.tonysys.admin.service;

import com.tonysys.admin.model.ConductScore;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:31
 * To change this template use File | Settings | File Templates.
 */
public interface ConductScoreServie {
    ConductScore getByID(Integer id);
    int update(ConductScore conductScore);
    int insert(ConductScore conductScore);
    int deleteByID(Integer id);
    int deleletByIDs(List<Integer> IDs);
    List<ConductScore> search(ConductScore conductScore,int page,int pageSize,String order,boolean isAll);
    PageIterator<ConductScore> pageSearch(ConductScore conductScore,int page,int pageSize,String order);
}
