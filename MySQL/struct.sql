

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ----------------------------
-- Table structure for master_chat
-- ----------------------------
DROP TABLE IF EXISTS master_chat;
CREATE TABLE master_chat (
  id int NOT NULL AUTO_INCREMENT COMMENT 'Primary key ID',
  chat_id varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Chat identifier',
  title varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Chat title',
  user_id varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'User ID',
  created_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
  PRIMARY KEY (id) USING BTREE,
  UNIQUE INDEX idx_chat_id (chat_id) USING BTREE,
  INDEX idx_user_id (user_id) USING BTREE,
  CONSTRAINT master_chat_ibfk_1 FOREIGN KEY (user_id) REFERENCES user_info (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Master chat information' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for master_message
-- ----------------------------
DROP TABLE IF EXISTS master_message;
CREATE TABLE master_message (
  id int NOT NULL AUTO_INCREMENT COMMENT 'Primary key ID',
  role varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Message role (user/assistant)',
  content text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'Message content',
  web_reference text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'Web references',
  gene_reference text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'Gene references',
  user_id varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'User ID',
  chat_id varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Chat ID',
  created_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
  PRIMARY KEY (id) USING BTREE,
  INDEX idx_chat_id (chat_id) USING BTREE,
  INDEX idx_user_id (user_id) USING BTREE,
  CONSTRAINT master_message_ibfk_1 FOREIGN KEY (user_id) REFERENCES user_info (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Master message information' ROW_FORMAT = Dynamic;



-- ----------------------------
-- Table structure for email_code
-- ----------------------------
DROP TABLE IF EXISTS `email_code`;
CREATE TABLE `email_code`  (
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '邮箱',
  `code` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '编号',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '0:未使用  1:已使用',
  PRIMARY KEY (`email`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '邮箱验证码' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of email_code
-- ----------------------------
INSERT INTO `email_code` VALUES ('test@qq.com', '08531', '2023-01-15 17:45:44', 1);
INSERT INTO `email_code` VALUES ('test02@qq.com', '02758', '2023-01-16 09:38:44', 1);

-- ----------------------------
-- Table structure for forum_article
-- ----------------------------
DROP TABLE IF EXISTS `forum_article`;
CREATE TABLE `forum_article`  (
  `article_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章ID',
  `board_id` int NULL DEFAULT NULL COMMENT '板块ID',
  `board_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '板块名称',
  `p_board_id` int NULL DEFAULT NULL COMMENT '父级板块ID',
  `p_board_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '父板块名称',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `nick_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '昵称',
  `user_ip_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最后登录ip地址',
  `title` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `cover` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '封面',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '内容',
  `markdown_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'markdown内容',
  `editor_type` tinyint NOT NULL COMMENT '0:富文本编辑器 1:markdown编辑器',
  `summary` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '摘要',
  `post_time` datetime NOT NULL COMMENT '发布时间',
  `last_update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `read_count` int NULL DEFAULT 0 COMMENT '阅读数量',
  `good_count` int NULL DEFAULT 0 COMMENT '点赞数',
  `comment_count` int NULL DEFAULT 0 COMMENT '评论数',
  `top_type` tinyint NULL DEFAULT 0 COMMENT '0未置顶  1:已置顶',
  `attachment_type` tinyint NULL DEFAULT NULL COMMENT '0:没有附件  1:有附件',
  `status` tinyint NULL DEFAULT NULL COMMENT '-1已删除 0:待审核  1:已审核 ',
  PRIMARY KEY (`article_id`) USING BTREE,
  INDEX `idx_board_id`(`board_id`) USING BTREE,
  INDEX `idx_pboard_id`(`p_board_id`) USING BTREE,
  INDEX `idx_post_time`(`post_time`) USING BTREE,
  INDEX `idx_top_type`(`top_type`) USING BTREE,
  INDEX `idx_title`(`title`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文章信息' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for forum_article_attachment
-- ----------------------------
DROP TABLE IF EXISTS `forum_article_attachment`;
CREATE TABLE `forum_article_attachment`  (
  `file_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件ID',
  `article_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章ID',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户id',
  `file_size` bigint NULL DEFAULT NULL COMMENT '文件大小',
  `file_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `download_count` int NULL DEFAULT NULL COMMENT '下载次数',
  `file_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件路径',
  `file_type` tinyint NULL DEFAULT NULL COMMENT '文件类型',
  `integral` int NULL DEFAULT NULL COMMENT '下载所需积分',
  PRIMARY KEY (`file_id`) USING BTREE,
  INDEX `idx_article_id`(`article_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文件信息' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for forum_article_attachment_download
-- ----------------------------
DROP TABLE IF EXISTS `forum_article_attachment_download`;
CREATE TABLE `forum_article_attachment_download`  (
  `file_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件ID',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
  `article_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章ID',
  `download_count` int NULL DEFAULT 1 COMMENT '文件下载次数',
  PRIMARY KEY (`file_id`, `user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户附件下载' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of forum_article_attachment_download
-- ----------------------------

-- ----------------------------
-- Table structure for forum_board
-- ----------------------------
DROP TABLE IF EXISTS `forum_board`;
CREATE TABLE `forum_board`  (
  `board_id` int NOT NULL AUTO_INCREMENT COMMENT '板块ID',
  `p_board_id` int NULL DEFAULT NULL COMMENT '父级板块ID',
  `board_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '板块名',
  `cover` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '封面',
  `board_desc` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `sort` int NULL DEFAULT NULL COMMENT '排序',
  `post_type` tinyint(1) NULL DEFAULT 1 COMMENT '0:只允许管理员发帖 1:任何人可以发帖',
  PRIMARY KEY (`board_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10007 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文章板块信息' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for forum_comment
-- ----------------------------
DROP TABLE IF EXISTS `forum_comment`;
CREATE TABLE `forum_comment`  (
  `comment_id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `p_comment_id` int NULL DEFAULT NULL COMMENT '父级评论ID',
  `article_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章ID',
  `content` varchar(800) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '回复内容',
  `img_path` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图片',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `nick_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `user_ip_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户ip地址',
  `reply_user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '回复人ID',
  `reply_nick_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '回复人昵称',
  `top_type` tinyint NULL DEFAULT 0 COMMENT '0:未置顶  1:置顶',
  `post_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `good_count` int NULL DEFAULT 0 COMMENT 'good数量',
  `status` tinyint NULL DEFAULT NULL COMMENT '0:待审核  1:已审核',
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `idx_article_id`(`article_id`) USING BTREE,
  INDEX `idx_post_time`(`post_time`) USING BTREE,
  INDEX `idx_top`(`top_type`) USING BTREE,
  INDEX `idx_p_id`(`p_comment_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10006 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '评论' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for like_record
-- ----------------------------
DROP TABLE IF EXISTS `like_record`;
CREATE TABLE `like_record`  (
  `op_id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `op_type` tinyint NULL DEFAULT NULL COMMENT '操作类型0:文章点赞 1:评论点赞',
  `object_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主体ID',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `create_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `author_user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '主体作者ID',
  PRIMARY KEY (`op_id`) USING BTREE,
  UNIQUE INDEX `idx_key`(`object_id`, `user_id`, `op_type`) USING BTREE,
  INDEX `idx_user_id`(`user_id`, `op_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10000 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '点赞记录' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for sys_setting
-- ----------------------------
DROP TABLE IF EXISTS `sys_setting`;
CREATE TABLE `sys_setting`  (
  `code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '编号',
  `json_content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设置信息',
  PRIMARY KEY (`code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统设置信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `nick_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `sex` tinyint(1) NULL DEFAULT NULL COMMENT '0:女 1:男',
  `person_description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '个人描述',
  `join_time` datetime NULL DEFAULT NULL COMMENT '加入时间',
  `last_login_time` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最后登录IP',
  `last_login_ip_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最后登录ip地址',
  `total_integral` int NULL DEFAULT NULL COMMENT '积分',
  `current_integral` int NULL DEFAULT NULL COMMENT '当前积分',
  `status` tinyint NULL DEFAULT NULL COMMENT '0:禁用 1:正常',
  `is_admin` int NULL DEFAULT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `key_email`(`email`) USING BTREE,
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户信息' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for user_integral_record
-- ----------------------------
DROP TABLE IF EXISTS `user_integral_record`;
CREATE TABLE `user_integral_record`  (
  `record_id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户ID',
  `oper_type` tinyint NULL DEFAULT NULL COMMENT '操作类型',
  `integral` int NULL DEFAULT NULL COMMENT '积分',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`record_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10025 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户积分记录表' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for user_message
-- ----------------------------
DROP TABLE IF EXISTS `user_message`;
CREATE TABLE `user_message`  (
  `message_id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `received_user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '接收人用户ID',
  `article_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章ID',
  `article_title` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章标题',
  `comment_id` int NULL DEFAULT NULL COMMENT '评论ID',
  `send_user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发送人用户ID',
  `send_nick_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发送人昵称',
  `message_type` tinyint NULL DEFAULT NULL COMMENT '0:系统消息 1:评论 2:文章点赞  3:评论点赞 4:附件下载',
  `message_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '消息内容',
  `status` tinyint NULL DEFAULT NULL COMMENT '1:未读 2:已读',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`message_id`) USING BTREE,
  UNIQUE INDEX `idx_key`(`article_id`, `comment_id`, `send_user_id`, `message_type`) USING BTREE,
  INDEX `idx_received_user_id`(`received_user_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_type`(`message_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10004 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户消息' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
