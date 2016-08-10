/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     2016/8/8 15:26:46                            */
/*==============================================================*/


drop table has_boardroom;

drop table has_meet_bdr;

drop table has_meeting;

drop table has_pad;

drop table sys_dict;

drop table sys_log;

drop table sys_menu;

drop table sys_org;

drop table sys_role;

drop table sys_role_menu;

drop table sys_user;

drop table sys_user_org;

drop table sys_user_role;

/*==============================================================*/
/* Table: has_boardroom                                         */
/*==============================================================*/
create table has_boardroom (
   id                   SERIAL               not null,
   name                 VARCHAR(128)         null,
   description          VARCHAR(512)         null,
   config               VARCHAR(512)         null,
   picture              VARCHAR(200)         null,
   pad_id             VARCHAR(60)          null,
   org_id               INT8                 null,
   type                 INT8                 null,
   create_time          VARCHAR(19)          null,
   create_user          INT8                 null,
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

comment on column has_boardroom.pad_id is
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
   org_id               INT8                 null,
   repeat               VARCHAR(3)           null,
   repeat_date          VARCHAR(200)         null,
   start_date           VARCHAR(10)          null,
   end_date             VARCHAR(10)          null,
   start_time           VARCHAR(5)           null,
   end_time             VARCHAR(5)           null,
   create_time          VARCHAR(19)          null,
   create_user          INT8                 null,
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
/* Table: has_pad                                               */
/*==============================================================*/
create table has_pad (
   id               SERIAL               not null,
   pad_code             VARCHAR(100)         null,
   org_id               INT8                 null,
   last_time            VARCHAR(19)          null,
   last_funct           VARCHAR(200)         null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table has_pad is
'终端设备表';

comment on column has_pad.id is
'终端ID';

comment on column has_pad.pad_code is
'终端编码';

comment on column has_pad.org_id is
'机构ID';

comment on column has_pad.last_time is
'最后通信时间';

comment on column has_pad.last_funct is
'最后通信方法';

comment on column has_pad.create_user is
'创建人';

comment on column has_pad.create_time is
'创建时间';

alter table has_pad
   add constraint PK_HAS_PAD primary key (id);

/*==============================================================*/
/* Table: sys_dict                                              */
/*==============================================================*/
create table sys_dict (
   id                   SERIAL               not null,
   dict_name            VARCHAR(128)         null,
   dict_type            INT8                 null,
   create_time          VARCHAR(19)          null,
   create_user          INT8                 null
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
/* Table: sys_log                                               */
/*==============================================================*/
create table sys_log (
   log_id               SERIAL               not null,
   log_type             VARCHAR(8)           null,
   log_content          TEXT                 null,
   deal_result          VARCHAR(20)          null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_log is
'系统日志表';

comment on column sys_log.log_id is
'日志ID';

comment on column sys_log.log_type is
'日志类型';

comment on column sys_log.log_content is
'日志内容';

comment on column sys_log.deal_result is
'处理结果';

comment on column sys_log.create_user is
'创建人';

comment on column sys_log.create_time is
'创建时间';

alter table sys_log
   add constraint PK_SYS_LOG primary key (log_id);

/*==============================================================*/
/* Table: sys_menu                                              */
/*==============================================================*/
create table sys_menu (
   id                   SERIAL               not null,
   name                 VARCHAR(40)          not null,
   parent_id            INT8                 null,
   target               VARCHAR(300)         null,
   url                  VARCHAR(300)         null,
   icon_name            VARCHAR(100)         null,
   sort_index           INT8                 null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_menu is
'菜单信息表';

comment on column sys_menu.id is
'权限ID';

comment on column sys_menu.name is
'会议室类型';

comment on column sys_menu.parent_id is
'父菜单ID';

alter table sys_menu
   add constraint PK_SYS_MENU primary key (id, name);

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
   org_seq              INT8                 null,
   state                VARCHAR(3)           null,
   create_time          VARCHAR(19)          null,
   create_user          INT8                 null,
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
/* Table: sys_role                                              */
/*==============================================================*/
create table sys_role (
   role_id              SERIAL               not null,
   role_name            VARCHAR(60)          null,
   role_desc            VARCHAR(512)         null,
   create_user          INT8                 null,
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
/* Table: sys_role_menu                                         */
/*==============================================================*/
create table sys_role_menu (
   role_id              INT8                 not null,
   menu_id              INT8                 not null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_role_menu is
'角色菜单关系表';

comment on column sys_role_menu.role_id is
'角色ID';

comment on column sys_role_menu.menu_id is
'菜单ID';

comment on column sys_role_menu.create_user is
'创建人';

comment on column sys_role_menu.create_time is
'创建时间';

alter table sys_role_menu
   add constraint PK_SYS_ROLE_MENU primary key (role_id, menu_id);

/*==============================================================*/
/* Table: sys_user                                              */
/*==============================================================*/
create table sys_user (
   id                   SERIAL               not null,
   user_account         VARCHAR(32)          null,
   user_pwd             VARCHAR(32)          null,
   user_no              VARCHAR(32)          null,
   user_name            VARCHAR(64)          null,
   max_period           INT8                 null,
   email                VARCHAR(50)          null,
   phone                VARCHAR(32)          null,
   address              VARCHAR(256)         null,
   user_type            INT8                 null,
   err_count            INT4                 null,
   unlock_time          TIMESTAMP            null,
   sex                  VARCHAR(32)          null,
   nation               VARCHAR(32)          null,
   birthday             VARCHAR(10)          null,
   "position"           VARCHAR(32)          null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null,
   update_time          VARCHAR(19)          null,
   org_id               INT8                 null,
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
/* Table: sys_user_org                                          */
/*==============================================================*/
create table sys_user_org (
   user_id              INT8                 not null,
   ord_id               INT8                 not null,
   create_user          INT8                 null,
   create_time          VARCHAR(19)          null
);

comment on table sys_user_org is
'用户机构关系表';

comment on column sys_user_org.user_id is
'角色ID';

comment on column sys_user_org.ord_id is
'机构ID';

comment on column sys_user_org.create_user is
'创建人';

comment on column sys_user_org.create_time is
'创建时间';

alter table sys_user_org
   add constraint PK_SYS_USER_ORG primary key (user_id, ord_id);

/*==============================================================*/
/* Table: sys_user_role                                         */
/*==============================================================*/
create table sys_user_role (
   role_id              INT8                 not null,
   user_id              INT8                 not null,
   create_user          INT8                 null,
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

