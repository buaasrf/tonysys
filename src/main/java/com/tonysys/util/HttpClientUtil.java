package com.tonysys.util;

import org.apache.http.*;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.params.ConnManagerParams;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.SingleClientConnManager;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

/**
 * Created with IntelliJ IDEA.
 * User: tony
 * Date: 12-11-2
 * Time: 下午2:16
 * To change this template use File | Settings | File Templates.
 */
public class HttpClientUtil{
    private static final Logger logger = LoggerFactory.getLogger(HttpClientUtil.class);

    private static final int connectionTimeoutMillis = 300;
    private static final int socketTimeoutMillis = 1000;
    private static final int connManagerTimeout = 1000;
    private static final boolean singleClient = false;
    private static HttpParams params;

    static {
        params = new BasicHttpParams();
        HttpProtocolParams.setVersion(params, HttpVersion.HTTP_1_1);
        HttpConnectionParams.setConnectionTimeout(params, connectionTimeoutMillis);
        logger.debug("ThreadSafeClient connectionTimeoutMillis:{}", connectionTimeoutMillis);
        HttpConnectionParams.setSoTimeout(params, socketTimeoutMillis);
        logger.debug("ThreadSafeClient socketTimeoutMillis:{}", socketTimeoutMillis);
        ConnManagerParams.setTimeout(params, connManagerTimeout);
        logger.debug("ThreadSafeClient connManagerTimeout:{}", connManagerTimeout);
    }

    public static HttpClient getHttpClient() {
        return getHttpClient(params);
    }

    public static HttpClient getHttpClient(HttpParams params) {
        logger.debug("Begin getHttpClient");
        long s = System.currentTimeMillis();
        try {
            return new DefaultHttpClient(params);
        } finally {
            logger.debug("End getHttpClient single:{} spend:{}", singleClient, (System.currentTimeMillis() - s));
        }
    }

    public static String postWithJsonResponse(String url) {
        return postWithJsonResponse(url, null, "UTF-8");
    }

    public static String postWithJsonResponse(String url, String charset) {
        return postWithJsonResponse(url, null, charset);
    }

    public static String postWithJsonResponse(String url, Map<String, String> params) {
        return postWithJsonResponse(url, params, "UTF-8");
    }

    public static String postWithJsonResponse(String url, Map<String, String> params, String charset) {
        return postWithJsonResponse(getHttpClient(), url, params, charset);
    }

    public static String postWithJsonResponse(HttpClient httpClient, String url, Map<String, String> params, String charset) {
        if (httpClient == null) {
            throw new NullPointerException("httpClient is null.");
        }
        logger.info("Begin HttpClientUtil.postWithJsonResponse url:{} params:{} charset:{}", new Object[]{url, params, charset});
        String response = "{}";
        List<NameValuePair> paramList = null;
        if (params != null) {
            Set<Map.Entry<String, String>> entrySet = params.entrySet();
            paramList = new ArrayList<NameValuePair>();
            for (Iterator<Map.Entry<String, String>> it = entrySet.iterator(); it.hasNext(); ) {
                Map.Entry<String, String> entry = it.next();
                String key = entry.getKey();
                String value = entry.getValue();
                if (key != null && value != null) {
                    NameValuePair nvp = new BasicNameValuePair(key, value);
                    paramList.add(nvp);
                }
            }
        }

        HttpPost httpPost = null;
        try {
            httpPost = new HttpPost(url);
            if (paramList != null)
                httpPost.setEntity(new UrlEncodedFormEntity(paramList, charset));
            HttpResponse httpResponse = httpClient.execute(httpPost);
            HttpEntity httpEntity = httpResponse.getEntity();
            int statusCode = httpResponse.getStatusLine().getStatusCode();
            if (statusCode != HttpStatus.SC_OK) {
                logger.warn("Unable to fetch page {}, status code: {}", httpPost.getURI(), statusCode);
            } else {
                response = EntityUtils.toString(httpEntity, charset);
                response = (response != null ? response.trim() : "{}");
                logger.debug("Fetch page {}, status code: {}", httpPost.getURI(), statusCode);
            }
            if (httpEntity != null) {
                httpEntity.consumeContent();
            }
        } catch (Exception e) {
            logger.error("", e);
            if (httpPost != null) {
                httpPost.abort();
            }
        } finally {
            if (httpClient != null && httpClient.getConnectionManager() instanceof SingleClientConnManager) {
                httpClient.getConnectionManager().shutdown();
            }
        }
        logger.debug("Begin HttpClientUtil.postWithJsonResponse response:{}", response);
        return response;
    }

