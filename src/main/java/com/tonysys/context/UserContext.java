package com.tonysys.context;


/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-10-31
 * Time: 下午2:24
 * To change this template use File | Settings | File Templates.
 */
public final class UserContext {
    /**
     * 当前用户访问的系统appid
     */
    public static final String APP_ID = "app_id";
    /**
     * 用户id
     */
    public static final String USER_ID="user_id";
    /**
     * 用户唯一编号
     */
    public static final String USER_NUMBER="user_number";
    /**
     * 用户名
     */
    public static final String USER_NAME="user_name";
    /**
     * 用户email
     */
    public static final String USER_EMAIL="user_email";
    /**
     * 用户权限级别
     */
    public static final String USER_PRIVILEGE="user_privilege";
    /**
     * 用户登录时间
     */
    public static final String LOGIN_TIME="login_time";
    /**
     * 用户资源列表
     */
    public static final String USER_RESOURCE="user_resource";
    /**
     * 用户身份标识
     */
    public static final String USER_TOKEN="user_token";
    /**
     * 用户当前请求的url地址
     */
    public static final String USER_REQUEST_URL="user_request_url";
    /**
     * 用户请求的上一个url地址
     */
    public static final String USER_REQUEST_PRE_URL="user_request_per_url";
}
