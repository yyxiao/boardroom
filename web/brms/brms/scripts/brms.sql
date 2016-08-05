/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     2016/8/5 10:47:44                            */
/*==============================================================*/


drop table brms.has_boardroom;

drop table brms.has_meet_bdr;

drop table brms.has_meeting;

drop table brms.sys_dict;

drop table brms.sys_org;

drop table brms.sys_per_brtype;

drop table brms.sys_permission;

drop table brms.sys_role;

drop table brms.sys_role_permission;

drop table brms.sys_user;

drop table brms.sys_user_role;

/*==============================================================*/
/* Table: has_boardroom                                         */
/*==============================================================*/
create table has_boardroom (
   id                   SERIAL               not null,
   name                 VARCHAR(128)         null,
   description          VARCHAR(512)         null,
   config               VARCHAR(512)         null,
   picture              VARCHAR(200)         null,
   pad_code             VARCHAR(60)          null,
   org_id               INT4                 null,
   type                 INT4                 null,
   create_time          VARCHAR(19)          null,
   create_user          INT4                 null,
   state                VARCHAR(3)           null
);

comment on table has_boardroom is
'会议室表';

comment on column has_boardroom.id is
'会议室ID';

comment on column has_boardroom.name is
'会议室名称';

comment on column has_boardroom.description is
'会议室描述';

comment on column has_boardroom.config is
'配置';

comment on column has_boardroom.picture is
'会议室图片';

comment on column has_boardroom.pad_code is
'设备编号';

comment on column has_boardroom.org_id is
'机构';

comment on column has_boardroom.type is
'类型';

comment on column has_boardroom.create_time is
'创建时间';

comment on column has_boardroom.state is
'状态';

alter table has_boardroom
   add constraint PK_HAS_BOARDROOM primary key (id);

