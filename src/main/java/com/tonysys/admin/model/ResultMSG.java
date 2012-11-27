package com.tonysys.admin.model;

/**
 * Created with IntelliJ IDEA.
 * User: ruifeng.sun
 * Date: 12-11-23
 * Time: 上午10:48
 * To change this template use File | Settings | File Templates.
 */
public class ResultMSG {
    private String error;
    private Integer result;

    public ResultMSG() {
        this.result=0;
        error="";
    }

    public ResultMSG(String error, Integer result) {
        this.error = error;
        this.result = result;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public Integer getResult() {
        return result;
    }

    public void setResult(Integer result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "{\"result\":"+this.result+",\"error\":\""+this.error+"\"}";
    }
}
