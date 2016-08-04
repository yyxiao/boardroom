from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Date,
    VARCHAR,
    DateTime,
    ForeignKey,
    CHAR,
    Numeric,
    Sequence,
)
from .meta import Base


class CapUser(Base):
    __tablename__ = 'cap_user'  # 用户信息表
    id = Column(Integer, Sequence('cap_user_id_seq', start=1000), primary_key=True)  # 用户主键id
    user_code = Column(VARCHAR(64), unique=True, nullable=False)  # 用户代码
    password = Column(VARCHAR(100))  # 密码，密文
    invalid_date = Column(Date)  # 密码失效时间
    user_name = Column(VARCHAR(64))  # 用户名
    auth_mode = Column(VARCHAR(255))  # 认证
    status = Column(VARCHAR(16))  # 状态
    unlock_time = Column(DateTime, nullable=False)  # 解锁时间
    menu_type = Column(VARCHAR(255))  # 菜单风格
    last_login = Column(DateTime, nullable=False)  # 最后登陆时间
    err_count = Column(Integer)  # 密码输错次数
    start_date = Column(Date)  # 有效开始日期
    end_date = Column(Date)  # 有效截止日期
    valid_time = Column(VARCHAR(255))  # 操作时间范围
    mac_code = Column(Integer)  # MAC
    ip_address = Column(VARCHAR(128))  # IP地址
    email = Column(VARCHAR(255))  # 邮箱地址
    create_by = Column(VARCHAR(64))  # 创建人
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改人
    update_time = Column(DateTime)  # 修改时间
    pwd_change_time = Column(DateTime)  # 密码修改时间

Index('user_code', CapUser.user_code, unique=True)


class CapRole(Base):
    __tablename__ = 'cap_role'  # 角色信息表
    role_id = Column(Integer, Sequence('cap_role_role_id_seq', start=1000), primary_key=True)  # 角色id
    role_code = Column(VARCHAR(64), nullable=False, unique=True)  # 角色代码
    role_name = Column(VARCHAR(64))  # 角色中文名
    role_desc = Column(VARCHAR(255))  # 角色描述
    create_by = Column(VARCHAR(64))  # 创建用户
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改用户
    update_time = Column(DateTime)  # 修改时间

Index('role_code', CapRole.role_code, unique=True)


class CapPartyAuth(Base):
    __tablename__ = 'cap_party_auth'  # 用户角色关联表
    party_type = Column(VARCHAR(64), nullable=False, primary_key=True)  # 参与者类型（user：表示用户）
    party_code = Column(VARCHAR(64), nullable=False, primary_key=True)  # 参与者代码
    role_type = Column(VARCHAR(64), nullable=False, primary_key=True)  # 角色类型（role）
    role_code = Column(VARCHAR(64), nullable=False, primary_key=True)  # 角色代码
    create_by = Column(VARCHAR(64))  # 创建人
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改人
    update_time = Column(DateTime)  # 修改时间


class HasMenu(Base):
    __tablename__ = 'has_menu'  # 菜单信息表
    id = Column(Integer, Sequence('has_menu_id_seq', start=1000), primary_key=True)  # 菜单id
    name = Column(VARCHAR(30))  # 菜单名称
    is_parent = Column(CHAR(1))  # 是否父节点(1-是;0-否)(或者菜单组)
    parent_id = Column(Integer)  # 父菜单id
    sort_index = Column(Integer)  # 索引号
    target = Column(VARCHAR(500))  # 目标模块
    url = Column(VARCHAR(500))  # 菜单url
    active_flag = Column(CHAR(1), server_default='1')  # 有效状态
    create_by = Column(VARCHAR(64))  # 创建人
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改人
    update_time = Column(DateTime)  # 修改时间
    version = Column(CHAR(1), server_default='1')  # 版本
    icon_name = Column(VARCHAR(100), nullable=False)  # 图表名称

Index('id', HasMenu.id, unique=True)  # 索引为id


