package com.tonysys.filter;

import com.tonysys.context.UserContext;
import com.tonysys.util.CookieUtil;
import com.tonysys.util.URLHelper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.StringUtils;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.net.URLDecoder;

/**
 * 用户登录过滤器，判断当前用户是否已经登录。
 * 参数包括（
 * excludeURL：不需要判断用户是否登录的url地址
 * notLoginURL：当用户没有登录时，跳转的url地址，默认为“/noLogin\S*”
 * 以上两个url都可以是带有正则表达式的地址，同时可以使用/ * * /，/ * /, / * * ,/ * 来匹配路径
 * ）
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-10-30
 * Time: 下午3:03
 * To change this template use File | Settings | File Templates.
 */
public class LoginFilter implements Filter {
    private final static Logger log = LoggerFactory.getLogger(LoginFilter.class);
    private String excludeURL;
    private String notLoginURL;
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        excludeURL=filterConfig.getInitParameter("excludeURL");
        notLoginURL=filterConfig.getInitParameter("notLoginURL");
        if(notLoginURL==null)
        {
            notLoginURL="/login.jsp";
        }
        if(log.isDebugEnabled())
        {
            log.debug("excludeURL:"+excludeURL);
            log.debug("notLoginURL:"+notLoginURL);
        }
    }

    /**
     * 用户登录过滤器，判断当前用户是否已经登录
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
        String decodeUri = URLDecoder.decode(requestUri,"UTF-8");
        HttpServletRequest req = (HttpServletRequest) request;

        //设置用户的当前访问的地址和上一个访问地址到session中
        String userRequestPreURL= (String) req.getSession().getAttribute(UserContext.USER_REQUEST_URL);
        if(userRequestPreURL!=null)
        {
            req.getSession().setAttribute(UserContext.USER_REQUEST_PRE_URL,userRequestPreURL);
        }
        req.getSession().setAttribute(UserContext.USER_REQUEST_URL,req.getRequestURL()+(req.getQueryString()==null?"":"?"+req.getQueryString()));


        log.info("user request uri:"+decodeUri);
        if(!URLHelper.checkURLs(excludeURL, decodeUri)&&!checkLogin(request,response))
        {
            log.info("user not login");
            ((HttpServletRequest)request).getRequestDispatcher(notLoginURL).forward(request,response);
        }
        chain.doFilter(request,response);

    }

    /**
     * 判断用户是否登录
     * 判断标准：查看当前用户的Cookie中是否存在用户token，
     * 如果存在说明当前用户已经登录过并且没有过期，
     * 如果存在则说明用户需要重新登录。
     * @param request
     * @param response
     * @return
     */
    private boolean checkLogin(ServletRequest request,ServletResponse response)
    {
        HttpServletRequest req = (HttpServletRequest) request;
        return req.getSession().getAttribute(UserContext.USER_ID)!=null;
    }
    @Override
    public void destroy() {
        
    }
}
