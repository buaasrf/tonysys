package com.tonysys.context;

import java.util.ArrayList;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: ruifeng.sun
 * Date: 12-11-27
 * Time: 下午1:46
 * To change this template use File | Settings | File Templates.
 */
public enum UserState {
    STU_WJ(4,"违纪","error"),
    STU_LJ(3,"留级","warning"),
    STU_QT(2,"其他","info"),
    STU_ZC(1,"正常","success");
    private UserState(Integer key,String value,String color){
        this.key=key;
        this.value=value;
        this.color=color;
    }
    public static UserState getUserState(Integer key){
        if(key.equals(STU_LJ.getKey()))return STU_LJ;
        else if(key.equals(STU_WJ.getKey())) return STU_WJ;
        else if(key.equals(STU_QT.getKey())) return STU_QT;
        else if(key.equals(STU_ZC.getKey())) return STU_ZC;
        else return null;
    }
    public static List<UserState> getAllState(){
        List<UserState> userStateList = new ArrayList<UserState>();
        userStateList.add(STU_WJ);
        userStateList.add(STU_LJ);
        userStateList.add(STU_QT);
        userStateList.add(STU_ZC);
        return userStateList;
    }
    public Integer getKey() {
        return key;
    }

    public String getValue() {
        return value;
    }

    public String getColor() {
        return color;
    }

    private Integer key;
    private String value;
    private String color;
}