class HasMenuOpt(Base):
    __tablename__ = 'has_menu_opt'  # 操作菜单表
    opt_id = Column(Integer, Sequence('has_menu_opt_opt_id_seq', start=10000), primary_key=True)  # 菜单id
    opt_name = Column(VARCHAR(30), nullable=False)  # 操作名称
    menu_id = Column(Integer, nullable=False)  # 菜单id
    active_flag = Column(CHAR(1), server_default='1')  # 有效时间
    create_by = Column(VARCHAR(64))  # 创建人
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改人
    update_time = Column(DateTime)  # 修改时间
    version = Column(CHAR(1), server_default='1')  # 版本
    icon_name = Column(VARCHAR(100), nullable=False)  # 图标名称


class HasPrivilege(Base):
    __tablename__ = 'has_privilege'  # 权限分配表
    id = Column(Integer, Sequence('has_privilege_id_seq', start=100), primary_key=True)  # id
    party_type = Column(VARCHAR(8), nullable=False)  # 参与者
    party_code = Column(VARCHAR(64), nullable=False)  # 参与者代码
    privilege = Column(VARCHAR(8), nullable=False)  # 权限（menu，opt）
    privilege_id = Column(Integer, nullable=False)  # 权限代码
    active_flag = Column(CHAR(1), server_default='1')  # 有效状态
    create_by = Column(VARCHAR(64))  # 创建人
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 修改人代码
    update_time = Column(DateTime)  # 修改时间


class HasLog(Base):
    __tablename__ = 'has_log'  # 系统日志表
    id = Column(Integer, Sequence('has_log_id_seq'), primary_key=True)  # id
    content = Column(Text)  # 操作内容
    module = Column(VARCHAR(100), nullable=False)  # 操作模块
    user_code = Column(VARCHAR(64), nullable=False)  # 用户代码
    create_time = Column(DateTime, nullable=False)  # 创建时间
    version = Column(CHAR(1), server_default='1')  # 版本


class OrgEmployee(Base):
    __tablename__ = 'org_employee'  # 员工表
    emp_id = Column(Integer, Sequence('org_employee_emp_id_seq', start=1000), primary_key=True)  # 员工主键id
    emp_code = Column(VARCHAR(64), nullable=False)  # 员工代码（同user_id）
    operator_id = Column(Integer)   # 用户主键id
    user_code = Column(VARCHAR(64))  # 用户代码
    name = Column(VARCHAR(50))  # 员工姓名
    name_en = Column(VARCHAR(50))  # 员工姓名（英文）
    gender = Column(VARCHAR(2))  # 性别
    birthday = Column(Date)  # 出生日期
    position_id = Column(Integer)  # 员工岗位
    status = Column(VARCHAR(255))   # 人员状态
    card_type = Column(VARCHAR(255))    # 证件类型
    card_no = Column(VARCHAR(32))   # 证件号码
    in_date = Column(Date)  # 入职日期
    out_date = Column(Date)  # 离职日期
    otel = Column(VARCHAR(12))  # 办公室电话
    oaddress = Column(VARCHAR(255))  # 办公地址
    ozipcode = Column(VARCHAR(10))  # 办公室邮编
    omeail = Column(VARCHAR(128))  # 办公室邮件
    faxno = Column(VARCHAR(14))  # 传真号码
    mobile = Column(VARCHAR(14))  # 手机号码
    qq = Column(VARCHAR(16))  # qq号
    htel = Column(VARCHAR(12))  # 家庭电话
    haddress = Column(VARCHAR(128))  # 家庭地址
    hzipcode = Column(VARCHAR(10))  # 家庭邮编
    pemail = Column(VARCHAR(128))  # 私人邮箱
    party = Column(VARCHAR(255))  # 政治面貌
    degree = Column(VARCHAR(255))  # 职级
    major = Column(VARCHAR(20))  # 直接主管
    specialty = Column(VARCHAR(1024))  # 可管理角色
    work_desc = Column(VARCHAR(512))  # 工作描述
    reg_date = Column(Date)  # 注册日期
    create_by = Column(VARCHAR(64))  # 创建人代码
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 更新人代码
    update_time = Column(DateTime)  # 更新时间
    org_id_list = Column(VARCHAR(128))  # 可管理机构
    org_id = Column(VARCHAR(10))  # 所属机构编号
    bak = Column(VARCHAR(512))  # 备注
    app_id = Column(VARCHAR(64))  # 应用id
    weibo = Column(VARCHAR(255))  # 微博


