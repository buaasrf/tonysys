package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.rowMapper.DormitoryRowMapper;
import com.tonysys.admin.rowMapper.UserBeanRowMapper;
import com.tonysys.util.PageIterator;
import net.sf.ehcache.CacheManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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
    private static final Logger log = LoggerFactory.getLogger(DormitoryDAOImpl.class);
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    CacheManager ehCacheManager;

    @Override
    public Dormitory getDormitoryByID(Integer id) {
        if(id ==null){
            log.warn("宿舍信息id为空");
            return null;
        }
        Dormitory dormitory =null;
        log.info("获取宿舍id为{}的信息",id);
        try{
            dormitory = tonysysJdbcTemplate.queryForObject("select * from "+Dormitory.TABLENAME+" where id=?",new Object[]{id},new DormitoryRowMapper());
            log.info("获取的宿舍信息为：{}", dormitory.toString());
        }
        catch (Exception e){
            log.error(e.getMessage());
        }
        return dormitory;
    }

    @Override
    public List<UserBean> getUserByDormitoryID(Integer id) {
        if(id==null){
            return null;
        }
        List<UserBean> userList =null;
        try{
            userList =tonysysJdbcTemplate.query("select "+UserBean.TABLENAME+".* from "+UserBean.TABLENAME+" inner join user_dormitory on "+UserBean.TABLENAME+".id=user_dormitory.userid where user_dormitory.dormitoryid=?",new Object[]{id},new UserBeanRowMapper());
        }
        catch (Exception e){
            log.error(e.getMessage());
        }
        return userList;
    }

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
