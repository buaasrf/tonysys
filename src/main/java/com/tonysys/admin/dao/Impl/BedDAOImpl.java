package com.tonysys.admin.dao.Impl;

import com.tonysys.admin.dao.BedDAO;
import com.tonysys.admin.model.Bed;
import com.tonysys.admin.rowMapper.BedRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-28
 * Time: 上午1:13
 * To change this template use File | Settings | File Templates.
 */
@Repository("bedDAO")
public class BedDAOImpl implements BedDAO {
    @Resource
    JdbcTemplate tonysysJdbcTemplate;
    @Resource
    BedRowMapper bedRowMapper;
    @Override
    public Bed getBedByID(Integer id) {
        Bed bed =null;
        try{
            bed =tonysysJdbcTemplate.queryForObject("select * from bed where id =?",new Object[]{id},bedRowMapper);
        }
        catch (Exception e){
            e.printStackTrace();
        }
        return bed;
    }

    @Override
    public Bed getBedByUserID(Integer userID) {
        Bed bed =null;
        try{
            bed =tonysysJdbcTemplate.queryForObject("select * from bed where userid =?",new Object[]{userID},bedRowMapper);
        }
        catch (Exception e){
            e.printStackTrace();
        }
        return bed;
    }

    @Override
    public Bed getBedByDormitoryID(Integer dormitoryID) {
        Bed bed =null;
        try{
            bed =tonysysJdbcTemplate.queryForObject("select * from bed where dormitoryid =?",new Object[]{dormitoryID},bedRowMapper);
        }
        catch (Exception e){
            e.printStackTrace();
        }
        return bed;
    }
}
