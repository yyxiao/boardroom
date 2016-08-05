from sqlalchemy import (
    Column,
    INT,
    VARCHAR,
    Sequence
)
from .meta import Base


BRMS_SCHEMA = 'brms'


class HasBoardroom(Base):
    __tablename__ = 'has_boardroom'             # 会议室表
    id = Column(INT, Sequence('has_boardroom_id_seq', schema=BRMS_SCHEMA), primary_key=True)   # 会议室ID
    name = Column(VARCHAR(128))                 # 会议室名称
    description = Column(VARCHAR(512))          # 会议室描述
    config = Column(VARCHAR(512))               # 会议室配置
    picture = Column(VARCHAR(200))              # 会议室照片
    pad_code = Column(VARCHAR(60))              # 绑定pad机器码
    org_id = Column(INT)                        # 所属机构id
    type = Column(INT)                          # 会议室类型
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人
    state = Column(VARCHAR(3))                  # 状态


class HasMeetBdr(Base):
    __tablename__ = 'has_meet_bdr'              # 会议会议室关系表
    meeting_id = Column(INT, primary_key=True)                           # 会议ID
    boardroom_id = Column(INT, primary_key=True)                         # 会议室ID
    create_user = Column(INT)                   # 创建人
    create_time = Column(VARCHAR(19))           # 创建时间


class HasMeeting(Base):
    __tablename__ = 'has_meeting'               # 会议表
    id = Column(INT, Sequence('has_meeting_id_seq', schema=BRMS_SCHEMA), primary_key=True)   # 会议ID
    name = Column(VARCHAR(128))                 # 会议名称
    description = Column(VARCHAR(512))          # 会议描述
    org_id = Column(INT)                        # 机构ID
    repeat = Column(VARCHAR(3))                 # 是否重复会议
    start_date = Column(VARCHAR(10))            # 开始日期
    end_date = Column(VARCHAR(10))              # 结束日期
    start_time = Column(VARCHAR(5))             # 开始时间
    end_time = Column(VARCHAR(5))               # 结束时间
    create_time = Column(VARCHAR(19))           # 创建时间
    create_uesr = Column(INT)                   # 创建人
    state = Column(VARCHAR(3))                  # 状态


class SysDict(Base):
    __tablename__ = 'sys_dict'                  # 字典表
    id = Column(INT, Sequence('sys_dict_id_seq', schema=BRMS_SCHEMA), primary_key=True)      # 字典ID
    dict_name = Column(VARCHAR(128))            # 字典名称
    dict_type = Column(VARCHAR(512))            # 字典类型
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人


class SysOrg(Base):
    __tablename__ = 'sys_org'                   # 机构表
    id = Column(INT, Sequence('sys_org_id_seq', schema=BRMS_SCHEMA), primary_key=True)      # 机构ID
    org_name = Column(VARCHAR(150))             # 机构名称
    org_type = Column(VARCHAR(3))               # 机构类型
    parent_id = Column(INT)                     # 上级机构
    org_manager = Column(VARCHAR(64))           # 法人
    phone = Column(VARCHAR(32))                 # 电话
    address = Column(VARCHAR(256))              # 地址
    org_seq = Column(INT)                       # 排序
    state = Column(VARCHAR(3))                  # 状态
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人
    update_time = Column(VARCHAR(19))           # 更新时间


class SysPerBrtype(Base):
    __tablename__ = 'sys_per_brtype'            # 权限会议室类型关系表
    per_id = Column(INT, primary_key=True)                                 # 权限ID
    boardroom_type = Column(INT, primary_key=True)                         # 会议室类型
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人


class SysPermission(Base):
    __tablename__ = 'sys_permission'            # 权限表
    id = Column(INT, Sequence('sys_permission_id_seq', schema=BRMS_SCHEMA), primary_key=True)  # 权限ID
    permission_name = Column(VARCHAR(128))      # 权限名称
    permission_desc = Column(VARCHAR(512))      # 权限描述
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人
    state = Column(VARCHAR(3))                  # 状态


class SysRole(Base):
    __tablename__ = 'sys_role'                  # 角色表
    role_id = Column(INT, Sequence('sys_role_id_seq', schema=BRMS_SCHEMA), primary_key=True)   # 角色ID
    role_name = Column(VARCHAR(60))             # 角色名称
    role_desc = Column(VARCHAR(512))            # 角色描述
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人


class SysRolePermission(Base):
    __tablename__ = 'sys_role_permission'       # 角色权限关系表
    role_id = Column(INT, primary_key=True)     # 角色ID
    per_id = Column(INT, primary_key=True)      # 权限ID
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人


class SysUser(Base):
    __tablename__ = 'sys_user'                  # 用户表
    id = Column(INT, Sequence('sys_user_id_seq', schema=BRMS_SCHEMA), primary_key=True)        # 用户ID
    user_account = Column(VARCHAR(32))          # 用户帐号
    user_pwd = Column(VARCHAR(32))              # 用户密码
    user_no = Column(VARCHAR(32))               # 用户工号
    user_name = Column(VARCHAR(64))             # 用户名称
    max_period = Column(INT)                    # 预约最大期限
    email = Column(VARCHAR(50))                 # 邮件
    phone = Column(VARCHAR(32))                 # 联系电话
    address = Column(VARCHAR(256))              # 联系地址
    user_type = Column(INT)                     # 用户类型
    gender = Column(INT)                        # 性别
    nation = Column(VARCHAR(32))                # 民族
    birthday = Column(VARCHAR(10))              # 出生日期
    position = Column(VARCHAR(32))              # 职位
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人
    update_time = Column(VARCHAR(19))           # 修改时间
    org_id = Column(INT)                        # 所属机构
    state = Column(VARCHAR(3))                  # 状态


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'             # 用户角色关系表
    role_id = Column(INT, primary_key=True)     # 角色ID
    user_id = Column(INT, primary_key=True)     # 用户ID
    create_time = Column(VARCHAR(19))           # 创建时间
    create_user = Column(INT)                   # 创建人

