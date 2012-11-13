package com.tonysys.util;

import org.codehaus.jackson.map.ObjectMapper;
import org.springframework.web.servlet.view.json.MappingJacksonJsonView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;

/**
 * Created with IntelliJ IDEA.
 * User: hxb
 * Date: 12-7-20
 * Time: 下午4:43
 * To change this template use File | Settings | File Templates.
 */
public class MappingJacksonJsonpView extends MappingJacksonJsonView {
    public static final String DEFAULT_CONTENT_TYPE = "application/javascript";

    public static final String PARAM_NAME = "callback";

    public MappingJacksonJsonpView() {
        super();
        super.setContentType(DEFAULT_CONTENT_TYPE);
    }

    @Override
    protected void renderMergedOutputModel(Map<String, Object> model, HttpServletRequest request, HttpServletResponse response) throws Exception {
        if (request.getParameterMap().containsKey(PARAM_NAME)) {
            String functionName = request.getParameterValues(PARAM_NAME)[0];
            response.getOutputStream().write((functionName + "(").getBytes());
            super.renderMergedOutputModel(model, request, response);
            response.getOutputStream().write(");".getBytes());
        } else {
            super.renderMergedOutputModel(model, request, response);
        }
    }

    @Override
    public void setObjectMapper(ObjectMapper objectMapper) {
        super.setObjectMapper(objectMapper);
    }
}
