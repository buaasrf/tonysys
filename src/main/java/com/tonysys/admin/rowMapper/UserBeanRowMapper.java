package com.tonysys.admin.rowMapper;

import com.tonysys.admin.dao.DormitoryDAO;
import com.tonysys.admin.model.Dormitory;
import com.tonysys.admin.model.UserBean;
import com.tonysys.context.UserType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午2:56
 * To change this template use File | Settings | File Templates.
 */
@Repository("userBeanRowMapper")
public class UserBeanRowMapper implements RowMapper<UserBean> {
    private  static  final Logger log = LoggerFactory.getLogger(UserBeanRowMapper.class);
    @Resource
    DormitoryDAO dormitoryDAO;

    public UserBeanRowMapper() {
    }
    public UserBeanRowMapper(DormitoryDAO dormitoryDAO) {
        this.dormitoryDAO = dormitoryDAO;
    }
    @Override
    public UserBean mapRow(ResultSet resultSet, int i) throws SQLException {
        log.info("开始根据result set 转换为UserBean");
        UserBean userBean = new UserBean();
        try
        {
            userBean.setId(resultSet.getInt(UserBean.ID));
            userBean.setType(resultSet.getString(UserBean.TYPE));
            userBean.setNumber(resultSet.getString(UserBean.NUMBER));
            userBean.setPassword(resultSet.getString(UserBean.PASSWORD));
            userBean.setName(resultSet.getString(UserBean.NAME));
            userBean.setDept(resultSet.getString(UserBean.DEPT));
            userBean.setTrainingLevel(resultSet.getString(UserBean.TRAININGLEVEL));
            userBean.setSubject(resultSet.getString(UserBean.SUBJECT));
            userBean.setGrade(resultSet.getString(UserBean.GRADE));
            userBean.setState(resultSet.getInt(UserBean.STATE));
            userBean.setGender(resultSet.getString(UserBean.GENDER));
            userBean.setNation(resultSet.getString(UserBean.NATION));
            userBean.setProvince(resultSet.getString(UserBean.PROVINCE));
            userBean.setBirth(resultSet.getString(UserBean.BIRTH));
            userBean.setIdNumber(resultSet.getString(UserBean.IDNUMBER));
            userBean.setCandidateNumber(resultSet.getString(UserBean.CANDIDATENUMBER));
            userBean.setExamNumber(resultSet.getString(UserBean.EXAMNUMBER));
            userBean.setPoliticsStatus(resultSet.getString(UserBean.POLITICSSTATUS));
            userBean.setEmail(resultSet.getString(UserBean.EMAIL));
            userBean.setPhone(resultSet.getString(UserBean.PHONE));
            userBean.setHomePhone(resultSet.getString(UserBean.HOMEPHONE));
            userBean.setRemark(resultSet.getString(UserBean.REMARK));
            userBean.setFatherName(resultSet.getString(UserBean.FATHERNAME));
            userBean.setFatherPhone(resultSet.getString(UserBean.FATHERPHONE));
            userBean.setHomePhone(resultSet.getString(UserBean.HOMEPHONE));
            userBean.setMotherName(resultSet.getString(UserBean.MOTHERNAME));
            userBean.setMotherPhone(resultSet.getString(UserBean.MOTHERPHONE));
            userBean.setDescrition(resultSet.getString(UserBean.DESCRITION));
            userBean.setUpdateBy(resultSet.getString(UserBean.UPDATEBY));
            userBean.setUpdateDate(resultSet.getDate(UserBean.UPDATEDATE));
            userBean.setCreateBy(resultSet.getString(UserBean.CREATEBY));
            userBean.setCreateDate(resultSet.getDate(UserBean.CREATEDATE));
            if(dormitoryDAO==null){
                log.info("dormitoryDAO 为空，无法正确获取学生的宿舍实体信息");
            }
            else {
                Integer dormitoryID = resultSet.getInt(UserBean.DORMITORYID);
                Dormitory dormitory = dormitoryDAO.getDormitoryByID(dormitoryID);
                userBean.setDormitory(dormitory);
            }
            userBean.setUserType(UserType.getUserType(userBean.getType()));
        }
        catch (Exception e)
        {
            e.printStackTrace();
            log.error(e.toString());
        }
        log.info("转换成功！");
        return userBean;
    }
}
