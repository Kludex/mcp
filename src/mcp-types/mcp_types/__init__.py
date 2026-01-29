from typing import Annotated, Any, Literal

from pydantic import Field, with_config
from typing_extensions import NotRequired, TypedDict


class Annotations(TypedDict):
    audience: NotRequired[list[str]]
    last_modified: Annotated[NotRequired[str], Field(alias="lastModified")]
    priority: NotRequired[float]


@with_config(extra="allow")
class Meta(TypedDict):
    pass


class AudioContent(TypedDict):
    _meta: NotRequired[Meta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["audio"]


class BaseMetadata(TypedDict):
    name: str
    title: NotRequired[str]


@with_config(extra="allow")
class BlobResourceContentsMeta(TypedDict):
    pass


class BlobResourceContents(TypedDict):
    _meta: NotRequired[BlobResourceContentsMeta]
    blob: str
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    uri: str


class BooleanSchema(TypedDict):
    default: NotRequired[bool]
    description: NotRequired[str]
    title: NotRequired[str]
    type: Literal["boolean"]


@with_config(extra="allow")
class ParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


@with_config(extra="allow")
class Arguments(TypedDict):
    pass


class TaskMetadata(TypedDict):
    ttl: NotRequired[int]


class CallToolRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    arguments: NotRequired[Arguments]
    name: str
    task: NotRequired[TaskMetadata]


class CallToolRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tools/call"]
    params: CallToolRequestParams


@with_config(extra="allow")
class CallToolRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


@with_config(extra="allow")
class ProgressTokenArguments(TypedDict):
    pass


class TaskCallToolRequestParams(TypedDict):
    _meta: NotRequired[CallToolRequestParamsMeta]
    arguments: NotRequired[ProgressTokenArguments]
    name: str
    task: NotRequired[TaskMetadata]


@with_config(extra="allow")
class CallToolResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ContentBlockMeta(TypedDict):
    pass


class TextContent(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    text: str
    type: Literal["text"]


class ImageContent(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["image"]


class Icon(TypedDict):
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    sizes: NotRequired[list[str]]
    src: str
    theme: NotRequired[str]


class ResourceLink(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    type: Literal["resource_link"]
    uri: str


@with_config(extra="allow")
class ResourceMeta(TypedDict):
    pass


class TextResourceContents(TypedDict):
    _meta: NotRequired[ResourceMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    text: str
    uri: str


class EmbeddedResource(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    resource: TextResourceContents | BlobResourceContents
    type: Literal["resource"]


@with_config(extra="allow")
class StructuredContent(TypedDict):
    pass


class CallToolResult(TypedDict):
    _meta: NotRequired[CallToolResultMeta]
    content: list[TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource]
    is_error: Annotated[NotRequired[bool], Field(alias="isError")]
    structured_content: Annotated[NotRequired[StructuredContent], Field(alias="structuredContent")]


class Params(TypedDict):
    task_id: Annotated[str, Field(alias="taskId")]


class CancelTaskRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/cancel"]
    params: Params


class CancelledNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    reason: NotRequired[str]
    request_id: Annotated[NotRequired[str | int], Field(alias="requestId")]


class CancelledNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/cancelled"]
    params: CancelledNotificationParams


@with_config(extra="allow")
class CancelledNotificationParamsMeta(TypedDict):
    pass


class RequestIdCancelledNotificationParams(TypedDict):
    _meta: NotRequired[CancelledNotificationParamsMeta]
    reason: NotRequired[str]
    request_id: Annotated[NotRequired[str | int], Field(alias="requestId")]


@with_config(extra="allow")
class Form(TypedDict):
    pass


@with_config(extra="allow")
class Url(TypedDict):
    pass


class Elicitation(TypedDict):
    form: NotRequired[Form]
    url: NotRequired[Url]


@with_config(extra="allow")
class Experimental(TypedDict):
    pass


class Roots(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


@with_config(extra="allow")
class Context(TypedDict):
    pass


@with_config(extra="allow")
class Tools(TypedDict):
    pass


class Sampling(TypedDict):
    context: NotRequired[Context]
    tools: NotRequired[Tools]


@with_config(extra="allow")
class Cancel(TypedDict):
    pass


@with_config(extra="allow")
class List(TypedDict):
    pass


@with_config(extra="allow")
class Create(TypedDict):
    pass


class RequestsElicitation(TypedDict):
    create: NotRequired[Create]


@with_config(extra="allow")
class CreateMessage(TypedDict):
    pass


class RequestsSampling(TypedDict):
    create_message: Annotated[NotRequired[CreateMessage], Field(alias="createMessage")]


class Requests(TypedDict):
    elicitation: NotRequired[RequestsElicitation]
    sampling: NotRequired[RequestsSampling]


class Tasks(TypedDict):
    cancel: NotRequired[Cancel]
    list: NotRequired[List]
    requests: NotRequired[Requests]


class ClientCapabilities(TypedDict):
    elicitation: NotRequired[Elicitation]
    experimental: NotRequired[Experimental]
    roots: NotRequired[Roots]
    sampling: NotRequired[Sampling]
    tasks: NotRequired[Tasks]


class NotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class InitializedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/initialized"]
    params: NotRequired[NotificationParams]


class ProgressNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    message: NotRequired[str]
    progress: float
    progress_token: Annotated[str | int, Field(alias="progressToken")]
    total: NotRequired[float]


class ProgressNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/progress"]
    params: ProgressNotificationParams


class TaskStatusNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/tasks/status"]
    params: Any


class RootsListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/roots/list_changed"]
    params: NotRequired[NotificationParams]


class Implementation(TypedDict):
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    name: str
    title: NotRequired[str]
    version: str
    website_url: Annotated[NotRequired[str], Field(alias="websiteUrl")]


class InitializeRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    capabilities: ClientCapabilities
    client_info: Annotated[Implementation, Field(alias="clientInfo")]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]


class InitializeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["initialize"]
    params: InitializeRequestParams


class RequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class PingRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["ping"]
    params: NotRequired[RequestParams]


class PaginatedRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    cursor: NotRequired[str]


class ListResourcesRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/list"]
    params: NotRequired[PaginatedRequestParams]


class ListResourceTemplatesRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/templates/list"]
    params: NotRequired[PaginatedRequestParams]


class ReadResourceRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    uri: str


class ReadResourceRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/read"]
    params: ReadResourceRequestParams


class SubscribeRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    uri: str


class SubscribeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/subscribe"]
    params: SubscribeRequestParams


class UnsubscribeRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    uri: str


class UnsubscribeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/unsubscribe"]
    params: UnsubscribeRequestParams


class ListPromptsRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["prompts/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ParamsArguments(TypedDict):
    pass


class GetPromptRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    arguments: NotRequired[ParamsArguments]
    name: str


class GetPromptRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["prompts/get"]
    params: GetPromptRequestParams


class ListToolsRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tools/list"]
    params: NotRequired[PaginatedRequestParams]


class IdParams(TypedDict):
    task_id: Annotated[str, Field(alias="taskId")]


class GetTaskRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/get"]
    params: IdParams


class GetTaskPayloadRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/result"]
    params: IdParams


class ListTasksRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/list"]
    params: NotRequired[PaginatedRequestParams]


class SetLevelRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    level: str


class SetLevelRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["logging/setLevel"]
    params: SetLevelRequestParams


class Argument(TypedDict):
    name: str
    value: str


@with_config(extra="allow")
class ContextArguments(TypedDict):
    pass


class ParamsContext(TypedDict):
    arguments: NotRequired[ContextArguments]


class PromptReference(TypedDict):
    name: str
    title: NotRequired[str]
    type: Literal["ref/prompt"]


class ResourceTemplateReference(TypedDict):
    type: Literal["ref/resource"]
    uri: str


class CompleteRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    argument: Argument
    context: NotRequired[ParamsContext]
    ref: PromptReference | ResourceTemplateReference


class CompleteRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["completion/complete"]
    params: CompleteRequestParams


@with_config(extra="allow")
class ClientResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class Result(TypedDict):
    _meta: NotRequired[ClientResultMeta]


@with_config(extra="allow")
class GetTaskPayloadResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]


class Task(TypedDict):
    created_at: Annotated[str, Field(alias="createdAt")]
    last_updated_at: Annotated[str, Field(alias="lastUpdatedAt")]
    poll_interval: Annotated[NotRequired[int], Field(alias="pollInterval")]
    status: str
    status_message: Annotated[NotRequired[str], Field(alias="statusMessage")]
    task_id: Annotated[str, Field(alias="taskId")]
    ttl: int


class ListTasksResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    tasks: list[Task]


@with_config(extra="allow")
class ContentMeta(TypedDict):
    pass


@with_config(extra="allow")
class Input(TypedDict):
    pass


class ToolUseContent(TypedDict):
    _meta: NotRequired[ContentMeta]
    id: str
    input: Input
    name: str
    type: Literal["tool_use"]


@with_config(extra="allow")
class ContentBlockStructuredContent(TypedDict):
    pass


class ToolResultContent(TypedDict):
    _meta: NotRequired[ContentMeta]
    content: list[TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource]
    is_error: Annotated[NotRequired[bool], Field(alias="isError")]
    structured_content: Annotated[NotRequired[ContentBlockStructuredContent], Field(alias="structuredContent")]
    tool_use_id: Annotated[str, Field(alias="toolUseId")]
    type: Literal["tool_result"]


class CreateMessageResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    content: (
        TextContent
        | ImageContent
        | AudioContent
        | ToolUseContent
        | ToolResultContent
        | list[TextContent | ImageContent | AudioContent | ToolUseContent | ToolResultContent]
    )
    model: str
    role: str
    stop_reason: Annotated[NotRequired[str], Field(alias="stopReason")]


@with_config(extra="allow")
class RootsMeta(TypedDict):
    pass


class Root(TypedDict):
    _meta: NotRequired[RootsMeta]
    name: NotRequired[str]
    uri: str


class ListRootsResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    roots: list[Root]


@with_config(extra="allow")
class Content(TypedDict):
    pass


class ElicitResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    action: str
    content: NotRequired[Content]


class ClientResultCompleteRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["completion/complete"]
    params: CompleteRequestParams


@with_config(extra="allow")
class CompleteRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ProgressTokenArgument(TypedDict):
    name: str
    value: str


class ProgressTokenContext(TypedDict):
    arguments: NotRequired[ContextArguments]


class ParamsCompleteRequestParams(TypedDict):
    _meta: NotRequired[CompleteRequestParamsMeta]
    argument: ProgressTokenArgument
    context: NotRequired[ProgressTokenContext]
    ref: PromptReference | ResourceTemplateReference


@with_config(extra="allow")
class CompleteResultMeta(TypedDict):
    pass


class Completion(TypedDict):
    has_more: Annotated[NotRequired[bool], Field(alias="hasMore")]
    total: NotRequired[int]
    values: list[str]


class CompleteResult(TypedDict):
    _meta: NotRequired[CompleteResultMeta]
    completion: Completion


@with_config(extra="allow")
class MessagesMeta(TypedDict):
    pass


class SamplingMessage(TypedDict):
    _meta: NotRequired[MessagesMeta]
    content: (
        TextContent
        | ImageContent
        | AudioContent
        | ToolUseContent
        | ToolResultContent
        | list[TextContent | ImageContent | AudioContent | ToolUseContent | ToolResultContent]
    )
    role: str


@with_config(extra="allow")
class Metadata(TypedDict):
    pass


class ModelHint(TypedDict):
    name: NotRequired[str]


class ModelPreferences(TypedDict):
    cost_priority: Annotated[NotRequired[float], Field(alias="costPriority")]
    hints: NotRequired[list[ModelHint]]
    intelligence_priority: Annotated[NotRequired[float], Field(alias="intelligencePriority")]
    speed_priority: Annotated[NotRequired[float], Field(alias="speedPriority")]


class ToolChoice(TypedDict):
    mode: NotRequired[str]


@with_config(extra="allow")
class ToolsMeta(TypedDict):
    pass


class ToolAnnotations(TypedDict):
    destructive_hint: Annotated[NotRequired[bool], Field(alias="destructiveHint")]
    idempotent_hint: Annotated[NotRequired[bool], Field(alias="idempotentHint")]
    open_world_hint: Annotated[NotRequired[bool], Field(alias="openWorldHint")]
    read_only_hint: Annotated[NotRequired[bool], Field(alias="readOnlyHint")]
    title: NotRequired[str]


class ToolExecution(TypedDict):
    task_support: Annotated[NotRequired[str], Field(alias="taskSupport")]


@with_config(extra="allow")
class Properties(TypedDict):
    pass


class InputSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: NotRequired[Properties]
    required: NotRequired[list[str]]
    type: Literal["object"]


@with_config(extra="allow")
class OutputSchemaProperties(TypedDict):
    pass


class OutputSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: NotRequired[OutputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class Tool(TypedDict):
    _meta: NotRequired[ToolsMeta]
    annotations: NotRequired[ToolAnnotations]
    description: NotRequired[str]
    execution: NotRequired[ToolExecution]
    icons: NotRequired[list[Icon]]
    input_schema: Annotated[InputSchema, Field(alias="inputSchema")]
    name: str
    output_schema: Annotated[NotRequired[OutputSchema], Field(alias="outputSchema")]
    title: NotRequired[str]


class CreateMessageRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    include_context: Annotated[NotRequired[str], Field(alias="includeContext")]
    max_tokens: Annotated[int, Field(alias="maxTokens")]
    messages: list[SamplingMessage]
    metadata: NotRequired[Metadata]
    model_preferences: Annotated[NotRequired[ModelPreferences], Field(alias="modelPreferences")]
    stop_sequences: Annotated[NotRequired[list[str]], Field(alias="stopSequences")]
    system_prompt: Annotated[NotRequired[str], Field(alias="systemPrompt")]
    task: NotRequired[TaskMetadata]
    temperature: NotRequired[float]
    tool_choice: Annotated[NotRequired[ToolChoice], Field(alias="toolChoice")]
    tools: NotRequired[list[Tool]]


class CreateMessageRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["sampling/createMessage"]
    params: CreateMessageRequestParams


@with_config(extra="allow")
class CreateMessageRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


@with_config(extra="allow")
class ProgressTokenMetadata(TypedDict):
    pass


class ExecutionCreateMessageRequestParams(TypedDict):
    _meta: NotRequired[CreateMessageRequestParamsMeta]
    include_context: Annotated[NotRequired[str], Field(alias="includeContext")]
    max_tokens: Annotated[int, Field(alias="maxTokens")]
    messages: list[SamplingMessage]
    metadata: NotRequired[ProgressTokenMetadata]
    model_preferences: Annotated[NotRequired[ModelPreferences], Field(alias="modelPreferences")]
    stop_sequences: Annotated[NotRequired[list[str]], Field(alias="stopSequences")]
    system_prompt: Annotated[NotRequired[str], Field(alias="systemPrompt")]
    task: NotRequired[TaskMetadata]
    temperature: NotRequired[float]
    tool_choice: Annotated[NotRequired[ToolChoice], Field(alias="toolChoice")]
    tools: NotRequired[list[Tool]]


@with_config(extra="allow")
class CreateMessageResultMeta(TypedDict):
    pass


class ToolChoiceCreateMessageResult(TypedDict):
    _meta: NotRequired[CreateMessageResultMeta]
    content: (
        TextContent
        | ImageContent
        | AudioContent
        | ToolUseContent
        | ToolResultContent
        | list[TextContent | ImageContent | AudioContent | ToolUseContent | ToolResultContent]
    )
    model: str
    role: str
    stop_reason: Annotated[NotRequired[str], Field(alias="stopReason")]


@with_config(extra="allow")
class CreateTaskResultMeta(TypedDict):
    pass


class CreateTaskResult(TypedDict):
    _meta: NotRequired[CreateTaskResultMeta]
    task: Task


@with_config(extra="allow")
class ElicitRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ElicitRequestURLParams(TypedDict):
    _meta: NotRequired[ElicitRequestParamsMeta]
    elicitation_id: Annotated[str, Field(alias="elicitationId")]
    message: str
    mode: Literal["url"]
    task: NotRequired[TaskMetadata]
    url: str


@with_config(extra="allow")
class RequestedSchemaProperties(TypedDict):
    pass


class RequestedSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: RequestedSchemaProperties
    required: NotRequired[list[str]]
    type: Literal["object"]


class ElicitRequestFormParams(TypedDict):
    _meta: NotRequired[ElicitRequestParamsMeta]
    message: str
    mode: NotRequired[Literal["form"]]
    requested_schema: Annotated[RequestedSchema, Field(alias="requestedSchema")]
    task: NotRequired[TaskMetadata]


class ElicitRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["elicitation/create"]
    params: ElicitRequestURLParams | ElicitRequestFormParams


@with_config(extra="allow")
class ElicitRequestFormParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ProgressTokenRequestedSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: RequestedSchemaProperties
    required: NotRequired[list[str]]
    type: Literal["object"]


class TaskElicitRequestFormParams(TypedDict):
    _meta: NotRequired[ElicitRequestFormParamsMeta]
    message: str
    mode: NotRequired[Literal["form"]]
    requested_schema: Annotated[ProgressTokenRequestedSchema, Field(alias="requestedSchema")]
    task: NotRequired[TaskMetadata]


@with_config(extra="allow")
class ElicitRequestURLParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ElicitRequestParamsElicitRequestURLParams(TypedDict):
    _meta: NotRequired[ElicitRequestURLParamsMeta]
    elicitation_id: Annotated[str, Field(alias="elicitationId")]
    message: str
    mode: Literal["url"]
    task: NotRequired[TaskMetadata]
    url: str


@with_config(extra="allow")
class ElicitResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ElicitResultContent(TypedDict):
    pass


class TaskElicitResult(TypedDict):
    _meta: NotRequired[ElicitResultMeta]
    action: str
    content: NotRequired[ElicitResultContent]


class ElicitationCompleteNotificationParams(TypedDict):
    elicitation_id: Annotated[str, Field(alias="elicitationId")]


class ElicitationCompleteNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/elicitation/complete"]
    params: ElicitationCompleteNotificationParams


@with_config(extra="allow")
class EmbeddedResourceMeta(TypedDict):
    pass


class TaskEmbeddedResource(TypedDict):
    _meta: NotRequired[EmbeddedResourceMeta]
    annotations: NotRequired[Annotations]
    resource: TextResourceContents | BlobResourceContents
    type: Literal["resource"]


class UntitledSingleSelectEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    enum: list[str]
    title: NotRequired[str]
    type: Literal["string"]


class GeneratedType(TypedDict):
    const: str
    title: str


class TitledSingleSelectEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    one_of: Annotated[list[GeneratedType], Field(alias="oneOf")]
    title: NotRequired[str]
    type: Literal["string"]


class Items(TypedDict):
    enum: list[str]
    type: Literal["string"]


class UntitledMultiSelectEnumSchema(TypedDict):
    default: NotRequired[list[str]]
    description: NotRequired[str]
    items: Items
    max_items: Annotated[NotRequired[int], Field(alias="maxItems")]
    min_items: Annotated[NotRequired[int], Field(alias="minItems")]
    title: NotRequired[str]
    type: Literal["array"]


class ItemsGeneratedType(TypedDict):
    const: str
    title: str


class EnumSchemaItems(TypedDict):
    any_of: Annotated[list[ItemsGeneratedType], Field(alias="anyOf")]


class TitledMultiSelectEnumSchema(TypedDict):
    default: NotRequired[list[str]]
    description: NotRequired[str]
    items: EnumSchemaItems
    max_items: Annotated[NotRequired[int], Field(alias="maxItems")]
    min_items: Annotated[NotRequired[int], Field(alias="minItems")]
    title: NotRequired[str]
    type: Literal["array"]


class LegacyTitledEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    enum: list[str]
    enum_names: Annotated[NotRequired[list[str]], Field(alias="enumNames")]
    title: NotRequired[str]
    type: Literal["string"]


class Error(TypedDict):
    code: int
    data: NotRequired[Any]
    message: str


class EnumSchemaGetPromptRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["prompts/get"]
    params: GetPromptRequestParams


@with_config(extra="allow")
class GetPromptRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsGetPromptRequestParams(TypedDict):
    _meta: NotRequired[GetPromptRequestParamsMeta]
    arguments: NotRequired[ProgressTokenArguments]
    name: str


@with_config(extra="allow")
class GetPromptResultMeta(TypedDict):
    pass


class PromptMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource
    role: str


class GetPromptResult(TypedDict):
    _meta: NotRequired[GetPromptResultMeta]
    description: NotRequired[str]
    messages: list[PromptMessage]


class RoleGetTaskPayloadRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/result"]
    params: IdParams


@with_config(extra="allow")
class GetTaskPayloadResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class IdGetTaskPayloadResult(TypedDict):
    _meta: NotRequired[GetTaskPayloadResultMeta]


class IdGetTaskRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/get"]
    params: IdParams


class IdIcon(TypedDict):
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    sizes: NotRequired[list[str]]
    src: str
    theme: NotRequired[str]


class Icons(TypedDict):
    icons: NotRequired[list[Icon]]


@with_config(extra="allow")
class ImageContentMeta(TypedDict):
    pass


class IdImageContent(TypedDict):
    _meta: NotRequired[ImageContentMeta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["image"]


class AnnotationsImplementation(TypedDict):
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    name: str
    title: NotRequired[str]
    version: str
    website_url: Annotated[NotRequired[str], Field(alias="websiteUrl")]


class AnnotationsInitializeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["initialize"]
    params: InitializeRequestParams


@with_config(extra="allow")
class InitializeRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsInitializeRequestParams(TypedDict):
    _meta: NotRequired[InitializeRequestParamsMeta]
    capabilities: ClientCapabilities
    client_info: Annotated[Implementation, Field(alias="clientInfo")]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]


@with_config(extra="allow")
class InitializeResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class Completions(TypedDict):
    pass


@with_config(extra="allow")
class CapabilitiesExperimental(TypedDict):
    pass


@with_config(extra="allow")
class Logging(TypedDict):
    pass


class Prompts(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class Resources(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]
    subscribe: NotRequired[bool]


@with_config(extra="allow")
class TasksCancel(TypedDict):
    pass


@with_config(extra="allow")
class TasksList(TypedDict):
    pass


@with_config(extra="allow")
class Call(TypedDict):
    pass


class RequestsTools(TypedDict):
    call: NotRequired[Call]


class TasksRequests(TypedDict):
    tools: NotRequired[RequestsTools]


class CapabilitiesTasks(TypedDict):
    cancel: NotRequired[TasksCancel]
    list: NotRequired[TasksList]
    requests: NotRequired[TasksRequests]


class CapabilitiesTools(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class ServerCapabilities(TypedDict):
    completions: NotRequired[Completions]
    experimental: NotRequired[CapabilitiesExperimental]
    logging: NotRequired[Logging]
    prompts: NotRequired[Prompts]
    resources: NotRequired[Resources]
    tasks: NotRequired[CapabilitiesTasks]
    tools: NotRequired[CapabilitiesTools]


class InitializeResult(TypedDict):
    _meta: NotRequired[InitializeResultMeta]
    capabilities: ServerCapabilities
    instructions: NotRequired[str]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]
    server_info: Annotated[Implementation, Field(alias="serverInfo")]


class ServerInfoInitializedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/initialized"]
    params: NotRequired[NotificationParams]


class JSONRPCErrorResponse(TypedDict):
    error: Error
    id: NotRequired[str | int]
    jsonrpc: Literal["2.0"]


class JSONRPCRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[IdParams]


@with_config(extra="allow")
class JSONRPCMessageParams(TypedDict):
    pass


class JSONRPCNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[JSONRPCMessageParams]


class JSONRPCResultResponse(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    result: Result


@with_config(extra="allow")
class JSONRPCNotificationParams(TypedDict):
    pass


class JSONRPCMessageJSONRPCNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[JSONRPCNotificationParams]


class JSONRPCMessageJSONRPCRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[IdParams]


class JSONRPCResponseJSONRPCResultResponse(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    result: Result


class ResultLegacyTitledEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    enum: list[str]
    enum_names: Annotated[NotRequired[list[str]], Field(alias="enumNames")]
    title: NotRequired[str]
    type: Literal["string"]


class ResultListPromptsRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["prompts/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ListPromptsResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class PromptsMeta(TypedDict):
    pass


class PromptArgument(TypedDict):
    description: NotRequired[str]
    name: str
    required: NotRequired[bool]
    title: NotRequired[str]


class Prompt(TypedDict):
    _meta: NotRequired[PromptsMeta]
    arguments: NotRequired[list[PromptArgument]]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    name: str
    title: NotRequired[str]


class ListPromptsResult(TypedDict):
    _meta: NotRequired[ListPromptsResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    prompts: list[Prompt]


class ParamsListResourceTemplatesRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/templates/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ListResourceTemplatesResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ResourceTemplatesMeta(TypedDict):
    pass


class ResourceTemplate(TypedDict):
    _meta: NotRequired[ResourceTemplatesMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    title: NotRequired[str]
    uri_template: Annotated[str, Field(alias="uriTemplate")]


class ListResourceTemplatesResult(TypedDict):
    _meta: NotRequired[ListResourceTemplatesResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    resource_templates: Annotated[list[ResourceTemplate], Field(alias="resourceTemplates")]


class AnnotationsListResourcesRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ListResourcesResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ResourcesMeta(TypedDict):
    pass


class Resource(TypedDict):
    _meta: NotRequired[ResourcesMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    uri: str


class ListResourcesResult(TypedDict):
    _meta: NotRequired[ListResourcesResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    resources: list[Resource]


class ListRootsRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["roots/list"]
    params: NotRequired[RequestParams]


@with_config(extra="allow")
class ListRootsResultMeta(TypedDict):
    pass


class ParamsListRootsResult(TypedDict):
    _meta: NotRequired[ListRootsResultMeta]
    roots: list[Root]


class ParamsListTasksRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tasks/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ListTasksResultMeta(TypedDict):
    pass


class ParamsListTasksResult(TypedDict):
    _meta: NotRequired[ListTasksResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    tasks: list[Task]


class ParamsListToolsRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["tools/list"]
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class ListToolsResultMeta(TypedDict):
    pass


class ListToolsResult(TypedDict):
    _meta: NotRequired[ListToolsResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    tools: list[Tool]


class LoggingMessageNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    data: Any
    level: str
    logger: NotRequired[str]


class LoggingMessageNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/message"]
    params: LoggingMessageNotificationParams


@with_config(extra="allow")
class LoggingMessageNotificationParamsMeta(TypedDict):
    pass


class LevelLoggingMessageNotificationParams(TypedDict):
    _meta: NotRequired[LoggingMessageNotificationParamsMeta]
    data: Any
    level: str
    logger: NotRequired[str]


class LevelModelHint(TypedDict):
    name: NotRequired[str]


class LevelModelPreferences(TypedDict):
    cost_priority: Annotated[NotRequired[float], Field(alias="costPriority")]
    hints: NotRequired[list[ModelHint]]
    intelligence_priority: Annotated[NotRequired[float], Field(alias="intelligencePriority")]
    speed_priority: Annotated[NotRequired[float], Field(alias="speedPriority")]


class Notification(TypedDict):
    method: str
    params: NotRequired[NotificationParams]


@with_config(extra="allow")
class NotificationParamsMeta(TypedDict):
    pass


class MultiSelectEnumSchemaNotificationParams(TypedDict):
    _meta: NotRequired[NotificationParamsMeta]


class NumberSchema(TypedDict):
    default: NotRequired[int]
    description: NotRequired[str]
    maximum: NotRequired[int]
    minimum: NotRequired[int]
    title: NotRequired[str]
    type: str


class PaginatedRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class PaginatedRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsPaginatedRequestParams(TypedDict):
    _meta: NotRequired[PaginatedRequestParamsMeta]
    cursor: NotRequired[str]


@with_config(extra="allow")
class PaginatedResultMeta(TypedDict):
    pass


class PaginatedResult(TypedDict):
    _meta: NotRequired[PaginatedResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]


class ProgressTokenPingRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["ping"]
    params: NotRequired[RequestParams]


class StringSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    format: NotRequired[str]
    max_length: Annotated[NotRequired[int], Field(alias="maxLength")]
    min_length: Annotated[NotRequired[int], Field(alias="minLength")]
    title: NotRequired[str]
    type: Literal["string"]


class PrimitiveSchemaDefinitionProgressNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/progress"]
    params: ProgressNotificationParams


@with_config(extra="allow")
class ProgressNotificationParamsMeta(TypedDict):
    pass


class ParamsProgressNotificationParams(TypedDict):
    _meta: NotRequired[ProgressNotificationParamsMeta]
    message: NotRequired[str]
    progress: float
    progress_token: Annotated[str | int, Field(alias="progressToken")]
    total: NotRequired[float]


@with_config(extra="allow")
class PromptMeta(TypedDict):
    pass


class ProgressTokenPrompt(TypedDict):
    _meta: NotRequired[PromptMeta]
    arguments: NotRequired[list[PromptArgument]]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    name: str
    title: NotRequired[str]


class ProgressTokenPromptArgument(TypedDict):
    description: NotRequired[str]
    name: str
    required: NotRequired[bool]
    title: NotRequired[str]


class PromptListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/prompts/list_changed"]
    params: NotRequired[NotificationParams]


class ParamsPromptMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource
    role: str


class RolePromptReference(TypedDict):
    name: str
    title: NotRequired[str]
    type: Literal["ref/prompt"]


class RoleReadResourceRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/read"]
    params: ReadResourceRequestParams


@with_config(extra="allow")
class ReadResourceRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsReadResourceRequestParams(TypedDict):
    _meta: NotRequired[ReadResourceRequestParamsMeta]
    uri: str


@with_config(extra="allow")
class ReadResourceResultMeta(TypedDict):
    pass


class ReadResourceResult(TypedDict):
    _meta: NotRequired[ReadResourceResultMeta]
    contents: list[TextResourceContents | BlobResourceContents]


class RelatedTaskMetadata(TypedDict):
    task_id: Annotated[str, Field(alias="taskId")]


class Request(TypedDict):
    method: str
    params: NotRequired[RequestParams]


@with_config(extra="allow")
class RequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ProgressTokenRequestParams(TypedDict):
    _meta: NotRequired[RequestParamsMeta]


class ProgressTokenResource(TypedDict):
    _meta: NotRequired[ResourceMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    uri: str


@with_config(extra="allow")
class ResourceContentsMeta(TypedDict):
    pass


class ResourceContents(TypedDict):
    _meta: NotRequired[ResourceContentsMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    uri: str


@with_config(extra="allow")
class ResourceLinkMeta(TypedDict):
    pass


class AnnotationsResourceLink(TypedDict):
    _meta: NotRequired[ResourceLinkMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    type: Literal["resource_link"]
    uri: str


class ResourceListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/resources/list_changed"]
    params: NotRequired[NotificationParams]


@with_config(extra="allow")
class ResourceRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ResourceRequestParams(TypedDict):
    _meta: NotRequired[ResourceRequestParamsMeta]
    uri: str


@with_config(extra="allow")
class ResourceTemplateMeta(TypedDict):
    pass


class ProgressTokenResourceTemplate(TypedDict):
    _meta: NotRequired[ResourceTemplateMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    icons: NotRequired[list[Icon]]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    title: NotRequired[str]
    uri_template: Annotated[str, Field(alias="uriTemplate")]


class AnnotationsResourceTemplateReference(TypedDict):
    type: Literal["ref/resource"]
    uri: str


class ResourceUpdatedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]
    uri: str


class ResourceUpdatedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/resources/updated"]
    params: ResourceUpdatedNotificationParams


@with_config(extra="allow")
class ResourceUpdatedNotificationParamsMeta(TypedDict):
    pass


class ParamsResourceUpdatedNotificationParams(TypedDict):
    _meta: NotRequired[ResourceUpdatedNotificationParamsMeta]
    uri: str


@with_config(extra="allow")
class ResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ParamsResult(TypedDict):
    _meta: NotRequired[ResultMeta]


@with_config(extra="allow")
class RootMeta(TypedDict):
    pass


class ParamsRoot(TypedDict):
    _meta: NotRequired[RootMeta]
    name: NotRequired[str]
    uri: str


class ParamsRootsListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/roots/list_changed"]
    params: NotRequired[NotificationParams]


@with_config(extra="allow")
class SamplingMessageMeta(TypedDict):
    pass


class ParamsSamplingMessage(TypedDict):
    _meta: NotRequired[SamplingMessageMeta]
    content: (
        TextContent
        | ImageContent
        | AudioContent
        | ToolUseContent
        | ToolResultContent
        | list[TextContent | ImageContent | AudioContent | ToolUseContent | ToolResultContent]
    )
    role: str


@with_config(extra="allow")
class ServerCapabilitiesCompletions(TypedDict):
    pass


@with_config(extra="allow")
class ServerCapabilitiesExperimental(TypedDict):
    pass


@with_config(extra="allow")
class ServerCapabilitiesLogging(TypedDict):
    pass


class ServerCapabilitiesPrompts(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class ServerCapabilitiesResources(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]
    subscribe: NotRequired[bool]


class ServerCapabilitiesTasks(TypedDict):
    cancel: NotRequired[TasksCancel]
    list: NotRequired[TasksList]
    requests: NotRequired[TasksRequests]


class ServerCapabilitiesTools(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class SamplingMessageContentBlockServerCapabilities(TypedDict):
    completions: NotRequired[ServerCapabilitiesCompletions]
    experimental: NotRequired[ServerCapabilitiesExperimental]
    logging: NotRequired[ServerCapabilitiesLogging]
    prompts: NotRequired[ServerCapabilitiesPrompts]
    resources: NotRequired[ServerCapabilitiesResources]
    tasks: NotRequired[ServerCapabilitiesTasks]
    tools: NotRequired[ServerCapabilitiesTools]


class ToolListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/tools/list_changed"]
    params: NotRequired[NotificationParams]


class ServerResultSetLevelRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["logging/setLevel"]
    params: SetLevelRequestParams


@with_config(extra="allow")
class SetLevelRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsSetLevelRequestParams(TypedDict):
    _meta: NotRequired[SetLevelRequestParamsMeta]
    level: str


class SingleSelectEnumSchemaStringSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    format: NotRequired[str]
    max_length: Annotated[NotRequired[int], Field(alias="maxLength")]
    min_length: Annotated[NotRequired[int], Field(alias="minLength")]
    title: NotRequired[str]
    type: Literal["string"]


class SingleSelectEnumSchemaSubscribeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/subscribe"]
    params: SubscribeRequestParams


@with_config(extra="allow")
class SubscribeRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsSubscribeRequestParams(TypedDict):
    _meta: NotRequired[SubscribeRequestParamsMeta]
    uri: str


class ProgressTokenTask(TypedDict):
    created_at: Annotated[str, Field(alias="createdAt")]
    last_updated_at: Annotated[str, Field(alias="lastUpdatedAt")]
    poll_interval: Annotated[NotRequired[int], Field(alias="pollInterval")]
    status: str
    status_message: Annotated[NotRequired[str], Field(alias="statusMessage")]
    task_id: Annotated[str, Field(alias="taskId")]
    ttl: int


@with_config(extra="allow")
class TaskAugmentedRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class TaskAugmentedRequestParams(TypedDict):
    _meta: NotRequired[TaskAugmentedRequestParamsMeta]
    task: NotRequired[TaskMetadata]


class TaskTaskMetadata(TypedDict):
    ttl: NotRequired[int]


class TaskTaskStatusNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/tasks/status"]
    params: Any


@with_config(extra="allow")
class TextContentMeta(TypedDict):
    pass


class ParamsTextContent(TypedDict):
    _meta: NotRequired[TextContentMeta]
    annotations: NotRequired[Annotations]
    text: str
    type: Literal["text"]


@with_config(extra="allow")
class TextResourceContentsMeta(TypedDict):
    pass


class AnnotationsTextResourceContents(TypedDict):
    _meta: NotRequired[TextResourceContentsMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    text: str
    uri: str


class TitledMultiSelectEnumSchemaItems(TypedDict):
    any_of: Annotated[list[ItemsGeneratedType], Field(alias="anyOf")]


class AnnotationsTitledMultiSelectEnumSchema(TypedDict):
    default: NotRequired[list[str]]
    description: NotRequired[str]
    items: TitledMultiSelectEnumSchemaItems
    max_items: Annotated[NotRequired[int], Field(alias="maxItems")]
    min_items: Annotated[NotRequired[int], Field(alias="minItems")]
    title: NotRequired[str]
    type: Literal["array"]


class TitledSingleSelectEnumSchemaGeneratedType(TypedDict):
    const: str
    title: str


class AnnotationsTitledSingleSelectEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    one_of: Annotated[list[TitledSingleSelectEnumSchemaGeneratedType], Field(alias="oneOf")]
    title: NotRequired[str]
    type: Literal["string"]


@with_config(extra="allow")
class ToolMeta(TypedDict):
    pass


@with_config(extra="allow")
class InputSchemaProperties(TypedDict):
    pass


class ExecutionInputSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: NotRequired[InputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class ExecutionOutputSchema(TypedDict):
    schema: Annotated[NotRequired[str], Field(alias="$schema")]
    properties: NotRequired[OutputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class AnnotationsTool(TypedDict):
    _meta: NotRequired[ToolMeta]
    annotations: NotRequired[ToolAnnotations]
    description: NotRequired[str]
    execution: NotRequired[ToolExecution]
    icons: NotRequired[list[Icon]]
    input_schema: Annotated[ExecutionInputSchema, Field(alias="inputSchema")]
    name: str
    output_schema: Annotated[NotRequired[ExecutionOutputSchema], Field(alias="outputSchema")]
    title: NotRequired[str]


class ExecutionToolAnnotations(TypedDict):
    destructive_hint: Annotated[NotRequired[bool], Field(alias="destructiveHint")]
    idempotent_hint: Annotated[NotRequired[bool], Field(alias="idempotentHint")]
    open_world_hint: Annotated[NotRequired[bool], Field(alias="openWorldHint")]
    read_only_hint: Annotated[NotRequired[bool], Field(alias="readOnlyHint")]
    title: NotRequired[str]


class ExecutionToolChoice(TypedDict):
    mode: NotRequired[str]


class ExecutionToolExecution(TypedDict):
    task_support: Annotated[NotRequired[str], Field(alias="taskSupport")]


class ExecutionToolListChangedNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: Literal["notifications/tools/list_changed"]
    params: NotRequired[NotificationParams]


@with_config(extra="allow")
class ToolResultContentMeta(TypedDict):
    pass


class ParamsToolResultContent(TypedDict):
    _meta: NotRequired[ToolResultContentMeta]
    content: list[TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource]
    is_error: Annotated[NotRequired[bool], Field(alias="isError")]
    structured_content: Annotated[NotRequired[ContentBlockStructuredContent], Field(alias="structuredContent")]
    tool_use_id: Annotated[str, Field(alias="toolUseId")]
    type: Literal["tool_result"]


@with_config(extra="allow")
class ToolUseContentMeta(TypedDict):
    pass


@with_config(extra="allow")
class ToolUseContentInput(TypedDict):
    pass


class ContentBlockToolUseContent(TypedDict):
    _meta: NotRequired[ToolUseContentMeta]
    id: str
    input: ToolUseContentInput
    name: str
    type: Literal["tool_use"]


class URLElicitationRequiredError(TypedDict):
    error: Any
    id: NotRequired[str | int]
    jsonrpc: Literal["2.0"]


class IdUnsubscribeRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: Literal["resources/unsubscribe"]
    params: UnsubscribeRequestParams


@with_config(extra="allow")
class UnsubscribeRequestParamsMeta(TypedDict):
    progress_token: Annotated[NotRequired[str | int], Field(alias="progressToken")]


class ParamsUnsubscribeRequestParams(TypedDict):
    _meta: NotRequired[UnsubscribeRequestParamsMeta]
    uri: str


class UntitledMultiSelectEnumSchemaItems(TypedDict):
    enum: list[str]
    type: Literal["string"]


class ProgressTokenUntitledMultiSelectEnumSchema(TypedDict):
    default: NotRequired[list[str]]
    description: NotRequired[str]
    items: UntitledMultiSelectEnumSchemaItems
    max_items: Annotated[NotRequired[int], Field(alias="maxItems")]
    min_items: Annotated[NotRequired[int], Field(alias="minItems")]
    title: NotRequired[str]
    type: Literal["array"]


class ProgressTokenUntitledSingleSelectEnumSchema(TypedDict):
    default: NotRequired[str]
    description: NotRequired[str]
    enum: list[str]
    title: NotRequired[str]
    type: Literal["string"]
