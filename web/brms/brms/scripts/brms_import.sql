-- 用户初始化
INSERT INTO "brms"."sys_user" ("id", "user_account", "user_pwd", "user_no", "user_name", "max_period", "email", "phone", "address", "user_type", "err_count", "unlock_time", "sex", "nation", "birthday", "position", "create_time", "create_user", "update_time", "org_id", "state") VALUES (1, 'sysadmin', 'MDAwMDAw', '', '超级管理员', 30, 'sysadmin@chyjr.com', '', '', 0, 0, now(), NULL, NULL, NULL, '超级管理员', NULL, NULL, NULL, 1, 1);
INSERT INTO "brms"."sys_user" ("id", "user_account", "user_pwd", "user_no", "user_name", "max_period", "email", "phone", "address", "user_type", "err_count", "unlock_time", "sex", "nation", "birthday", "position", "create_time", "create_user", "update_time", "org_id", "state") VALUES (2, 'jingyh', 'MDAwMDAw', '', 'jingyh', 30, 'sysadmin@chyjr.com', '', '', 0, 0, now(), NULL, NULL, NULL, '系统管理员', NULL, NULL, NULL, 1, 1);
INSERT INTO "brms"."sys_user" ("id", "user_account", "user_pwd", "user_no", "user_name", "max_period", "email", "phone", "address", "user_type", "err_count", "unlock_time", "sex", "nation", "birthday", "position", "create_time", "create_user", "update_time", "org_id", "state") VALUES (3, 'wuyr', 'MDAwMDAw', '', 'wuyr', 30, 'sysadmin@chyjr.com', '', '', 0, 0, now(), NULL, NULL, NULL, '系统管理员', NULL, NULL, NULL, 1, 1);
SELECT SETVAL('brms.sys_user_id_seq', 4, false);

-- 机构初始化
INSERT INTO "brms"."sys_org" ("id", "org_name", "org_type", "parent_id", "org_manager", "phone", "address", "org_seq", "state", "create_time", "create_user", "update_time") VALUES ('1', '海银金控', '0', '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
SELECT SETVAL('brms.sys_org_id_seq', 2, false);

-- 用户机构初始化
INSERT INTO "brms"."sys_user_org" ("user_id", "org_id", "create_time", "create_user") VALUES (1, 1, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_user_org" ("user_id", "org_id", "create_time", "create_user") VALUES (2, 1, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_user_org" ("user_id", "org_id", "create_time", "create_user") VALUES (3, 1, '2016-08-31 13:36:39', '1');

-- 角色初始化
INSERT INTO "brms"."sys_role" ("role_id", "role_name", "role_desc", "create_time", "create_user") VALUES (1, '超级管理员', '超级管理员', '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role" ("role_id", "role_name", "role_desc", "create_time", "create_user") VALUES (2, '系统管理员', '系统管理员', '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role" ("role_id", "role_name", "role_desc", "create_time", "create_user") VALUES (3, '普通用户', '普通用户', '2016-08-31 13:36:39', '1');
SELECT SETVAL('brms.sys_role_id_seq', 4, false);

-- 用户角色初始化
INSERT INTO "brms"."sys_user_role" ("role_id", "user_id", "create_time", "create_user") VALUES (1, 1, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_user_role" ("role_id", "user_id", "create_time", "create_user") VALUES (2, 2, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_user_role" ("role_id", "user_id", "create_time", "create_user") VALUES (2, 3, '2016-08-31 13:36:39', '1');

-- 角色菜单初始化
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 1, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 2, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 3, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 4, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 5, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 6, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (1, 7, '2016-08-31 13:36:39', '1');

INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 1, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 2, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 4, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 5, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 6, '2016-08-31 13:36:39', '1');
INSERT INTO "brms"."sys_role_menu" ("role_id", "menu_id", "create_time", "create_user") VALUES (2, 7, '2016-08-31 13:36:39', '1');


-- 菜单初始化
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (1, '用户管理', NULL, NULL, '/user/to_user', 'fa fa-user', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (2, '机构管理', NULL, NULL, '/org/to_org', 'fa fa-sitemap', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (3, '角色管理', NULL, NULL, '/role/to_role', 'fa fa-group', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (4, '授权管理', NULL, NULL, '/auth/to_auth', 'fa fa-unlock-alt', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (5, '会议室管理', NULL, NULL, '/boardroom/to_boardroom', 'fa fa-home', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (6, '终端管理', NULL, NULL, '/terminal/to_terminal', 'fa fa-apple', NULL, NULL, NULL);
INSERT INTO "brms"."sys_menu" ("id", "name", "parent_id", "target", "url", "icon_name", "sort_index", "create_time", "create_user") VALUES (7, '会议管理', NULL, NULL, '/meeting/to_meeting', 'fa fa-leaf', NULL, NULL, NULL);
SELECT SETVAL('brms.sys_menu_id_seq', 8, false);
