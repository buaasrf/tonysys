package com.tonysys.converter;

import org.springframework.http.HttpInputMessage;
import org.springframework.http.HttpOutputMessage;
import org.springframework.http.MediaType;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.util.FileCopyUtils;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;

/**
 * Created with IntelliJ IDEA.
 * User: hxb
 * Date: 12-7-16
 * Time: 上午10:20
 * To change this template use File | Settings | File Templates.
 */
public class UTF8StringHttpMessageConverter extends StringHttpMessageConverter {

    public static final Charset DEFAULT_CHARSET = Charset.forName("UTF-8");

    private boolean writeAcceptCharset = true;

    @Override
    protected String readInternal(Class clazz, HttpInputMessage inputMessage) throws IOException {
        MediaType contentType = inputMessage.getHeaders().getContentType();
        Charset charset = contentType.getCharSet() != null ? contentType.getCharSet() : DEFAULT_CHARSET;
        return FileCopyUtils.copyToString(new InputStreamReader(inputMessage.getBody(), charset));
    }

    @Override
    protected void writeInternal(String s, HttpOutputMessage outputMessage) throws IOException {
        if (this.writeAcceptCharset) {
            outputMessage.getHeaders().setAcceptCharset(getAcceptedCharsets());
        }
        MediaType contentType = outputMessage.getHeaders().getContentType();
        Charset charset = contentType.getCharSet() != null ? contentType.getCharSet() : DEFAULT_CHARSET;
        outputMessage.getHeaders().setContentType(new MediaType(contentType.getType(), contentType.getSubtype(), charset));
        FileCopyUtils.copy(s, new OutputStreamWriter(outputMessage.getBody(), charset));
    }

    public void setWriteAcceptCharset(boolean writeAcceptCharset) {
        super.setWriteAcceptCharset(writeAcceptCharset);
        this.writeAcceptCharset = writeAcceptCharset;
    }
}
