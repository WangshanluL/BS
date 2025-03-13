以下是数据库中各个表的结构描述：
表master_chat
chat_id,title,master_user_id
表master_message

### 1. `chat` 表
- **字段**:
  - `user_id` (varchar(255)): 用户ID，主键。
  - `chatMessages` (text): 聊天消息内容。
- **约束**:
  - 主键: `user_id`。
  - 外键: `user_id` 引用 `user_info` 表的 `user_id`。

### 2. `email_code` 表
- **字段**:
  - `email` (varchar(150)): 邮箱，主键。
  - `code` (varchar(5)): 验证码，主键。
  - `create_time` (datetime): 创建时间。
  - `status` (tinyint): 状态（0:未使用，1:已使用）。
- **约束**:
  - 主键: `email`, `code`。

### 3. `forum_article` 表
- **字段**:
  - `article_id` (varchar(15)): 文章ID，主键。
  - `board_id` (int): 板块ID。
  - `board_name` (varchar(50)): 板块名称。
  - `p_board_id` (int): 父级板块ID。
  - `p_board_name` (varchar(50)): 父板块名称。
  - `user_id` (varchar(15)): 用户ID。
  - `nick_name` (varchar(20)): 昵称。
  - `user_ip_address` (varchar(100)): 最后登录IP地址。
  - `title` (varchar(150)): 标题。
  - `cover` (varchar(100)): 封面。
  - `content` (text): 内容。
  - `markdown_content` (text): Markdown内容。
  - `editor_type` (tinyint): 编辑器类型（0:富文本编辑器，1:Markdown编辑器）。
  - `summary` (varchar(200)): 摘要。
  - `post_time` (datetime): 发布时间。
  - `last_update_time` (timestamp): 最后更新时间。
  - `read_count` (int): 阅读数量。
  - `good_count` (int): 点赞数。
  - `comment_count` (int): 评论数。
  - `top_type` (tinyint): 置顶类型（0:未置顶，1:已置顶）。
  - `attachment_type` (tinyint): 附件类型（0:没有附件，1:有附件）。
  - `status` (tinyint): 状态（-1:已删除，0:待审核，1:已审核）。
- **约束**:
  - 主键: `article_id`。
  - 索引: `idx_board_id`, `idx_pboard_id`, `idx_post_time`, `idx_top_type`, `idx_title`, `idx_user_id`。

### 4. `forum_article_attachment` 表
- **字段**:
  - `file_id` (varchar(15)): 文件ID，主键。
  - `article_id` (varchar(15)): 文章ID。
  - `user_id` (varchar(15)): 用户ID。
  - `file_size` (bigint): 文件大小。
  - `file_name` (varchar(200)): 文件名称。
  - `download_count` (int): 下载次数。
  - `file_path` (varchar(100)): 文件路径。
  - `file_type` (tinyint): 文件类型。
  - `integral` (int): 下载所需积分。
- **约束**:
  - 主键: `file_id`。
  - 索引: `idx_article_id`, `idx_user_id`。

### 5. `forum_article_attachment_download` 表
- **字段**:
  - `file_id` (varchar(15)): 文件ID，主键。
  - `user_id` (varchar(15)): 用户ID，主键。
  - `article_id` (varchar(15)): 文章ID。
  - `download_count` (int): 文件下载次数。
- **约束**:
  - 主键: `file_id`, `user_id`。

### 6. `forum_board` 表
- **字段**:
  - `board_id` (int): 板块ID，主键，自增。
  - `p_board_id` (int): 父级板块ID。
  - `board_name` (varchar(50)): 板块名。
  - `cover` (varchar(50)): 封面。
  - `board_desc` (varchar(150)): 描述。
  - `sort` (int): 排序。
  - `post_type` (tinyint): 发帖类型（0:只允许管理员发帖，1:任何人可以发帖）。
- **约束**:
  - 主键: `board_id`。

