package com.tonysys.admin.rowMapper;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.UserBean;
import com.tonysys.context.UserState;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

/**
 * 宿舍实体和数据库表的转换类
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午2:31
 * To change this template use File | Settings | File Templates.
 */
@Repository("dormitoryRowMapper")
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
        dormitory.setTel(resultSet.getString(Dormitory.TEL));
        dormitory.setState(UserState.STU_ZC.getColor());
        if(dormitoryDAO!=null){
            List<UserBean> userBeanList = dormitoryDAO.getUserByDormitoryID(dormitory.getId());
            int state=UserState.STU_ZC.getKey();
            for(UserBean userBean:userBeanList){
                if(userBean.getState()>state){
                    state=userBean.getState();
                    dormitory.setState(UserState.getUserState(userBean.getState()).getColor());
                }
            }
        }
//        dormitory.setUserList(dormitoryDAO.getUserByDormitoryID(dormitory.getId()));
        return dormitory;
    }
}
