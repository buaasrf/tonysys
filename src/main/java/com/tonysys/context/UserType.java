package com.tonysys.context;

import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * 用户权限类型
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-25
 * Time: 下午8:02
 * To change this template use File | Settings | File Templates.
 */
public enum UserType {
    /**
     * 学生
     */
    STUDENT("student","学生"),
    /**
     * 军体部长
     */
    STU_JT("stu_jt","军体部长"),
    /**
     * 劳生部长
     */
    STU_LS("stu_ls","劳生部长"),
    /**
     * 纪检部长
     */
    STU_JJ("stu_jj","纪检部长"),
    /**
     * 教师
     */
    TEACHER("teacher","教师"),
    /**
     * 管理员
     */
    ADMIN("admin","管理员"),
    /**
     * 超级管理员
     */
    ROOT("root","超级管理员");
    private UserType(String key,String value){
        this.key=key;
        this.value =value;
    }
    public String getValue(){
        return this.value;
    }
    public String getKey(){
        return this.key;
    }
    public boolean equal(UserType userType){
        return userType != null && userType.getKey().equals(this.getKey());
    }
    public static UserType getUserType(String key){
        if(StringUtils.isBlank(key)){
            return null;
        }
        if(key.equals(STUDENT.getKey())) return  STUDENT;
        else if(key.equals(STU_JJ.getKey()))  return STU_JJ;
        else if(key.equals(STU_JT.getKey()))  return STU_JT;
        else if(key.equals(STU_LS.getKey()))  return STU_LS;
        else if(key.equals(TEACHER.getKey()))  return TEACHER;
        else if(key.equals(ROOT.getKey()))  return ROOT;
        else if(key.equals(ADMIN.getKey()))  return ADMIN;
        else return null;
    }
    public static List<UserType> getAllUserType(){
        List<UserType> userTypeList = new ArrayList<UserType>();
        userTypeList.add(STUDENT);
        userTypeList.add(STU_JJ);
        userTypeList.add(STU_JT);
        userTypeList.add(STU_LS);
        userTypeList.add(TEACHER);
        userTypeList.add(ADMIN);
        userTypeList.add(ROOT);
        return userTypeList;
    }
    private String key;
    private String value;
}
