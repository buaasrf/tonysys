package com.tonysys.admin.model;

import java.util.List;

/**
 * 宿舍信息实体类
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-17
 * Time: 下午12:21
 * To change this template use File | Settings | File Templates.
 */
public class Dormitory {
    /*************** 定义宿舍表及其属性名称********************************/
    public static final String TABLENAME="dormitory";
    public static final String ID="id";
    public static final String BUILDING="building";
    public static final String ROOM="room";
    public static final String DOOR="door";
    public static final String BEDNUMBER="bednumber";
    public static final String TEL="tel";
    /*************************************************/
    private Integer id;
    private String building;
    private String room;
    private String door;
    private Integer bednumber;
    private String tel;
    private String state;
    private List<UserBean> userList;

    @Override
    public String toString() {
        return "Dormitory{" +
                "id=" + id +
                ", building='" + building + '\'' +
                ", room='" + room + '\'' +
                ", door='" + door + '\'' +
                ", bednumber=" + bednumber +
                '}';
    }

    public Dormitory() {
    }

    public Dormitory(Integer id, String building, String room, String door, Integer bednumber ,String tel) {
        this.id = id;
        this.building = building;
        this.room = room;
        this.door = door;
        this.bednumber = bednumber;
        this.tel=tel;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getBuilding() {
        return building;
    }

    public void setBuilding(String building) {
        this.building = building;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public String getDoor() {
        return door;
    }

    public void setDoor(String door) {
        this.door = door;
    }

    public Integer getBednumber() {
        return bednumber;
    }

    public void setBednumber(Integer bednumber) {
        this.bednumber = bednumber;
    }

    public String getTel() {
        return tel;
    }

    public void setTel(String tel) {
        this.tel = tel;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public List<UserBean> getUserList() {
        return userList;
    }

    public void setUserList(List<UserBean> userList) {
        this.userList = userList;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Dormitory)) return false;

        Dormitory dormitory = (Dormitory) o;

        if (building != null ? !building.equals(dormitory.building) : dormitory.building != null) return false;
        if (door != null ? !door.equals(dormitory.door) : dormitory.door != null) return false;
        if (room != null ? !room.equals(dormitory.room) : dormitory.room != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = id != null ? id.hashCode() : 0;
        result = 31 * result + (building != null ? building.hashCode() : 0);
        result = 31 * result + (room != null ? room.hashCode() : 0);
        result = 31 * result + (door != null ? door.hashCode() : 0);
        result = 31 * result + (bednumber != null ? bednumber.hashCode() : 0);
        return result;
    }
}
