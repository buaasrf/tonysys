package com.tonysys.admin.rowMapper;

import com.tonysys.admin.dao.DormitoryDAO;
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
    @Resource
    DormitoryDAO dormitoryDAO;
    @Override
    public UserBean mapRow(ResultSet resultSet, int i) throws SQLException {
        UserBean userBean = new UserBean();
        userBean.setId(resultSet.getInt(UserBean.ID));
        userBean.setType(resultSet.getString(UserBean.TYPE));
        userBean.setNumber(resultSet.getString(UserBean.NUMBER));
        userBean.setPassword(resultSet.getString(UserBean.PASSWORD));
        userBean.setName(resultSet.getString(UserBean.NAME));
        userBean.setDept(resultSet.getString(UserBean.DEPT));
        userBean.setTrainingLevel(resultSet.getString(UserBean.TRAININGLEVEL));
        userBean.setSubject(resultSet.getString(UserBean.SUBJECT));
        userBean.setGrade(resultSet.getString(UserBean.GRADE));
        userBean.setState(resultSet.getString(UserBean.STATE));
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
        userBean.setDormitory(dormitoryDAO.getDormitoryByID(resultSet.getInt(UserBean.DORMITORYID)));
        return userBean;
    }
}
