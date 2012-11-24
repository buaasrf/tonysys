package com.tonysys.admin.rowMapper;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * 宿舍实体和数据库表的转换类
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午2:31
 * To change this template use File | Settings | File Templates.
 */
@Repository
public class DormitoryRowMapper implements RowMapper<Dormitory> {
    @Resource
    DormitoryDAO dormitoryDAO;
    @Override
    public Dormitory mapRow(ResultSet resultSet, int i) throws SQLException {
        Dormitory dormitory = new Dormitory();
        dormitory.setId(resultSet.getInt(Dormitory.ID));
        dormitory.setBuilding(resultSet.getString(Dormitory.BUILDING));
        dormitory.setRoom(resultSet.getString(Dormitory.ROOM));
        dormitory.setDoor(resultSet.getString(Dormitory.DOOR));
        dormitory.setBednumber(resultSet.getInt(Dormitory.BEDNUMBER));
//        dormitory.setUserList(dormitoryDAO.getUserByDormitoryID(dormitory.getId()));
        return dormitory;
    }
}