    public static String getWithJsonResponse(String url) {
        return getWithJsonResponse(url, null, "UTF-8");
    }

    public static String getWithCookiedJsonResponse(String url,String cookie) {
        return getWithCookiedJsonResponse(getHttpClient(), url, null, "UTF-8",cookie);
    }
    public static String getWithJsonResponse(String url, String charset) {
        return getWithJsonResponse(url, null, charset);
    }

    public static String getWithJsonResponse(String url, Map<String, String> params) {
        return getWithJsonResponse(url, params, "UTF-8");
    }

    public static String getWithJsonResponse(String url, Map<String, String> params, String charset) {
        return getWithJsonResponse(getHttpClient(), url, params, charset);
    }

    public static String getWithJsonResponse(HttpClient httpClient, String url, Map<String, String> params, String charset) {

        String response = "{}";
        if (httpClient == null) {
            logger.error("httpClient is null.");
            return response;
        }
        logger.info("Begin HttpClientUtil.getWithJsonResponse url:{} params:{} charset:{}", new Object[]{url, params, charset});
        HttpParams httpParams = new BasicHttpParams();
        if (params != null) {
            for (Iterator<Map.Entry<String, String>> it = params.entrySet().iterator(); it.hasNext(); ) {
                Map.Entry<String, String> entry = it.next();
                if (entry.getKey() != null && entry.getValue() != null) {
                    httpParams.setParameter(entry.getKey(), entry.getValue());
                }
            }
        }

        HttpGet httpGet = null;
        try {
            httpGet = new HttpGet(url);
            httpGet.setParams(httpParams);
            HttpResponse httpResponse = httpClient.execute(httpGet);
            HttpEntity httpEntity = httpResponse.getEntity();
            int statusCode = httpResponse.getStatusLine().getStatusCode();
            if (statusCode != HttpStatus.SC_OK) {
                logger.warn("Unable to fetch page {}, status code: {}", httpGet.getURI(), statusCode);
            } else {
                response = EntityUtils.toString(httpEntity, charset);
                response = (response != null ? response.trim() : "{}");
                logger.debug("Fetch page {}, status code: {}", httpGet.getURI(), statusCode);
            }
            if (httpEntity != null) {
                httpEntity.consumeContent();
            }
        } catch (Exception e) {
            logger.error("", e);
            if (httpGet != null) {
                httpGet.abort();
            }
        } finally {
            if (httpClient != null) {
                httpClient.getConnectionManager().shutdown();
            }
        }
        logger.debug("Begin HttpClientUtil.geEndJsonResponse response:{}", response);
        return response;
    }
    public static String getWithCookiedJsonResponse(HttpClient httpClient, String url, Map<String, String> params, String charset,String cookie) {

        String response = "{}";
        if (httpClient == null) {
            logger.error("httpClient is null.");
            return response;
        }
        logger.info("Begin HttpClientUtil.getWithJsonResponse url:{} params:{} charset:{}", new Object[]{url, params, charset});
        HttpParams httpParams = new BasicHttpParams();
        if (params != null) {
            for (Iterator<Map.Entry<String, String>> it = params.entrySet().iterator(); it.hasNext(); ) {
                Map.Entry<String, String> entry = it.next();
                if (entry.getKey() != null && entry.getValue() != null) {
                    httpParams.setParameter(entry.getKey(), entry.getValue());
                }
            }
        }

        HttpGet httpGet = null;
        try {
            httpGet = new HttpGet(url);
            httpGet.setParams(httpParams);
            httpGet.setHeader("Cookie",cookie);
            HttpResponse httpResponse = httpClient.execute(httpGet);
            HttpEntity httpEntity = httpResponse.getEntity();
            int statusCode = httpResponse.getStatusLine().getStatusCode();
            if (statusCode != HttpStatus.SC_OK) {
                logger.warn("Unable to fetch page {}, status code: {}", httpGet.getURI(), statusCode);
            } else {
                response = EntityUtils.toString(httpEntity, charset);
                response = (response != null ? response.trim() : "{}");
                logger.debug("Fetch page {}, status code: {}", httpGet.getURI(), statusCode);
            }
            if (httpEntity != null) {
                httpEntity.consumeContent();
            }
        } catch (Exception e) {
            logger.error("", e);
            if (httpGet != null) {
                httpGet.abort();
            }
        } finally {
            if (httpClient != null) {
                httpClient.getConnectionManager().shutdown();
            }
        }
        logger.debug("Begin HttpClientUtil.geEndJsonResponse response:{}", response);
        return response;
    }
}
