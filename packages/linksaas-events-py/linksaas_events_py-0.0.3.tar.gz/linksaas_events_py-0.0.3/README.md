定义在linksaas里面的事件

## 项目事件

事件定义在project_events.py

| 类名                      | 事件类型     |
| ------------------------- | ------------ |
| CreateProjectEvent        | 创建项目     |
| UpdateProjectEvent        | 设置项目     |
| OpenProjectEvent          | 打开项目     |
| CloseProjectEvent         | 关闭项目     |
| RemoveProjectEvent        | 删除项目     |
| GenInviteEvent            | 创建邀请码   |
| JoinProjectEvent          | 加入项目     |
| LeaveProjectEvent         | 离开项目     |
| CreateRoleEvent           | 创建角色     |
| UpdateRoleEvent           | 更新角色     |
| RemoveRoleEvent           | 删除角色     |
| UpdateProjectMemberEvent  | 更新成员     |
| RemoveProjectMemberEvent  | 删除成员     |
| SetProjectMemberRoleEvent | 设置成员角色 |
| UploadWorkSnapShotEvent   | 工作快照     |
| CreateChannelEvent        | 创建频道     |
| UpdateChannelEvent        | 更新频道     |
| OpenChannelEvent          | 打开频道     |
| CloseChannelEvent         | 关闭频道     |
| RemoveChannelEvent        | 删除频道     |
| AddChannelMemberEvent     | 增加频道成员 |
| RemoveChannelMemberEvent  | 删除频道成员 |
| CreateAppraiseEvent       | 创建评估     |
| AddProjectAppEvent        | 增加项目应用 |
| RemoveProjectAppEvent     | 删除项目应用 |

## 文档事件

事件定义在project_doc_events.py

| 类名                  | 事件类型                                                    |
| --------------------- | ----------------------------------------------------------- |
| CreateSpaceEvent      | 创建文档空间                                                |
| UpdateSpaceEvent      | 修改文档空间                                                |
| RemoveSpaceEvent      | 删除文档空间                                                |
| CreateDocEvent        | 创建文档                                                    |
| UpdateDocEvent        | 更新文档 (同一个用户同一个文档修改，不记录一个小时内的操作) |
| MoveDocToRecycleEvent | 移动到回收站                                                |
| RemoveDocEvent        | 删除文档                                                    |
| RecoverDocEvent       | 恢复文档                                                    |
| WatchDocEvent         | 关注文档                                                    |
| UnWatchDocEvent       | 取消关注文档                                                |
| MoveDocEvent          | 移动文档                                                    |


## 迭代事件

事件定义在project_sprit_events.py

| 类名        | 事件类型 |
| ----------- | -------- |
| CreateEvent | 创建迭代 |
| UpdateEvent | 更新迭代 |
| RemoveEvent | 删除迭代 |

## 工单事件

事件定义在project_issue_event.py

| 类名                       | 事件类型         |
| -------------------------- | ---------------- |
| CreateEvent                | 创建issue        |
| UpdateEvent                | 更新issue        |
| RemoveEvent                | 删除issue        |
| AssignExecUserEvent        | 指派执行者       |
| AssignCheckUserEvent       | 指派检查者       |
| ChangeStateEvent           | 修改状态         |
| LinkSpritEvent             | 关联到迭代       |
| CancelLinkSpritEvent       | 取消到迭代的关联 |
| SetStartTimeEvent          | 设置开始时间     |
| CancelStartTimeEvent       | 取消开始时间     |
| SetEndTimeEvent            | 设置结束时间     |
| CancelEndTimeEvent         | 取消结束时间     |
| SetEstimateMinutesEvent    | 设置预估时间     |
| CancelEstimateMinutesEvent | 取消预估时间     |
| SetRemainMinutesEvent      | 设置剩余时间     |
| CancelRemainMinutesEvent   | 取消剩余时间     |
| CreateSubIssueEvent        | 增加子工单       |
| UpdateSubIssueEvent        | 更新子工单       |
| UpdateSubIssueStateEvent   | 更新子工单状态   |
| RemoveSubIssueEvent        | 删除子工单       |
| AddDependenceEvent         | 增加依赖         |
| RemoveDependenceEvent      | 删除依赖         |

## 书库事件

事件定义在project_book_shelf_events.py
| 类名            | 事件类型 |
| --------------- | -------- |
| AddBookEvent    | 增加书本 |
| RemoveBookEvent | 删除书本 |


## 第三方接入事件

事件定义在project_ext_event_events.py

| 类名                     | 事件类型           |
| ------------------------ | ------------------ |
| CreateEvent              | 创建事件源         |
| UpdateEvent              | 更新事件源         |
| GetSecretEvent           | 获取事件源秘钥     |
| RemoveEvent              | 删除事件源         |
| SetSourceUserPolicyEvent | 设置事件源用户策略 |

## gitlab事件

事件定义在project_gitlab_events.py

| 类名              | 事件类型 |
| ----------------- | -------- |
| BuildEvent        |          |
| CommentEvent      |          |
| IssueEvent        |          |
| JobEvent          |          |
| MergeRequestEvent |          |
| PipelineEvent     |          |
| PushEvent         |          |
| TagEvent          |          |
| WikiEvent         |          |

## gitee事件

事件定义在project_gitee_events.py

| 类名             | 事件类型 |
| ---------------- | -------- |
| PushEvent        |          |
| IssueEvent       |          |
| PullRequestEvent |          |
| NoteEvent        |          |

## 机器人事件

事件定义在project_robot_events.py

| 类名                  | 事件类型     |
| --------------------- | ------------ |
| CreateEvent           | 创建机器人   |
| UpdateEvent           | 更新机器人   |
| RemoveEvent           | 删除机器人   |
| AddAccessUserEvent    | 新增访问用户 |
| RemoveAccessUserEvent | 删除访问用户 |
| RenewTokenEvent       | 更新访问令牌 |

## earthly事件

事件定义在project_earthly_events.py

| 类名              | 事件类型     |
| ----------------- | ------------ |
| AddRepoEvent      | 创建仓库     |
| RemoveRepoEvent   | 删除仓库     |
| CreateActionEvent | 创建执行命令 |
| UpdateActionEvent | 更新执行命令 |
| RemoveActionEvent | 删除执行命令 |

