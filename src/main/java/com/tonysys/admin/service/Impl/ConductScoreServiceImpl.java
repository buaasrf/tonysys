package com.tonysys.admin.service.Impl;

import com.tonysys.admin.dao.ConductScoreDAO;
import com.tonysys.admin.model.ConductScore;
import com.tonysys.admin.service.ConductScoreServie;
import com.tonysys.util.PageIterator;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-18
 * Time: 上午12:33
 * To change this template use File | Settings | File Templates.
 */
@Service("conductScoreService")
public class ConductScoreServiceImpl implements ConductScoreServie {
    @Resource
    ConductScoreDAO conductScoreDAO;
    @Override
    public ConductScore getByID(Integer id) {
        return conductScoreDAO.getByID(id);
    }

    @Override
    public int update(ConductScore conductScore) {
        return conductScoreDAO.update(conductScore);
    }

    @Override
    public int insert(ConductScore conductScore) {
        return conductScoreDAO.insert(conductScore);
    }

    @Override
    public int deleteByID(Integer id) {
        return conductScoreDAO.deleteByID(id);
    }

    @Override
    public int deleletByIDs(List<Integer> IDs) {
        return conductScoreDAO.deleteByIDs(IDs);
    }

    @Override
    public List<ConductScore> search(ConductScore conductScore, int page, int pageSize, String order,boolean isAll) {
        return conductScoreDAO.search(conductScore,page,pageSize,order,isAll);
    }

    @Override
    public PageIterator<ConductScore> pageSearch(ConductScore conductScore, int page, int pageSize, String order) {
        return conductScoreDAO.pageSearch(conductScore,page,pageSize,order);
    }
}
