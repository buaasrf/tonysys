package com.tonsys.util;

import java.util.regex.Pattern;

/**
 * Created with IntelliJ IDEA.
 * User: ruifeng.sun
 * Date: 12-11-1
 * Time: 上午10:55
 * To change this template use File | Settings | File Templates.
 */
public class URLHelper {
    public static boolean checkPattern(String patternUrl,String input)
    {
        if(!hasText(patternUrl)&&!hasText(input))
        {
            return true;
        }
        if(!hasText(patternUrl)||!hasText(input))
        {
            return false;
        }
        patternUrl="^"+patternUrl+"$";
        String patternUrlStr = patternUrl.replace("/*/", "/[\\d|a-z|A-Z|?|=|_|$|%|&|*|#|(|)]+/")
                .replace("/**/", "/\\S+/")
                .replace("/**", "/\\S*")
                .replace("/*", "/[\\d|a-z|A-Z|?|=|_|$|%|&|*|#|(|)]*");

        Pattern pt = Pattern.compile(patternUrlStr);
        return  pt.matcher(input).find();
    }
    public static boolean checkURLs(String urls,String userRequestURL)
    {
        if(hasText(urls))
        {
            String [] urlArray = urls.split(",");
            for(String url:urlArray)
            {
                if(checkPattern(url,userRequestURL))
                {
                    return true;
                }
            }
        }
        return false;
    }
    public static boolean hasText(String input)
    {
        if(input==null||input.trim().length()==0)
        {
            return false;
        }
        return true;
    }
}