/*==============================================================*/
/* Table: has_meet_bdr                                          */
/*==============================================================*/
create table has_meet_bdr (
   meeting_id           INT8                 not null,
   boardroom_id         INT8                 not null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table has_meet_bdr is
'会议会议室关系表';

comment on column has_meet_bdr.meeting_id is
'会议室ID';

comment on column has_meet_bdr.boardroom_id is
'会议ID';

alter table has_meet_bdr
   add constraint PK_HAS_MEET_BDR primary key (meeting_id, boardroom_id);

/*==============================================================*/
/* Table: has_meeting                                           */
/*==============================================================*/
create table has_meeting (
   id                   SERIAL               not null,
   name                 VARCHAR(128)         null,
   description          VARCHAR(512)         null,
   org_id               INT4                 null,
   repeat               VARCHAR(3)           null,
   start_date           VARCHAR(10)          null,
   end_date             VARCHAR(10)          null,
   start_time           VARCHAR(5)           null,
   end_time             VARCHAR(5)           null,
   create_time          VARCHAR(19)          null,
   create_user          INT4                 null,
   state                VARCHAR(3)           null
);

comment on table has_meeting is
'会议表';

comment on column has_meeting.id is
'会议ID';

comment on column has_meeting.name is
'会议名称';

comment on column has_meeting.description is
'滚动文字';

comment on column has_meeting.org_id is
'机构';

comment on column has_meeting.repeat is
'是否重复';

comment on column has_meeting.start_date is
'开始日期';

comment on column has_meeting.end_date is
'结束日期';

comment on column has_meeting.start_time is
'开始时间';

comment on column has_meeting.end_time is
'结束时间';

comment on column has_meeting.create_time is
'创建时间';

comment on column has_meeting.state is
'状态';

alter table has_meeting
   add constraint PK_HAS_MEETING primary key (id);

/*==============================================================*/
/* Table: sys_dict                                              */
/*==============================================================*/
create table sys_dict (
   id                   SERIAL               not null,
   dict_name            VARCHAR(128)         null,
   dict_type            VARCHAR(512)         null,
   create_time          VARCHAR(19)          null,
   create_user          INT4                 null
);

comment on table sys_dict is
'字典表';

comment on column sys_dict.id is
'字典ID';

comment on column sys_dict.dict_name is
'字典名称';

comment on column sys_dict.dict_type is
'字典类型';

comment on column sys_dict.create_time is
'创建时间';

alter table sys_dict
   add constraint PK_SYS_DICT primary key (id);

/*==============================================================*/
/* Table: sys_org                                               */
/*==============================================================*/
create table sys_org (
   id                   SERIAL               not null,
   org_name             VARCHAR(150)         null,
   org_type             VARCHAR(3)           null,
   parent_id            VARCHAR(32)          null,
   org_manager          VARCHAR(64)          null,
   phone                VARCHAR(30)          null,
   address              VARCHAR(256)         null,
   org_seq              INT4                 null,
   state                VARCHAR(3)           null,
   create_time          VARCHAR(19)          null,
   create_user          INT4                 null,
   update_time          VARCHAR(19)          null
);

comment on table sys_org is
'机构表';

comment on column sys_org.id is
'机构ID';

comment on column sys_org.org_name is
'机构名称';

comment on column sys_org.org_type is
'机构类型';

comment on column sys_org.parent_id is
'父机构编号';

comment on column sys_org.org_manager is
'法人';

comment on column sys_org.address is
'地址';

comment on column sys_org.org_seq is
'排序';

comment on column sys_org.state is
'状态';

comment on column sys_org.create_time is
'创建时间';

alter table sys_org
   add constraint PK_SYS_ORG primary key (id);

/*==============================================================*/
/* Table: sys_per_brtype                                        */
/*==============================================================*/
create table sys_per_brtype (
   per_id               INT4                 not null,
   boardroom_type       INT4                 not null,
   create_user          INT4                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_per_brtype is
'权限会议室类型关系表';

comment on column sys_per_brtype.per_id is
'权限ID';

comment on column sys_per_brtype.boardroom_type is
'会议室类型';

alter table sys_per_brtype
   add constraint PK_SYS_PER_BRTYPE primary key (per_id, boardroom_type);

/*==============================================================*/
/* Table: sys_permission                                        */
/*==============================================================*/
create table sys_permission (
   id                   SERIAL               not null,
   permission_name      VARCHAR(128)         null,
   permission_desc      VARCHAR(512)         null,
   create_time          VARCHAR(19)          null,
   create_user          INT4                 null,
   state                VARCHAR(3)           null
);

comment on table sys_permission is
'权限表';

comment on column sys_permission.id is
'权限ID';

comment on column sys_permission.permission_name is
'权限名称';

comment on column sys_permission.permission_desc is
'权限描述';

comment on column sys_permission.create_time is
'创建时间';

comment on column sys_permission.create_user is
'创建者';

comment on column sys_permission.state is
'状态';

alter table sys_permission
   add constraint PK_SYS_PERMISSION primary key (id);

/*==============================================================*/
/* Table: sys_role                                              */
/*==============================================================*/
create table sys_role (
   role_id              SERIAL               not null,
   role_name            VARCHAR(60)          null,
   role_desc            VARCHAR(512)         null,
   create_user          INT4                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_role is
'系统角色表';

comment on column sys_role.role_id is
'角色ID';

comment on column sys_role.role_name is
'角色名称';

comment on column sys_role.role_desc is
'角色描述';

comment on column sys_role.create_user is
'创建人';

comment on column sys_role.create_time is
'创建时间';

alter table sys_role
   add constraint PK_SYS_ROLE primary key (role_id);

/*==============================================================*/
/* Table: sys_role_permission                                   */
/*==============================================================*/
create table sys_role_permission (
   role_id              INT4                 not null,
   per_id               INT4                 not null,
   create_user          INT4                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_role_permission is
'角色权限关系表';

comment on column sys_role_permission.role_id is
'角色ID';

comment on column sys_role_permission.per_id is
'权限ID';

comment on column sys_role_permission.create_user is
'创建人';

comment on column sys_role_permission.create_time is
'创建时间';

alter table sys_role_permission
   add constraint PK_SYS_ROLE_PERMISSION primary key (role_id, per_id);

/*==============================================================*/
/* Table: sys_user                                              */
/*==============================================================*/
create table sys_user (
   id                   SERIAL               not null,
   user_account         VARCHAR(32)          null,
   user_pwd             VARCHAR(32)          null,
   user_no              VARCHAR(32)          null,
   user_name            VARCHAR(64)          null,
   max_period           INT4                 null,
   email                VARCHAR(50)          null,
   phone                VARCHAR(32)          null,
   address              VARCHAR(256)         null,
   user_type            INT4                 null,
   sex                  VARCHAR(32)          null,
   nation               VARCHAR(32)          null,
   birthday             VARCHAR(10)          null,
   "position"           VARCHAR(32)          null,
   create_user          INT4                 null,
   create_time          VARCHAR(19)          null,
   update_time          VARCHAR(19)          null,
   org_id               INT4                 null,
   state                VARCHAR(3)           null
);

comment on table sys_user is
'用户表';

comment on column sys_user.id is
'用户ID';

comment on column sys_user.user_account is
'用户帐号';

comment on column sys_user.user_pwd is
'用户密码';

comment on column sys_user.user_no is
'工号';

comment on column sys_user.user_name is
'用户姓名';

comment on column sys_user.max_period is
'最大期限';

comment on column sys_user.email is
'邮箱地址';

comment on column sys_user.phone is
'联系电话';

comment on column sys_user.address is
'联系地址';

comment on column sys_user.user_type is
'用户类型';

comment on column sys_user.sex is
'性别';

comment on column sys_user.nation is
'民族';

comment on column sys_user.birthday is
'出生日期';

comment on column sys_user."position" is
'职业';

comment on column sys_user.create_user is
'创建人';

comment on column sys_user.create_time is
'创建时间';

comment on column sys_user.update_time is
'修改时间';

comment on column sys_user.org_id is
'机构ID';

comment on column sys_user.state is
'状态';

alter table sys_user
   add constraint PK_SYS_USER primary key (id);

/*==============================================================*/
/* Table: sys_user_role                                         */
/*==============================================================*/
create table sys_user_role (
   role_id              INT4                 not null,
   user_id              INT4                 not null,
   create_user          INT4                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_user_role is
'用户角色关系表';

comment on column sys_user_role.role_id is
'角色ID';

comment on column sys_user_role.user_id is
'用户ID';

comment on column sys_user_role.create_user is
'创建人';

comment on column sys_user_role.create_time is
'创建时间';

alter table sys_user_role
   add constraint PK_SYS_USER_ROLE primary key (role_id, user_id);

