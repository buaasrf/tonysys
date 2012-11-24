package com.tonysys.util;

import com.alibaba.fastjson.serializer.SerializerFeature;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-24
 * Time: 下午5:13
 * To change this template use File | Settings | File Templates.
 */
public class FastJsonHelper {
    public static final SerializerFeature[] features = {
            SerializerFeature.WriteDateUseDateFormat,
            SerializerFeature.WriteMapNullValue, // 输出空置字段
            SerializerFeature.WriteNullListAsEmpty, // list字段如果为null，输出为[]，而不是null
            SerializerFeature.WriteNullNumberAsZero, // 数值字段如果为null，输出为0，而不是null
            SerializerFeature.WriteNullBooleanAsFalse, // Boolean字段如果为null，输出为false，而不是null
            SerializerFeature.WriteNullStringAsEmpty // 字符类型字段如果为null，输出为""，而不是null
    };
}
