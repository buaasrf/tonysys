package com.tonysys.admin.rowMapper;

import com.tonysys.admin.dao.UserDAO;
import com.tonysys.admin.model.ConductScore;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Created with IntelliJ IDEA.
 * User: sunruifeng
 * Date: 12-11-17
 * Time: 下午3:08
 * To change this template use File | Settings | File Templates.
 */
@Repository
public class ConductScoreRowMapper implements RowMapper<ConductScore> {
    @Resource
    UserDAO userDAO;
    @Override
    public ConductScore mapRow(ResultSet resultSet, int i) throws SQLException {
        ConductScore conductScore = new ConductScore();
        conductScore.setId(resultSet.getInt(ConductScore.ID));
        conductScore.setType(resultSet.getString(ConductScore.TYPE));
        conductScore.setNumber(resultSet.getString(ConductScore.NUMBER));
        conductScore.setName(resultSet.getString(ConductScore.NAME));
        conductScore.setGrade(resultSet.getString(ConductScore.GRADE));
        conductScore.setScore(resultSet.getInt(ConductScore.SCORE));
        conductScore.setTime(resultSet.getDate(ConductScore.TIME));
        conductScore.setPlace(resultSet.getString(ConductScore.PLACE));
        conductScore.setRemark(resultSet.getString(ConductScore.REMARK));
        conductScore.setDescription(resultSet.getString(ConductScore.DESCRIPTION));
        conductScore.setUpdateBy(resultSet.getString(ConductScore.UPDATEBY));
        conductScore.setUpdateDate(resultSet.getDate(ConductScore.UPDATEDATE));
        conductScore.setCreateBy(resultSet.getString(ConductScore.CREATEBY));
        conductScore.setCreateDate(resultSet.getDate(ConductScore.CREATEDATE));
        conductScore.setUser(userDAO.getUserByNumber(conductScore.getNumber()));
        return conductScore;
    }
}
