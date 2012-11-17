package com.tonysys.admin.rowMapper;

import com.tonysys.admin.model.UserBean;
import org.springframework.jdbc.core.RowMapper;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午2:56
 * To change this template use File | Settings | File Templates.
 */
public class UserBeanRowMapper implements RowMapper<UserBean> {
    @Override
    public UserBean mapRow(ResultSet resultSet, int i) throws SQLException {
        UserBean userBean = new UserBean();
        userBean.setId(resultSet.getInt(UserBean.ID));
        userBean.setBirth(resultSet.getString(UserBean.BIRTH));
        userBean.setCandidateNumber(resultSet.getString(UserBean.CANDIDATENUMBER));
        userBean.setDept(resultSet.getString(UserBean.DEPT));
        userBean.setDescrition(resultSet.getString(UserBean.DESCRITION));
        userBean.setEmail(resultSet.getString(UserBean.EMAIL));
        userBean.setExamNumber(resultSet.getString(UserBean.EXAMNUMBER));
        userBean.setFatherName(resultSet.getString(UserBean.FATHERNAME));
        userBean.setIdNumber(resultSet.getString(UserBean.IDNUMBER));
        userBean.setFatherPhone(resultSet.getString(UserBean.FATHERPHONE));
        userBean.setPhone(resultSet.getString(UserBean.PHONE));
        userBean.setGender(resultSet.getString(UserBean.GENDER));
        userBean.setRemark(resultSet.getString(UserBean.REMARK));
        userBean.setHomePhone(resultSet.getString(UserBean.HOMEPHONE));
        userBean.setMotherName(resultSet.getString(UserBean.MOTHERNAME));
        userBean.setMotherPhone(resultSet.getString(UserBean.MOTHERPHONE));
        userBean.setNation(resultSet.getString(UserBean.NATION));
        userBean.setPoliticsStatus(resultSet.getString(UserBean.POLITICSSTATUS));
        userBean.setSubject(resultSet.getString(UserBean.SUBJECT));
        userBean.setType(resultSet.getString(UserBean.TYPE));
        userBean.setGrade(resultSet.getString(UserBean.GRADE));
        userBean.setState(resultSet.getString(UserBean.STATE));
        userBean.setPassword(resultSet.getString(UserBean.PASSWORD));
        return userBean;
    }
}
