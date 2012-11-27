package com.tonysys.admin.dao.Impl;

import com.mysql.jdbc.Statement;
import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.UserBean;
import com.tonysys.admin.rowMapper.DormitoryRowMapper;
import com.tonysys.admin.rowMapper.UserBeanNoDormitoryRowMapper;
import com.tonysys.admin.rowMapper.UserBeanRowMapper;
import com.tonysys.util.PageIterator;
import net.sf.ehcache.CacheManager;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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
    @Resource
    DormitoryRowMapper dormitoryRowMapper;
    @Resource
    UserBeanRowMapper userBeanRowMapper;
    @Resource
    UserBeanNoDormitoryRowMapper userBeanNoDormitoryRowMapper;

    @Override
    public Dormitory getDormitoryByID(Integer id) {
        if(id ==null||id<=0){
            log.warn("宿舍信息id为空");
            return null;
        }
        Dormitory dormitory =null;
        log.info("获取宿舍id为{}的信息",id);
        try{
            dormitory = tonysysJdbcTemplate.queryForObject("select * from  dormitory where id=?",new Object[]{id},dormitoryRowMapper);
            log.info("获取的宿舍信息为：{}", dormitory.toString());
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return dormitory;
    }

    @Override
    public Dormitory getDormitoryByUserID(Integer id) {
        if(id ==null||id<=0){
            log.warn("宿舍信息id为空");
            return null;
        }
        Dormitory dormitory =null;
        log.info("获取宿舍id为{}的信息",id);
        try{
            dormitory = tonysysJdbcTemplate.queryForObject("select dormitory.* from  dormitory inner join bed on dormitory.id = bed.dormitoryid  where bed.userid=?",new Object[]{id},dormitoryRowMapper);
            log.info("获取的宿舍信息为：{}", dormitory.toString());
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return dormitory;
    }

    @Override
    public List<UserBean> getUserByDormitoryID(Integer id) {
        log.info("begin search UserBean list by dormitory id:{}",id);
        if(id==null){
            return null;
        }
        List<UserBean> userList =null;
        try{
            userList =tonysysJdbcTemplate.query("select user.* from user inner join bed on bed.userid=user.id  where bed.dormitoryid=?",new Object[]{id},userBeanNoDormitoryRowMapper);
            log.info("search userBean list size:{}",userList.size());
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return userList;
    }

    @Override
    public int insert(final Dormitory dormitory) {
        log.info("user begin to insert into dormitory：{}",dormitory.toString());
        if(dormitory==null){
            log.info("dormitory is null");
            return 0;
        }
        int result=0;
            final StringBuffer insertStr= new StringBuffer("(");
            KeyHolder keyHolder = new  GeneratedKeyHolder();
            insertStr.append(Dormitory.BUILDING).append(",").append(Dormitory.ROOM).append(",").append(Dormitory.DOOR)
                    .append(",").append(Dormitory.BEDNUMBER).append(",").append(Dormitory.TEL).append(")");
            result=tonysysJdbcTemplate.update(new PreparedStatementCreator() {
                @Override
                public PreparedStatement createPreparedStatement(Connection connection) throws SQLException {
                    PreparedStatement ps = connection.prepareStatement("insert into "+Dormitory.TABLENAME+insertStr.toString()+" values" +
                            "(?,?,?,?,?)", Statement.RETURN_GENERATED_KEYS);
                    ps.setString(1,dormitory.getBuilding());
                    ps.setString(2,dormitory.getRoom());
                    ps.setString(3,dormitory.getDoor());
                    ps.setInt(4, dormitory.getBednumber());
                    ps.setString(5,dormitory.getTel());
                    return ps;
                }
            },keyHolder);
            result =keyHolder.getKey().intValue();
            if(result>0&&dormitory.getBednumber()!=null&&dormitory.getBednumber()>0){
                for(int i=1;i<=dormitory.getBednumber();i++){
                    tonysysJdbcTemplate.update("insert into bed (number,dormitoryid) values(?,?)",new Object[]{i,result});
                }
            }
            log.info("insert database dormitory {}",result==0?"failed":"success");
        return result;
    }

    @Override
    public int update(Dormitory dormitory) {
        log.info("begin to update dormitory:{}",dormitory);
        if(dormitory==null||dormitory.getId()==null){
            log.info("dormitory is null");
            return 0;
        }
        int result=0;
        try{
            StringBuffer updateStr = new StringBuffer();
            updateStr.append(" set ").append(Dormitory.BUILDING).append("=?,")
                    .append(Dormitory.ROOM).append("=?,")
                    .append(Dormitory.DOOR).append("=?,")
                    .append(Dormitory.BEDNUMBER).append("=?,")
                    .append(Dormitory.TEL).append("=? where ").append(Dormitory.ID).append("=?");
            result = tonysysJdbcTemplate.update("update "+Dormitory.TABLENAME+updateStr.toString()
                    ,new Object[]{dormitory.getBuilding(),dormitory.getRoom(),dormitory.getDoor(),dormitory.getBednumber(),dormitory.getTel(),dormitory.getId()});
            log.info("update database dormitory {}",result==0?"failed":"success");
        }
        catch (Exception e){
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public int count(String whereStr) {
        log.info("begin to count dormitory by condition:{}",whereStr);
        if(StringUtils.isBlank(whereStr)){
            return 0;
        }
        int result=0;
        try{
            result=tonysysJdbcTemplate.queryForInt("select count(1) from "+Dormitory.TABLENAME+" where "+whereStr);
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return result;
    }

    @Override
    public List<Dormitory> search(Dormitory dormitory, int page, int pageSize, String order, boolean isall) {
        if(page<1){
            page =1;
        }
        if(pageSize<0||pageSize==Integer.MAX_VALUE){
            pageSize=300;
        }
        String pageStr = "";
        if(!isall){
            pageStr=" limit "+((page-1)*pageSize)+","+pageSize+" ";
        }
        List<Dormitory> dormitoryList = null;
        try{
            dormitoryList = tonysysJdbcTemplate.query("select * from "+Dormitory.TABLENAME+" where "+createWhereStr(dormitory)+pageStr+getOrderStr(order),dormitoryRowMapper);
        }
        catch (Exception e){
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return dormitoryList;
    }

    @Override
    public PageIterator<Dormitory> pageSearch(Dormitory dormitory, int page, int pageSize, String order) {
        if(page<1){
            page =1;
        }
        if(pageSize<0||pageSize==Integer.MAX_VALUE){
            pageSize=300;
        }
        String whereStr = createWhereStr(dormitory);
        String orderBy = getOrderStr(order);
        log.info("begin page search from database page:{} pageSize:{} where:{} order:{}",page,pageSize,whereStr,order);
        int count =count(whereStr);
        PageIterator<Dormitory> pageIterator =  PageIterator.createInstance(page,pageSize,count);
        try{
            List<Dormitory> dormitoryList =tonysysJdbcTemplate.query("select * from "+Dormitory.TABLENAME+" where "+whereStr+" limit "+((page-1)*pageSize)+","+pageSize+ orderBy,dormitoryRowMapper);
            pageIterator.setData(dormitoryList);
            log.info("page search dormitory from database rows:{}",dormitoryList.size());
        }
        catch (Exception e){
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return pageIterator;
    }
    private String getOrderStr(String order){
        return StringUtils.isBlank(order)?"":(" order by "+order);
    }
    private  String createWhereStr(Dormitory dormitory){
        StringBuffer whereStr = new StringBuffer(" 1=1 ");
        if(dormitory!=null){
            if(StringUtils.isNotBlank(dormitory.getBuilding())){
                whereStr.append(" and ").append(Dormitory.BUILDING).append("='").append(dormitory.getBuilding().trim()).append("'");
            }
            if(StringUtils.isNotBlank(dormitory.getRoom())){
                whereStr.append(" and ").append(Dormitory.ROOM).append("='").append(dormitory.getRoom().trim()).append("'");
            }
            if(StringUtils.isNotBlank(dormitory.getDoor())){
                whereStr.append(" and ").append(Dormitory.DOOR).append("='").append(dormitory.getDoor().trim()).append("'");
            }
            if(dormitory.getBednumber()!=null){
                whereStr.append(" and ").append(Dormitory.BEDNUMBER).append("=").append(dormitory.getBednumber());
            }
            if(StringUtils.isNotBlank(dormitory.getTel())){
                whereStr.append(" and ").append(Dormitory.TEL).append(" like'%").append(dormitory.getTel().trim()).append("%'");
            }
        }
        return whereStr.toString();
    }
    @Override
    public int deleteByID(Integer id) {
        log.info("begin to delete dormitory by id:{}",id);
        if(id==null){
            return 0;
        }
        int result=0;
        try{
            result=tonysysJdbcTemplate.update("delete from "+Dormitory.TABLENAME+" where id=?",new Object[]{id});
            log.info("delete database dormitory {}",result==0?"failed":"success");
        }
        catch (Exception e){
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public int deleteByIDs(List<Integer> IDs) {
        if(IDs==null){
            return 0;
        }
        int result=0;
        for(Integer id:IDs){
            result+=deleteByID(id);
        }
        return result;
    }
}
