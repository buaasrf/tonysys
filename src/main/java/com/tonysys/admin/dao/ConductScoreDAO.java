package com.tonysys.admin.dao;

import com.tonysys.admin.model.ConductScore;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午3:15
 * To change this template use File | Settings | File Templates.
 */
public interface ConductScoreDAO {
    int insert(ConductScore conductSorce);
    int update(ConductScore conductScore);
    int deleteByID(Integer id);
    int deleteByIDs(List<Integer>IDs);
    List<ConductScore> search(ConductScore conductScore,int page,int pageSize,String order,boolean isall);
    PageIterator<ConductScore> pageSearch(ConductScore conductScore,int page,int pageSize,String order);
}
