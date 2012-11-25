package com.tonysys.admin.service.Impl;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.service.DormitoryService;
import com.tonysys.util.PageIterator;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-18
 * Time: 上午12:32
 * To change this template use File | Settings | File Templates.
 */
@Service("dormitoryService")
public class DormitoryServiceImpl implements DormitoryService {
    @Resource
    DormitoryDAO dormitoryDAO;
    @Override
    public Dormitory getDormitoryByID(Integer id) {
        return dormitoryDAO.getDormitoryByID(id);
    }

    @Override
    public int insert(Dormitory dormitory) {
        return dormitoryDAO.insert(dormitory);
    }

    @Override
    public int update(Dormitory dormitory) {
        return dormitoryDAO.update(dormitory);
    }

    @Override
    public int deleteByID(Integer id) {
        return dormitoryDAO.deleteByID(id);
    }

    @Override
    public int deleteByIDs(List<Integer> IDs) {
        return dormitoryDAO.deleteByIDs(IDs);
    }

    @Override
    public List<Dormitory> search(Dormitory dormitory, int page, int pageSize, String order, boolean isAll) {
        return dormitoryDAO.search(dormitory,page,pageSize,order,isAll);
    }

    @Override
    public PageIterator<Dormitory> pageSearch(Dormitory dormitory, int page, int pageSize, String order) {
        return dormitoryDAO.pageSearch(dormitory,page,pageSize,order);
    }

    @Override
    public int count(String whereStr) {
        return dormitoryDAO.count(whereStr);
    }
}
