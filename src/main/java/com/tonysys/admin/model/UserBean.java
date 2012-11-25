/**
 * 
 */
package com.tonysys.admin.model;

import com.tonysys.context.UserType;

import java.util.Date;

/**
 * 
 * 科技系： 学年   学期  年级  院(系)/部  专业  班级  学制  学号  姓名  性别  出生日期    身份证号    考生号 籍贯  培养层次        更正  签名
 * 科技系教师：系(教研室)/研究室/实验室/科室    工号  姓名  性别  出生日期    学历  学位  职称  岗位  是否在岗    联系电话    电子邮箱 
 * 学生模板：入学年份 学号  姓名  班级  在校状态    学籍状态    招生季节    入学日期    性别  民族  籍贯  出生日期    身份证号    考生号 准考证号    政治面貌    培养层次    培养类别    培养对象    办学形式    曾用名 姓名拼音    入党团日期   生源省份    毕业中学    地区代码    联系地址    联系人 邮政编码    联系电话    WHCD_ID 入学成绩    入学方式    考生类别    档案行号    档案页号    办学类型    科类代码    WYYZDM  特长  电子信箱    出生地 学习形式    考生特征    GATDM_ID    辅修年级    辅修专业    学习年限    ZXWYJBMC    JSJDJ   录取专业    STUDTYPE    XJLB_ID1    户籍类别    毕业类别    健康状况    备注
 * 
 * @author yangwm Sep 10, 2011 9:19:01 PM
 */
public class UserBean {
    /**
     * 
     */
    public static final String TABLENAME="user";
    public static final String ID="id";
    public static final String TYPE="type";
    public static final String NUMBER="number";
    public static final String PASSWORD="password";
    public static final String NAME="name";
    public static final String DEPT="dept";
    public static final String TRAININGLEVEL="trainingLevel";
    public static final String SUBJECT="subject";
    public static final String GRADE="grade";
    public static final String STATE="state";
    public static final String GENDER="gender";
    public static final String NATION="nation";
    public static final String PROVINCE="province";
    public static final String BIRTH="birth";
    public static final String IDNUMBER="idNumber";
    public static final String CANDIDATENUMBER="candidateNumber";
    public static final String EXAMNUMBER="examNumber";
    public static final String POLITICSSTATUS="politicsStatus";
    public static final String EMAIL="email";
    public static final String PHONE="phone";
    public static final String HOMEPHONE="homePhone";
    public static final String REMARK="remark";
    public static final String FATHERNAME="fatherName";
    public static final String FATHERPHONE="fatherPhone";
    public static final String MOTHERNAME="motherName";
    public static final String MOTHERPHONE="motherPhone";
    public static final String DESCRITION="descrition";
    public static final String UPDATEBY="updateBy";
    public static final String UPDATEDATE="updateDate";
    public static final String CREATEBY="createBy";
    public static final String CREATEDATE="createDate";
    public static final String DORMITORYID="dormitoryid";

    private static final long serialVersionUID = -7558233566805685694L;
    
    private long id;
    private String type;// 用户类别（不同权限）-- student, 军体部长,劳生部长,纪检部长, teacher, admin, root
    private String number;// 学号/工号 
    private String password;// 密码 
    private String name;// 姓名  
    private String dept;// 院(系)/部
    private String trainingLevel;// 培养层次
    private String subject;// 专业
    private String grade;// 班级  
    private String state;// 状态      
    private String gender;// 性别  
    private String nation;// 民族  
    private String province;// 籍贯 
    private String birth;// 出生日期    
    private String idNumber;// 身份证号    
    private String candidateNumber;// 考生号 
    private String examNumber;// 准考证号    
    private String politicsStatus;// 政治面貌  
    private String email;// 电子邮箱     
    private String phone;// 联系电话
    private String homePhone;// 家庭电话 
    private String remark;// 备注 
    private String descrition;// 描述  
    
    private String fatherName;// 父亲姓名  
    private String fatherPhone;// 联系电话  
    private String motherName;// 母亲姓名  
    private String motherPhone;// 联系电话

    private String updateBy;
    private Date updateDate;
    private String createBy;
    private Date createDate;

    private Dormitory dormitory;//学生所在宿舍
    private UserType userType;
    @Override
    public boolean equals(Object obj) {
        if (null == obj) {
            return false;
        }
        if (this == obj) {
            return true;
        }
        if (!(obj instanceof UserBean)) {
            return false;
        }
        UserBean bean = (UserBean) obj;
        return number.equals(bean.getNumber());
    }

