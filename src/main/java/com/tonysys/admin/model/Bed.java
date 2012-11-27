package com.tonysys.admin.model;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-28
 * Time: 上午1:03
 * To change this template use File | Settings | File Templates.
 */
public class Bed {
    private Integer id;
    private Integer userid;
    private Integer dormitoryid;

    public Bed() {
    }

    public Bed(Integer userid, Integer dormitoryid) {
        this.userid = userid;
        this.dormitoryid = dormitoryid;
    }

    public Bed(Integer id, Integer userid, Integer dormitoryid) {
        this.id = id;
        this.userid = userid;
        this.dormitoryid = dormitoryid;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUserid() {
        return userid;
    }

    public void setUserid(Integer userid) {
        this.userid = userid;
    }

    public Integer getDormitoryid() {
        return dormitoryid;
    }

    public void setDormitoryid(Integer dormitoryid) {
        this.dormitoryid = dormitoryid;
    }
}
