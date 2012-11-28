package com.tonysys.admin.dao.Impl;

import com.mysql.jdbc.Statement;
import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.dao.UserDAO;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.rowMapper.UserBeanNoDormitoryRowMapper;
import com.tonysys.admin.rowMapper.UserBeanRowMapper;
import com.tonysys.util.PageIterator;
import net.sf.ehcache.CacheManager;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.PreparedStatementCreator;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午2:19
 * To change this template use File | Settings | File Templates.
 */
@Repository("userDAO")
public class UserDAOImpl implements UserDAO {
    private  static final Logger log = LoggerFactory.getLogger(UserDAOImpl.class);
    @Resource
    DormitoryDAO dormitoryDAO;
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    CacheManager ehCacheManager;
    @Resource
    UserBeanRowMapper userBeanRowMapper;
    @Resource
    UserBeanNoDormitoryRowMapper userBeanNoDormitoryRowMapper;
    @Override
    public UserBean getUserByID(Integer id) {
        log.info("根据学生id{},获取用户信息",id);
        if(id==null){
            return null;
        }
        UserBean userBean = null;
        try{
            userBean = tonysysJdbcTemplate.queryForObject("select * from "+UserBean.TABLENAME+" where "+UserBean.ID+"=?",new Object[]{id},userBeanNoDormitoryRowMapper);
        }
        catch (Exception e){
             log.error(e.getMessage());
        }
        return userBean;
    }

    @Override
    public UserBean getUserNoDormitoryByID(Integer id) {
        log.info("根据学生id{},获取用户信息",id);
        if(id==null){
            return null;
        }
        UserBean userBean = null;
        try{
            userBean = tonysysJdbcTemplate.queryForObject("select * from "+UserBean.TABLENAME+" where "+UserBean.ID+"=?",new Object[]{id},userBeanRowMapper);
        }
        catch (Exception e){
            log.error(e.getMessage());
        }
        return userBean;
    }

    @Override
    public UserBean getUserByNumber(String number) {
        log.info("根据学生number{},获取用户信息",number);
        if(StringUtils.isBlank(number)){
            return null;
        }
        UserBean userBean = null;
        try{
            userBean = tonysysJdbcTemplate.queryForObject("select * from "+UserBean.TABLENAME+" where "+UserBean.NUMBER+"=?",new Object[]{number},userBeanRowMapper);
        }
        catch (EmptyResultDataAccessException e){
            log.error("根据number为{},的用户不存在。",userBean.getNumber());
        }
        return userBean;
    }

    @Override
    public int insert(final UserBean userBean) {
        if(userBean==null){
            return 0;
        }
        int result = 0;
        KeyHolder keyHolder = new GeneratedKeyHolder();
        result = tonysysJdbcTemplate.update(new PreparedStatementCreator() {
            @Override
            public PreparedStatement createPreparedStatement(Connection connection) throws SQLException {
                PreparedStatement ps =connection.prepareStatement("insert into user (name," +
                        "number,gender,birth,idNumber,province,dept," +
                        "trainingLevel,subject,grade,homePhone,phone) " +
                        "values(?,?,?,?,?,?,?,?,?,?,?,?)",
                        Statement.RETURN_GENERATED_KEYS);
                ps.setString(1,userBean.getName());
                ps.setString(2,userBean.getNumber());
                ps.setString(3,userBean.getGender());
                ps.setString(4,userBean.getBirth());
                ps.setString(5,userBean.getIdNumber());
                ps.setString(6,userBean.getProvince());
                ps.setString(7,userBean.getDept());
                ps.setString(8,userBean.getTrainingLevel());
                ps.setString(9,userBean.getSubject());
                ps.setString(10,userBean.getGrade());
                ps.setString(11,userBean.getHomePhone());
                ps.setString(12,userBean.getPhone());
                return ps;
            }
        },keyHolder);
        if(result>0){
            result = keyHolder.getKey().intValue();
            if(userBean.getBed()!=null&&userBean.getBed().getId()!=null&&userBean.getBed().getId()>0){
                tonysysJdbcTemplate.update("update bed set userid=? where id=?",new Object[]{result,userBean.getBed().getId()});
            }
        }
        return result;
    }

    @Override
    public int update(UserBean userBean) {
        return 0;  
    }

    @Override
    public int count(String whereStr) {
        if(StringUtils.isBlank(whereStr)){
            return 0;
        }
        int result=0;
        try{
            result=tonysysJdbcTemplate.queryForInt("select count(1) from "+UserBean.TABLENAME+" where "+whereStr);
        }
        catch (Exception e){
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return result;
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
