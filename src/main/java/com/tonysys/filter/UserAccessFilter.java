package com.tonysys.filter;

import com.tonysys.context.UserContext;
import com.tonysys.util.CookieUtil;
import com.tonysys.util.URLHelper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.StringUtils;

import javax.servlet.*;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.net.URLDecoder;
import java.util.List;

/**
 * 用户访问控制过滤器，用于控制用户访问当前请求的路径
 * 参数包括（
 * excludeURL：不进行访问控制的路径
 * doAuthURL：进行访问控制的路径，为空时表示控制除excludeURL以外的所有路径
 * noAuthURL：当用户没有权限访问当前路径时跳转的url地址，默认是“/noAuthURL\S*”
 * serverAddress：中央权限控制服务器获取用户权限数据的接口路径，用于获取用户的权限资源信息
 * 注：以上路径都可以是带有正则表达式的路径，同时可以使用／**／，／*／，/**,/*来匹配路径
 * ）
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-10-30
 * Time: 下午3:05
 * To change this template use File | Settings | File Templates.
 */
public class UserAccessFilter implements Filter {
    private Logger log = LoggerFactory.getLogger(UserAccessFilter.class);
    private String excludeURL;
    private String doAuthURL;
    private String noAuthURL;
    private String serverAddress;
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        excludeURL=filterConfig.getInitParameter("excludeURL");
        doAuthURL=filterConfig.getInitParameter("doAuthURL");
        noAuthURL=filterConfig.getInitParameter("noAuthURL");
        serverAddress=filterConfig.getInitParameter("serverAddress");
        if(noAuthURL==null)
        {
            noAuthURL="/noAuth.jsp";
        }
        if(serverAddress==null)
        {
            log.warn("server address is null can't get resource from server");
        }
    }

    /**
     * 过滤用户访问路径，对当前用户访问的路径进行访问控制
     * @param request
     * @param response
     * @param chain
     * @throws java.io.IOException
     * @throws javax.servlet.ServletException
     */
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        String servletPath=((HttpServletRequest)request).getServletPath();
        String queryString = ((HttpServletRequest)request).getQueryString();
        String requestUri = servletPath+ (StringUtils.hasText(queryString)?("?"+queryString):"");
        String decodeUri = URLDecoder.decode(requestUri, "UTF-8");
        HttpServletRequest req = (HttpServletRequest) request;

        log.info("user access url:"+decodeUri);
        if(URLHelper.checkURLs(excludeURL, decodeUri))
        {
           chain.doFilter(request,response);
        }

        //如果用户配置了过滤路径则，并且当前访问的路径在过滤路径中，并且用户没有权限访问当前路径则跳转到制定页面，其他情况继续执行
        //如果用没有配置过滤路径，并且当前用户没权限访问当前路径则跳转到制定页面，其他情况继续执行
        if(URLHelper.hasText(doAuthURL)){
            if(URLHelper.checkURLs(doAuthURL,decodeUri)){
                if(!doAccessCheck(req,decodeUri)){
                    log.info("user has no auth to access");
                    req.getRequestDispatcher(noAuthURL).forward(request,response);
                }
            }
        }
        else{
            if(!doAccessCheck(req,decodeUri)){
                log.info("user has no auth to access");
                req.getRequestDispatcher(noAuthURL).forward(request,response);
            }
        }
        log.info("user access into request url");
        chain.doFilter(request,response);
    }

    /**
     * 判断用户是否有访问当前路径的权限
     * 判断用户访问权限时首先获取用户session中的数据，如果用户用户session中已经没有数据则根据用户token
     * 去远程服务器获取当前用户的权限资源数据
     * @param req 当前HttpServletRequest
     * @param userRequestURI 用户请求的当前路径
     * @return
     */
    private boolean doAccessCheck(HttpServletRequest req,String userRequestURI)
    {
        List<String> resources = (List<String>) req.getSession().getAttribute(UserContext.USER_RESOURCE);
        if(resources==null)
        {
            Cookie userTokenCookie = CookieUtil.getCookie(req, UserContext.USER_TOKEN);
            String userToken = userTokenCookie==null?"":userTokenCookie.getValue();
            //String userResources = HttpClientUtil.getWithJsonResponse(serverAddress);
        }
        if(resources==null||resources.size()==0)
        {
            return false;
        }
        for(String url:resources)
        {
            if(URLHelper.checkPattern(url,userRequestURI))
            {
                return true;
            }
        }
        return false;
    }
    @Override
    public void destroy() {

    }
}