### 7. `forum_comment` 表
- **字段**:
  - `comment_id` (int): 评论ID，主键，自增。
  - `p_comment_id` (int): 父级评论ID。
  - `article_id` (varchar(15)): 文章ID。
  - `content` (varchar(800)): 回复内容。
  - `img_path` (varchar(150)): 图片。
  - `user_id` (varchar(15)): 用户ID。
  - `nick_name` (varchar(20)): 昵称。
  - `user_ip_address` (varchar(100)): 用户IP地址。
  - `reply_user_id` (varchar(15)): 回复人ID。
  - `reply_nick_name` (varchar(20)): 回复人昵称。
  - `top_type` (tinyint): 置顶类型（0:未置顶，1:置顶）。
  - `post_time` (datetime): 发布时间。
  - `good_count` (int): 点赞数。
  - `status` (tinyint): 状态（0:待审核，1:已审核）。
- **约束**:
  - 主键: `comment_id`。
  - 索引: `idx_article_id`, `idx_post_time`, `idx_top`, `idx_p_id`, `idx_status`, `idx_user_id`。

### 8. `like_record` 表
- **字段**:
  - `op_id` (int): 自增ID，主键。
  - `op_type` (tinyint): 操作类型（0:文章点赞，1:评论点赞）。
  - `object_id` (varchar(15)): 主体ID。
  - `user_id` (varchar(15)): 用户ID。
  - `create_time` (datetime): 发布时间。
  - `author_user_id` (varchar(15)): 主体作者ID。
- **约束**:
  - 主键: `op_id`。
  - 唯一索引: `idx_key` (`object_id`, `user_id`, `op_type`)。
  - 索引: `idx_user_id`。

### 9. `sys_setting` 表
- **字段**:
  - `code` (varchar(10)): 编号，主键。
  - `json_content` (varchar(500)): 设置信息。
- **约束**:
  - 主键: `code`。

### 10. `user_info` 表
- **字段**:
  - `user_id` (varchar(15)): 用户ID，主键。
  - `nick_name` (varchar(20)): 昵称。
  - `email` (varchar(150)): 邮箱。
  - `password` (varchar(50)): 密码。
  - `sex` (tinyint): 性别（0:女，1:男）。
  - `person_description` (varchar(200)): 个人描述。
  - `join_time` (datetime): 加入时间。
  - `last_login_time` (datetime): 最后登录时间。
  - `last_login_ip` (varchar(15)): 最后登录IP。
  - `last_login_ip_address` (varchar(100)): 最后登录IP地址。
  - `total_integral` (int): 总积分。
  - `current_integral` (int): 当前积分。
  - `status` (tinyint): 状态（0:禁用，1:正常）。
  - `is_admin` (int): 是否是管理员。
  - `image` (varchar(255)): 用户头像。
- **约束**:
  - 主键: `user_id`。
  - 唯一索引: `key_email`, `key_nick_name`。

### 11. `user_integral_record` 表
- **字段**:
  - `record_id` (int): 记录ID，主键，自增。
  - `user_id` (varchar(15)): 用户ID。
  - `oper_type` (tinyint): 操作类型。
  - `integral` (int): 积分。
  - `create_time` (datetime): 创建时间。
- **约束**:
  - 主键: `record_id`。

### 12. `user_message` 表
- **字段**:
  - `message_id` (int): 自增ID，主键。
  - `received_user_id` (varchar(15)): 接收人用户ID。
  - `article_id` (varchar(15)): 文章ID。
  - `article_title` (varchar(150)): 文章标题。
  - `comment_id` (int): 评论ID。
  - `send_user_id` (varchar(15)): 发送人用户ID。
  - `send_nick_name` (varchar(20)): 发送人昵称。
  - `message_type` (tinyint): 消息类型（0:系统消息，1:评论，2:文章点赞，3:评论点赞，4:附件下载）。
  - `message_content` (varchar(1000)): 消息内容。
  - `status` (tinyint): 状态（1:未读，2:已读）。
  - `create_time` (datetime): 创建时间。
- **约束**:
  - 主键: `message_id`。
  - 唯一索引: `idx_key` (`article_id`, `comment_id`, `send_user_id`, `message_type`)。
  - 索引: `idx_received_user_id`, `idx_status`, `idx_type`。

这些表结构描述了数据库中的各个表及其字段、约束和索引。