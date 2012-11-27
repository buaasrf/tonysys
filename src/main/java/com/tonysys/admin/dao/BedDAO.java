package com.tonysys.admin.dao;

import com.tonysys.admin.model.Bed;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-28
 * Time: 上午1:12
 * To change this template use File | Settings | File Templates.
 */
public interface BedDAO {
    Bed getBedByID(Integer id);
    Bed getBedByUserID(Integer userID);
    Bed getBedByDormitoryID(Integer dormitoryID);

}