    @Override
    public int hashCode() {
        int result = 17;
        if(number != null) {
            result = 37 * result + number.hashCode();
        }
        return result;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("UserBean{");
        sb.append(id);
        sb.append(",");
        sb.append(number);
        sb.append(",");
        sb.append(name);
        sb.append(",");

        sb.append(super.toString());
        sb.append("}");
        return sb.toString();
    }

    
    public long getId() {
        return id;
    }
    public void setId(long id) {
        this.id = id;
    }
    public String getType() {
        return type;
    }
    public void setType(String type) {
        this.type = type;
    }
    public String getNumber() {
        return number;
    }
    public void setNumber(String number) {
        this.number = number;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getDept() {
        return dept;
    }
    public void setDept(String dept) {
        this.dept = dept;
    }
    public String getTrainingLevel() {
        return trainingLevel;
    }
    public void setTrainingLevel(String trainingLevel) {
        this.trainingLevel = trainingLevel;
    }
    public String getSubject() {
        return subject;
    }
    public void setSubject(String subject) {
        this.subject = subject;
    }
    public String getGrade() {
        return grade;
    }
    public void setGrade(String grade) {
        this.grade = grade;
    }
    public String getState() {
        return state;
    }
    public void setState(String state) {
        this.state = state;
    }
    public String getGender() {
        return gender;
    }
    public void setGender(String gender) {
        this.gender = gender;
    }
    public String getNation() {
        return nation;
    }
    public void setNation(String nation) {
        this.nation = nation;
    }
    public String getProvince() {
        return province;
    }
    public void setProvince(String province) {
        this.province = province;
    }
    public String getBirth() {
        return birth;
    }
    public void setBirth(String birth) {
        this.birth = birth;
    }
    public String getIdNumber() {
        return idNumber;
    }
    public void setIdNumber(String idNumber) {
        this.idNumber = idNumber;
    }
    public String getCandidateNumber() {
        return candidateNumber;
    }
    public void setCandidateNumber(String candidateNumber) {
        this.candidateNumber = candidateNumber;
    }
    public String getExamNumber() {
        return examNumber;
    }
    public void setExamNumber(String examNumber) {
        this.examNumber = examNumber;
    }
    public String getPoliticsStatus() {
        return politicsStatus;
    }
    public void setPoliticsStatus(String politicsStatus) {
        this.politicsStatus = politicsStatus;
    }
    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public String getPhone() {
        return phone;
    }
    public void setPhone(String phone) {
        this.phone = phone;
    }
    public String getHomePhone() {
        return homePhone;
    }
    public void setHomePhone(String homePhone) {
        this.homePhone = homePhone;
    }
    public String getRemark() {
        return remark;
    }
    public void setRemark(String remark) {
        this.remark = remark;
    }
    public String getDescrition() {
        return descrition;
    }
    public void setDescrition(String descrition) {
        this.descrition = descrition;
    }
    public String getFatherName() {
        return fatherName;
    }
    public void setFatherName(String fatherName) {
        this.fatherName = fatherName;
    }
    public String getFatherPhone() {
        return fatherPhone;
    }
    public void setFatherPhone(String fatherPhone) {
        this.fatherPhone = fatherPhone;
    }
    public String getMotherName() {
        return motherName;
    }
    public void setMotherName(String motherName) {
        this.motherName = motherName;
    }
    public String getMotherPhone() {
        return motherPhone;
    }
    public void setMotherPhone(String motherPhone) {
        this.motherPhone = motherPhone;
    }

    public String getUpdateBy() {
        return updateBy;
    }

    public void setUpdateBy(String updateBy) {
        this.updateBy = updateBy;
    }

    public Date getUpdateDate() {
        return updateDate;
    }

    public void setUpdateDate(Date updateDate) {
        this.updateDate = updateDate;
    }

    public String getCreateBy() {
        return createBy;
    }

    public void setCreateBy(String createBy) {
        this.createBy = createBy;
    }

    public Date getCreateDate() {
        return createDate;
    }

    public void setCreateDate(Date createDate) {
        this.createDate = createDate;
    }

    public Dormitory getDormitory() {
        return dormitory;
    }

    public void setDormitory(Dormitory dormitory) {
        this.dormitory = dormitory;
    }

    public UserType getUserType() {
        return userType;
    }

    public void setUserType(UserType userType) {
        this.userType = userType;
    }
}
