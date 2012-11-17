package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.UserDAO;
import com.tonysys.admin.model.UserBean;
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
 * Time: 下午2:19
 * To change this template use File | Settings | File Templates.
 */
@Repository("userDAO")
public class UserDAOImpl implements UserDAO {
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    CacheManager ehCacheManager;

    @Override
    public UserBean getUserByID(Integer id) {
        if(id==null){
            return null;
        }
        return null;
    }

    @Override
    public UserBean getUserByNumber(String number) {
        return null;  
    }

    @Override
    public int update(UserBean userBean) {
        return 0;  
    }

    @Override
    public PageIterator<UserBean> pageSearch(UserBean userBean, int page, int pageSize, String order) {
        return null;  
    }

    @Override
    public List<UserBean> search(UserBean userBean, int page, int pageSize, String order, boolean isall) {
        return null;  
    }
}
