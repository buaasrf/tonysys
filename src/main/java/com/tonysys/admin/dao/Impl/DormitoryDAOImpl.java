package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.util.PageIterator;
import net.sf.ehcache.CacheManager;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午3:19
 * To change this template use File | Settings | File Templates.
 */
@Repository("dormitoryDAO")
public class DormitoryDAOImpl implements DormitoryDAO {
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    CacheManager ehCacheManager;
    @Override
    public int insert(Dormitory dormitory) {
        return 0;  
    }

    @Override
    public int update(Dormitory dormitory) {
        return 0;  
    }

    @Override
    public List<Dormitory> search(Dormitory dormitory, int page, int pageSize, String order, boolean isall) {
        return null;  
    }

    @Override
    public PageIterator<Dormitory> pageSearch(Dormitory dormitory, int page, int pageSize, String order) {
        return null;  
    }

    @Override
    public int deleteByID(Integer id) {
        return 0;  
    }

    @Override
    public int deleteByIDs(List<Integer> IDs) {
        return 0;  
    }
}
