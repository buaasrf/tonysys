/**
 * 
 */
package com.tonysys.admin.model;

import java.util.Date;


/**
 * 操行分 
 * 
 * @author yangwm Oct 6, 2011 11:01:51 AM
 */
public class ConductScore{
    /**
     * 
     */
    public static final String tablename="conduct_score";
    public static final String ID="id";
    public static final String TYPE="type";
    public static final String NUMBER="number";
    public static final String NAME="name";
    public static final String GRADE="grade";
    public static final String SCORE="score";
    public static final String TIME="time";
    public static final String PLACE ="place";
    public static final String REMARK="remark";
    public static final String DESCRITION="descrition";
    public static final String UPDATEBY="updateBy";
    public static final String UPDATEDATE="updateDate";
    public static final String CREATEBY="createBy";
    public static final String CREATEDATE="createDate";

    private static final long serialVersionUID = 4914051393292204381L;
    private long id;
    private String type;// 出操/内务/考勤 :drill, housekeeping, attendance, 
    private String number;// 学号/工号 
    private String name;// 姓名  
    private String grade;// 班级  
    private int score;// 分数   
    private Date time;//日期时间
    private String place;//地点
    private String remark;// 备注
    private UserBean user; //学生
    
    /** 
     * type
     */
    public static class Type {
        public static final String DRILL = "drill";
        public static final String HOUSE_KEEPING = "housekeeping";
        public static final String ATTENDANCE = "attendance";
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("ConductScore{");
        sb.append(id);
        sb.append(",");
        sb.append(type);
        sb.append(",");
        sb.append(number);
        sb.append(",");
        sb.append(score);
        sb.append(",");

        sb.append(super.toString());
        sb.append("}");
        return sb.toString();
    }

    
    public long getId() {
        return id;
    }
    public void setId(long id) {
        this.id = id;
    }
    public String getType() {
        return type;
    }
    public void setType(String type) {
        this.type = type;
    }
    public String getNumber() {
        return number;
    }
    public void setNumber(String number) {
        this.number = number;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getGrade() {
        return grade;
    }
    public void setGrade(String grade) {
        this.grade = grade;
    }
    public int getScore() {
        return score;
    }
    public void setScore(int score) {
        this.score = score;
    }
    public Date getTime() {
        return time;
    }
    public void setTime(Date time) {
        this.time = time;
    }
    public String getPlace() {
        return place;
    }
    public void setPlace(String place) {
        this.place = place;
    }
    public String getRemark() {
        return remark;
    }
    public void setRemark(String remark) {
        this.remark = remark;
    }

    public UserBean getUser() {
        return user;
    }

    public void setUser(UserBean user) {
        this.user = user;
    }
}
