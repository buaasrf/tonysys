package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.ConductScoreDAO;
import com.tonysys.admin.model.ConductScore;
import com.tonysys.util.PageIterator;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午3:21
 * To change this template use File | Settings | File Templates.
 */
public class ConductScoreDAOImpl implements ConductScoreDAO{
    @Override
    public int insert(ConductScore conductSorce) {
        return 0;  
    }

    @Override
    public int update(ConductScore conductScore) {
        return 0;  
    }

    @Override
    public int deleteByID(Integer id) {
        return 0;  
    }

    @Override
    public int deleteByIDs(List<Integer> IDs) {
        return 0;  
    }

    @Override
    public List<ConductScore> search(ConductScore conductScore, int page, int pageSize, String order, boolean isall) {
        return null;  
    }

    @Override
    public PageIterator<ConductScore> pageSearch(ConductScore conductScore, int page, int pageSize, String order) {
        return null;  
    }
}