Index('emp_code', OrgEmployee.emp_code, unique=True)


# 员工机构表
class OrgEmpOrg(Base):
    __tablename__ = 'org_emp_org'
    id = Column(Integer, Sequence('org_emp_org_id_seq', start=1000), primary_key=True)  # id
    org_id = Column(Integer)  # 机构ID
    emp_id = Column(Integer)  # 员工主键ID
    is_main = Column(VARCHAR(1))  # 是否主机构
    app_id = Column(VARCHAR(64))  # 应用ID


# 机构表
class OrgOrganization(Base):
    __tablename__ = 'org_organization'
    org_id = Column(Integer, Sequence('org_organization_org_id_seq', start=1000), primary_key=True)  # 机构id
    org_code = Column(VARCHAR(32))  # 机构代码
    org_name = Column(VARCHAR(64))  # 机构名称
    org_level = Column(VARCHAR(2))  # 机构级别
    org_degree = Column(VARCHAR(255))  # 机构等级
    org_seq = Column(VARCHAR(512))  # 序列号
    org_type = Column(VARCHAR(12))  # 机构类型
    org_addr = Column(VARCHAR(256))  # 机构地址
    zipcode = Column(VARCHAR(10))  # 邮编
    manager_position = Column(VARCHAR(10))  # 机构主管岗位
    manager_id = Column(VARCHAR(20))  # 机构主管编号
    org_manager = Column(VARCHAR(128))  # 机构主管
    link_man = Column(VARCHAR(30))  # 联系人
    link_tel = Column(VARCHAR(20))  # 联系电话
    email = Column(VARCHAR(255))  # 电子邮件
    web_url = Column(VARCHAR(512))  # 网站地址
    start_date = Column(Date)  # 生效日期
    end_date = Column(Date)  # 失效日期
    status = Column(VARCHAR(255))  # 机构状态
    area = Column(VARCHAR(30))  # 所属地域
    create_by = Column(VARCHAR(64))  # 创建人代码
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 更新人代码
    update_time = Column(DateTime)  # 更新时间
    sort_index = Column(Integer)  # 排列顺序
    is_leaf = Column(VARCHAR(1))  # 是否是叶子节点
    sub_count = Column(Integer)  # 子节点个数
    remark = Column(VARCHAR(512))  # 备注
    app_id = Column(VARCHAR(64))  # 应用id
    parent_id = Column(Integer)  # 上级机构id


Index('org_code', OrgOrganization.org_code, unique=True)


# 岗位表
class OrgPosition(Base):
    __tablename__ = 'org_position'
    position_id = Column(Integer, Sequence('org_position_position_id_seq', start=1000), primary_key=True)  # 岗位编号
    position_code = Column(VARCHAR(20), unique=True)  # 岗位代码
    position_name = Column(VARCHAR(128))  # 岗位名称
    position_level = Column(VARCHAR(2))  # 岗位级别
    position_seq = Column(VARCHAR(512))  # 岗位序列号
    position_type = Column(VARCHAR(255))  # 岗位类型
    create_by = Column(VARCHAR(64))  # 创建人代码
    create_time = Column(DateTime)  # 创建时间
    update_by = Column(VARCHAR(64))  # 更新人代码
    update_time = Column(DateTime)  # 更新时间
    start_date = Column(Date)  # 生效时间
    end_date = Column(Date)  # 失效时间
    status = Column(VARCHAR(255))  # 岗位状态
    is_leaf = Column(VARCHAR(1))  # 是否为叶子节点
    sub_count = Column(Integer)  # 子节点个数
    app_id = Column(VARCHAR(64))  # 应用id
    duty_id = Column(VARCHAR(10))  # 职务编号
    org_id = Column(Integer)  # 所属机构id
    mana_posi = Column(Integer)  # 副岗位


Index('position_code', OrgPosition.position_code, unique=True)







