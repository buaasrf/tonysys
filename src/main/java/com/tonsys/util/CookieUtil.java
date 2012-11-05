package com.tonsys.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Created with IntelliJ IDEA.
 * User: ruifeng.sun
 * Date: 12-11-2
 * Time: 上午11:33
 * To change this template use File | Settings | File Templates.
 */
public class CookieUtil {
    private static final Logger log = LoggerFactory.getLogger(CookieUtil.class);
    public static Cookie getCookie(HttpServletRequest request, String key) {
        if (request.getCookies() == null) {
            return null;
        }
        for (Cookie c : request.getCookies()) {
            if (c.getName().equals(key)) {
                return c;
            }
        }
        return null;
    }

    public static boolean writeCookie(HttpServletResponse response, String name, String value, String domain, int time) {
        if (domain == null) {
            throw new IllegalArgumentException("please get value from config for domains.root");
        }

        try {
            Cookie cookie = new Cookie(name, value);
            cookie.setPath("/");
            if (!domain.equals("localhost")) {
                cookie.setDomain(domain);
            }
            if (time > 0) {
                cookie.setMaxAge(time);
            }
            response.addCookie(cookie);
            return true;
        } catch (Exception e) {
            log.error("write cookie(" + name + ":" + value + ") error:" + e.getMessage());
            return false;
        }
    }
    public static void deleteCookie(HttpServletRequest request, HttpServletResponse response, String name) {
        deleteCookie(request,response, null, name);
    }

    public static void deleteCookie(HttpServletRequest request, HttpServletResponse response, String domain, String name) {
        if (domain == null) {
            throw new IllegalArgumentException("please get value from config for domains.root");
        }
        Cookie cookie = null;
        if (request.getCookies() != null) {
            for (Cookie c : request.getCookies()) {
                if (c.getName().equals(name)) {
                    c.setValue(null);
                    c.setMaxAge(0);
                    if (!domain.equals("localhost")) {
                        c.setDomain(domain);
                    }
                    c.setPath("/");
                    cookie = c;
                }
            }
        }
        if (cookie != null) {
            response.addCookie(cookie);
        }
    }
}
