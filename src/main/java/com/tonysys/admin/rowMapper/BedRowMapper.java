package com.tonysys.admin.rowMapper;

import com.tonysys.admin.model.Bed;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-28
 * Time: 上午1:07
 * To change this template use File | Settings | File Templates.
 */
@Repository("bedRowMapper")
public class BedRowMapper implements RowMapper<Bed> {
    @Override
    public Bed mapRow(ResultSet resultSet, int i) throws SQLException {
        Bed bed = new Bed();
        bed.setId(resultSet.getInt("id"));
        bed.setDormitoryid(resultSet.getInt("dormitoryid"));
        bed.setUserid(resultSet.getInt("userid"));
        return bed;
    }
}
