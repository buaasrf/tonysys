package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.ConductScoreDAO;
import com.tonysys.admin.model.ConductScore;
import com.tonysys.admin.rowMapper.ConductScoreRowMapper;
import com.tonysys.util.PageIterator;
import net.sf.ehcache.CacheManager;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午3:21
 * To change this template use File | Settings | File Templates.
 */
@Repository("conductScoreDAO")
public class ConductScoreDAOImpl implements ConductScoreDAO{
    private static final Logger log = LoggerFactory.getLogger(ConductScoreDAOImpl.class);
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    CacheManager ehCacheManager;

    @Override
    public ConductScore getByID(Integer id) {
        if(id==null){
            return  null;
        }
        ConductScore conductScore=null;
        try{
            conductScore = tonysysJdbcTemplate.queryForObject("select * from "+ConductScore.TABLENAME+" where id=?",new Object[]{id},new ConductScoreRowMapper());
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return conductScore;
    }

    @Override
    public int insert(ConductScore conductSorce) {
        if(conductSorce==null ){
            return 0;
        }

        int result=0;
        try{
            log.info("开始插入conductScore:"+conductSorce.toString());

            result =tonysysJdbcTemplate.update("insert into "+ ConductScore.TABLENAME+" (type,number,name,grade,score,time,place,remark,description,updateBy,updateDate,createBy,createDate,) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    new Object[]{conductSorce.getType(),conductSorce.getNumber(),conductSorce.getName(),conductSorce.getGrade(),conductSorce.getScore(),conductSorce.getTime(),conductSorce.getPlace(),conductSorce.getRemark(),
                    conductSorce.getDescription(),conductSorce.getUpdateBy(),conductSorce.getUpdateDate(),conductSorce.getCreateBy(),conductSorce.getCreateDate()});
        }
        catch (Exception e){
            log.error("插入操行分失败：{}",e.getMessage());
        }
        return result;
    }

    @Override
    public int update(ConductScore conductScore) {
        if(conductScore==null){
            return 0;
        }
        int result=0;
        try{
            StringBuffer updateStr= new StringBuffer();
            updateStr.append(" set ")
                    .append(ConductScore.DESCRIPTION).append("=?,")
                    .append(ConductScore.GRADE).append("=?,")
                    .append(ConductScore.NAME).append("=?,")
                    .append(ConductScore.NUMBER).append("=?,")
                    .append(ConductScore.PLACE).append("=?,")
                    .append(ConductScore.REMARK).append("=?,")
                    .append(ConductScore.SCORE).append("=?,")
                    .append(ConductScore.TIME).append("=?,")
                    .append(ConductScore.TYPE).append("=? where ").append(ConductScore.ID).append("=?");
            result=tonysysJdbcTemplate.update("update "+ConductScore.TABLENAME+updateStr.toString()
                    ,new Object[]{conductScore.getDescription(),conductScore.getGrade(),conductScore.getName()
                    ,conductScore.getNumber(),conductScore.getPlace(),conductScore.getRemark(),conductScore.getScore()
            ,conductScore.getTime(),conductScore.getType(),conductScore.getId()});
            log.info("update database ConductSorce {}",(result==0?"failed":"success"));
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return result;
    }

    @Override
    public int deleteByID(Integer id) {
        if(id==null){
            return 0;
        }
        int result =0;
        try{
            result=tonysysJdbcTemplate.update("delete from "+ConductScore.TABLENAME+" where "+ConductScore.ID+"=?",new Object[]{id});

        }
        catch (Exception e){
            log.error("删除操行分失败：{}",e.getMessage());
        }
        return result;
    }

    @Override
    public int deleteByIDs(List<Integer> IDs) {
        if(IDs==null){
            return 0;
        }
        int result=0;

        try{
            for(Integer id:IDs){
                result+=deleteByID(id);
            }
        }
        catch (Exception e){
            log.error("批量删除操行分失败：{}",e.getMessage());
        }
        return result;
    }

    @Override
    public int count(String whereStr) {
        if(StringUtils.isBlank(whereStr)){
            return 0;
        }
        int result=0;
        try{
            result=tonysysJdbcTemplate.queryForInt("select count(1) from "+ConductScore.TABLENAME+" where "+ whereStr);
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return result;
    }

    @Override
    public List<ConductScore> search(ConductScore conductScore, int page, int pageSize, String order, boolean isall) {
        if(page<1){
            page=1;
        }
        if(pageSize<0||pageSize==Integer.MAX_VALUE){
            pageSize=300;
        }
        String whereStr = createWhereStr(conductScore);
        int count = count(whereStr);
        List<ConductScore> conductScoreList=null;
        try{
            conductScoreList = tonysysJdbcTemplate.query("select * from "+ConductScore.TABLENAME+" where "+whereStr+" limit "+((page-1)*pageSize)+","+pageSize+getOrderStr(order),new ConductScoreRowMapper());
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return conductScoreList;
    }

    @Override
    public PageIterator<ConductScore> pageSearch(ConductScore conductScore, int page, int pageSize, String order) {
        if(page<1){
            page=1;
        }
        if(pageSize<0||pageSize==Integer.MAX_VALUE){
            pageSize=300;
        }
        String whereStr = createWhereStr(conductScore);
        int count = count(whereStr);
        PageIterator<ConductScore> pageIterator = PageIterator.createInstance(page,pageSize,count);
        try{
            List<ConductScore> conductScoreList = tonysysJdbcTemplate.query("select * from " + ConductScore.TABLENAME + " where " + whereStr + " limit " + ((page - 1) * pageSize) + "," + pageSize + getOrderStr(order), new ConductScoreRowMapper());
            pageIterator.setData(conductScoreList);
        }
        catch (Exception e){
            e.printStackTrace();
            log.error(e.getMessage());
        }
        return pageIterator;
    }
    private String  getOrderStr(String order){
        return order==null?"":(" order by "+order);
    }
    private String createWhereStr(ConductScore conductScore){
        StringBuffer whereStr = new StringBuffer(" 1=1 ");
        if(conductScore!=null){
            if(StringUtils.isNotBlank(conductScore.getNumber())){
                whereStr.append(" and ").append(ConductScore.NUMBER).append("='").append(conductScore.getNumber().trim()).append("'");
            }
            if(StringUtils.isNotBlank(conductScore.getName())){
                whereStr.append(" and ").append(ConductScore.NAME).append("='").append(conductScore.getName().trim()).append("'");
            }
            if(StringUtils.isNotBlank(conductScore.getGrade())){
                whereStr.append(" and ").append(ConductScore.GRADE).append("='").append(conductScore.getGrade().trim()).append("'");
            }
            if(StringUtils.isNotBlank(conductScore.getType())){
                whereStr.append(" and ").append(ConductScore.TYPE).append("='").append(conductScore.getType()).append("'");
            }
        }
        return whereStr.toString();
    }
}
