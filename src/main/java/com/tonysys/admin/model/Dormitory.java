package com.tonysys.admin.model;

/**
 * 宿舍信息实体类
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午12:21
 * To change this template use File | Settings | File Templates.
 */
public class Dormitory {
    private Integer id;
    private String building;
    private String room;
    private String door;
    private Integer bednumber;

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

    public Dormitory(Integer id, String building, String room, String door, Integer bednumber) {
        this.id = id;
        this.building = building;
        this.room = room;
        this.door = door;
        this.bednumber = bednumber;
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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Dormitory)) return false;

        Dormitory dormitory = (Dormitory) o;

        if (bednumber != null ? !bednumber.equals(dormitory.bednumber) : dormitory.bednumber != null) return false;
        if (building != null ? !building.equals(dormitory.building) : dormitory.building != null) return false;
        if (door != null ? !door.equals(dormitory.door) : dormitory.door != null) return false;
        if (id != null ? !id.equals(dormitory.id) : dormitory.id != null) return false;
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
