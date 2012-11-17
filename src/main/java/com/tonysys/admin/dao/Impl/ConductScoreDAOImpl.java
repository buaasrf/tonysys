package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.ConductScoreDAO;
import com.tonysys.admin.model.ConductScore;
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
        return 0;  
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
    public List<ConductScore> search(ConductScore conductScore, int page, int pageSize, String order, boolean isall) {
        return null;  
    }

    @Override
    public PageIterator<ConductScore> pageSearch(ConductScore conductScore, int page, int pageSize, String order) {
        return null;  
    }
}
